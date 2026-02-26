from pydantic import BaseModel


class GoogleUserData(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    access_token: str
