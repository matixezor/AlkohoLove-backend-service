from pydantic import Field, validator

from src.domain.common import MongoBaseModel, PyObjectId
from src.domain.alcohol_suggestion.alcohol_suggestion_base import AlcoholSuggestionBase


class AlcoholSuggestion(MongoBaseModel, AlcoholSuggestionBase):
    user_ids: list[PyObjectId] = Field(default_factory=PyObjectId, alias="user_ids")
    descriptions: list[str] | None

    @validator('user_ids', always=True)
    def set_id(cls, v):
        for i in range(len(v)):
            v[i] = str(v[i])
        return v
