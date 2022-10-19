from pydantic import validator

from src.domain.user_tag import UserTagBase
from src.infrastructure.common.validate_object_id import validate_object_id


class UserTagMigrate(UserTagBase):
    alcohols: list[str]

    @validator('alcohols', each_item=True)
    def check_alcohol_id(cls, value: str):
        validate_object_id(value)
        return value
