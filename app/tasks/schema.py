
from pydantic import BaseModel, model_validator, ConfigDict


class TaskSchema(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int
    user_id: int


    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_non(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self

    model_config = ConfigDict(
        from_attributes=True
    )

class TaskCreateSchema(BaseModel):
    name: str
    pomodoro_count: int
    category_id: int
    user_id: int


class TaskCategorySchema(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
