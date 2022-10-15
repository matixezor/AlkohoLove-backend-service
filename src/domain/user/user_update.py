from pydantic import validator, root_validator

from src.domain.common.base_model import BaseModel
from src.infrastructure.config.patterns import email_pattern, password_pattern


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
