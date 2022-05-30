from bson import ObjectId
from typing import TypedDict

from src.domain.user.user_basic_info import FollowUserBasicInfo


class Following(TypedDict):
    _id: ObjectId
    following: list[FollowUserBasicInfo]
