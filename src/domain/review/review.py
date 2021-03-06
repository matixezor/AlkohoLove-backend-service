from datetime import datetime
from pydantic import Field, validator

from src.domain.review import ReviewBase
from src.domain.common import PyObjectId
from src.domain.common import MongoBaseModel


class Review(MongoBaseModel, ReviewBase):
    username: str
    date: datetime
    alcohol_id: PyObjectId = Field(default_factory=PyObjectId, alias="alcohol_id")

    @validator('alcohol_id', always=True)
    def set_user_id(cls, v):
        return str(v)
