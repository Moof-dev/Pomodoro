from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    username: str
    password: str

class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str

