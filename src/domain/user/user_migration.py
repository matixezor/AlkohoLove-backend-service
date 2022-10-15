from pydantic import validator

from src.domain.common.base_model import BaseModel
from src.domain.user_tag.user_tag_migrate import UserTagMigrate
from src.infrastructure.common.validate_object_id import validate_object_id
from src.domain.alcohol.alcohol_history_migrate import AlcoholHistoryMigrate


class UserMigration(BaseModel):
    wishlist: list[str]
    search_history: list[AlcoholHistoryMigrate]
    favourites: list[str]
    tags: list[UserTagMigrate]

    @validator('wishlist', 'favourites', each_item=True)
    def check_alcohol_id(cls, value: str):
        validate_object_id(value)
        return value
