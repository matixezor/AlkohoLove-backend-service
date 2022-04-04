from re import compile
from pydantic import BaseModel, validator


email_pattern = compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}')
password_pattern = compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')


class UserBase(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
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


class User(UserBase):
    user_id: int
