from bson import ObjectId
from typing_extensions import TypedDict


class AlcoholSuggestion(TypedDict):
    _id: ObjectId
    user_ids: list[ObjectId]
    barcode: str
    kind: str
    name: str
    descriptions: list[str|None] | None
