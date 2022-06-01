from bson import ObjectId
from typing import TypedDict


class Followers(TypedDict):
    _id: ObjectId
    followers: list[ObjectId]
