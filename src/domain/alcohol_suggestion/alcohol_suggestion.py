from pydantic import BaseModel, Field, validator
from src.domain.common import MongoBaseModel, PyObjectId


class AlcoholSuggestion(MongoBaseModel, BaseModel):
    user_ids: list[PyObjectId] = Field(default_factory=PyObjectId, alias="user_ids")
    barcode: str
    kind: str
    name: str
    descriptions: list[str]

    @validator('user_ids', always=True)
    def set_id(cls, v):
        for i in range(len(v)):
            v[i] = str(v[i])
        return v
