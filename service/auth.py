from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt, JWTError

from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from settings import Setting

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmUiOjE3NzI1ODM3OTcuMDg2NzA1fQ.eDOIxV5cUK_iF4ZxmQLNVXYGtRLqkPJ12LAFibgwrp8
@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Setting

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)


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

