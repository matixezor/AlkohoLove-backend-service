from bson import ObjectId
from typing import TypedDict


class AlcoholSuggestion(TypedDict):
    _id: ObjectId
    user_ids: list[ObjectId]
    barcode: str
    kind: str
    name: str
    description: list[str]
