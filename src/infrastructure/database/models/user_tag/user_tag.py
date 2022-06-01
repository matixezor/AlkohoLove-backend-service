from bson import ObjectId
from typing import TypedDict


class UserTag(TypedDict):
    _id: ObjectId
    user_id: ObjectId
    tag_name: str
    alcohols: list[ObjectId]
