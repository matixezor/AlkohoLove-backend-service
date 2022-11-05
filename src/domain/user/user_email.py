from pydantic import validator, BaseModel

from src.infrastructure.config.patterns import email_pattern


class UserEmail(BaseModel):
    email: str


@validator('email')
def email_match(cls, value: str) -> str:
    if not email_pattern.match(value):
        raise ValueError('Invalid email')
    return value
