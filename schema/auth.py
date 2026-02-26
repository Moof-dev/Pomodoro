from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    username: str
    password: str

class GoogleUserData(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    access_token: str
