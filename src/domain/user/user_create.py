from datetime import datetime
from pydantic import validator

from src.domain.user import UserBase
from src.infrastructure.config.patterns import email_pattern, password_pattern


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
