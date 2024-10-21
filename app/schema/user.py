from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserBaseSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserBaseSchema):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None
    name: str | None = None
