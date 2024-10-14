from typing import Annotated

from pydantic import BaseModel, model_validator, Field


class TaskBaseSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    @model_validator(mode='after')
    def check_name_and_pomodoro(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Task name and pomodoro count should be provided")
        return self


class TaskSchema(TaskBaseSchema):
    id: int

    class Config:
        from_attributes = True



