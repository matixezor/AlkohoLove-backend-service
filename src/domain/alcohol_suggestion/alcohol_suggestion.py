from pydantic import Field, validator

from src.domain.alcohol_suggestion.alcohol_suggestion_base import AlcoholSuggestionBase
from src.domain.common import MongoBaseModel, PyObjectId


class AlcoholSuggestion(MongoBaseModel, AlcoholSuggestionBase):
    user_ids: list[PyObjectId] = Field(default_factory=PyObjectId, alias="user_ids")

    @validator('user_ids', always=True)
    def set_id(cls, v):
        for i in range(len(v)):
            v[i] = str(v[i])
        return v
