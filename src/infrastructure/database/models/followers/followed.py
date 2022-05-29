from bson import ObjectId
from typing import TypedDict

from src.domain.user.user_basic_info import UserBasicInfo


class Followed(TypedDict):
    _id: ObjectId
    followed: list[UserBasicInfo]
