from bson import ObjectId
from typing import TypedDict

from src.domain.user.user_basic_info import UserBasicInfo


class Followers(TypedDict):
    _id: ObjectId
    followers: list[UserBasicInfo]
