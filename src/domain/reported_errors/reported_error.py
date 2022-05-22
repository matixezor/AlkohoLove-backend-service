from pydantic import validator, Field

from src.domain.common import PyObjectId
from src.domain.common import MongoBaseModel
from src.domain.reported_errors import ReportedErrorBase


class ReportedError(MongoBaseModel, ReportedErrorBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")

    @validator('user_id', always=True)
    def set_user_id(cls, v):
        return str(v)
