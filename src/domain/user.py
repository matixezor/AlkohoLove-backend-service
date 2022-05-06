from re import compile
from datetime import datetime
from pydantic import BaseModel, validator, root_validator

from src.domain.page_info import PageInfo

email_pattern = compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}')
password_pattern = compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class User(UserBase):
    email: str


class UserCreate(User):
    password: str

    @validator('email')
    def email_match(cls, value: str) -> str:
        if not email_pattern.match(value):
            raise ValueError('Invalid email')
        return value

    @validator('password')
    def password_validator(cls, value: str) -> str:
        if not password_pattern.match(value):
            raise ValueError('Password does not comply with rules')
        return value


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    new_password: str | None = None

    @validator('email')
    def email_match(cls, value: str | None) -> str:
        if value and not email_pattern.match(value):
            raise ValueError('Invalid email')
        return value

    @root_validator(pre=True)
    def any_of(cls, values: dict):
        if not any(values.values()):
            raise ValueError('At least one value needs to be provided')
        return values

    @validator('new_password')
    def password_validator(cls, value: str) -> str:
        if not password_pattern.match(value):
            raise ValueError('New password does not comply with rules')
        return value


class UserAdminUpdate(UserCreate):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    is_banned: bool | None = None
    last_login: datetime | None = None


class UserAdminInfo(User):
    user_id: int
    is_banned: bool
    last_login: datetime | None = None
    created_on: datetime


class PaginatedUserAdminInfo(BaseModel):
    users: list[UserAdminInfo]
    page_info: PageInfo
