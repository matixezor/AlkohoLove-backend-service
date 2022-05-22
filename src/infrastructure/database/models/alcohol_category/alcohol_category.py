from bson import ObjectId
from typing import TypedDict


class AlcoholCategory(TypedDict):
    _id: ObjectId
    properties: dict
    required: list[str]
    title: str
