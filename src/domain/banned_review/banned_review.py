from datetime import datetime
from pydantic import Field, validator

from src.domain.banned_review import BannedReviewBase
from src.domain.common import PyObjectId
from src.domain.common import MongoBaseModel


class BannedReview(MongoBaseModel, BannedReviewBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")
    username: str
    date: datetime
    alcohol_id: PyObjectId = Field(default_factory=PyObjectId, alias="alcohol_id")
    report_count: int
    reporters: list[PyObjectId] = Field(default_factory=PyObjectId, alias="reporters")
    ban_date: datetime
    reason: str

    @validator('alcohol_id', always=True)
    def set_alcohol_id(cls, v):
        return str(v)

    @validator('user_id', always=True)
    def set_user_id(cls, v):
        return str(v)

    @validator('reporters', always=True)
    def set_reporters_id(cls, v):
        return [str(user_id) for user_id in v]
