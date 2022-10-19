from datetime import datetime
from pydantic import validator

from src.domain.common.base_model import BaseModel
from src.infrastructure.common.validate_object_id import validate_object_id


class AlcoholHistoryMigrate(BaseModel):
    alcohol_id: str
    date: datetime

    @validator('alcohol_id', pre=True)
    def check_alcohol_id(cls, value: str):
        validate_object_id(value)
        return value
