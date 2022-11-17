from pydantic import validator, BaseModel

from src.infrastructure.config.patterns import password_pattern


class UserChangePassword(BaseModel):
    token: str
    new_password: str

    @validator('new_password')
    def password_validator(cls, value: str) -> str:
        if not password_pattern.match(value):
            raise ValueError('Password does not comply with rules')
        return value
