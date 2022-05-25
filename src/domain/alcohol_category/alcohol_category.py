from pydantic import BaseModel

from src.domain.common import MongoBaseModel
from src.domain.alcohol_category.alcohol_category_property import PropertyOut


class AlcoholCategory(MongoBaseModel, BaseModel):
    properties: list[PropertyOut]
    title: str
    required: list[str] | None
