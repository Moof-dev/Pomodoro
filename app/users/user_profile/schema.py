from pydantic import BaseModel, Field, model_validator

from app.exception import BadRequestException


class UserCreateSchema(BaseModel):
    username: str | None = Field(None, min_length=4, max_length=20)
    password: str | None = Field(None, min_length=8)
    email: str | None = None
    name: str | None = None
    google_access_token: str | None = None

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_non(self):
        if not ((self.username and self.password) or self.google_access_token):
            raise BadRequestException
        return self

