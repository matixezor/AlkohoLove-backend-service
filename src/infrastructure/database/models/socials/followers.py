from bson import ObjectId
from typing import TypedDict

from src.domain.user.user_basic_info import FollowUserBasicInfo


class Followers(TypedDict):
    _id: ObjectId
    followers: list[FollowUserBasicInfo]
