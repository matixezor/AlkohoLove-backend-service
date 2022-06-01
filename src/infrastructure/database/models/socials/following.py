from bson import ObjectId
from typing import TypedDict


class Following(TypedDict):
    _id: ObjectId
    following: list[ObjectId]
