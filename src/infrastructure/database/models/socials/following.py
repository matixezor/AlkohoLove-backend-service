from bson import ObjectId
from typing import TypedDict

from src.domain.user.user_basic_info import UserBasicInfo


class Following(TypedDict):
    _id: ObjectId
    following: list[UserBasicInfo]
