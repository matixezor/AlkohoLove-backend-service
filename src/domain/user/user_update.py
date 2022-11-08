from pydantic import validator, root_validator

from src.domain.common.base_model import BaseModel
from src.infrastructure.config.patterns import email_pattern, password_pattern


class UserUpdate(BaseModel):
    email: str | None = None

    @validator('email')
    def email_match(cls, value: str | None) -> str:
        if value and not email_pattern.match(value):
            raise ValueError('Invalid email')
        return value
