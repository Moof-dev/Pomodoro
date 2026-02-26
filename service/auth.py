from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt, JWTError

from client import GoogleClient
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema
from settings import Setting

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmUiOjE3NzI1ODM3OTcuMDg2NzA1fQ.eDOIxV5cUK_iF4ZxmQLNVXYGtRLqkPJ12LAFibgwrp8
@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Setting
    google_client: GoogleClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)


    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.now(dt.UTC) + timedelta(days=7)).timestamp()
        access_token = jwt.encode({"user_id": user_id, "expire": expires_date_unix},
                                  key=self.settings.JWT_SECRET_KEY,
                                  algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return access_token

    def get_user_id_from_access_token(self,access_token: str) -> int:
        try:
            encode_token = jwt.decode(access_token, key=self.settings.JWT_SECRET_KEY,
                                      algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect

        if encode_token["expire"] < (dt.datetime.now(dt.UTC)).timestamp():
            raise TokenExpired
        return encode_token["user_id"]

