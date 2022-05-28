from typing import TypedDict
from bson import ObjectId

from src.domain.user_list.search_history import SearchHistoryEntry


class UserSearchHistory(TypedDict):
    _id: ObjectId
    user_id: ObjectId
    alcohols: list[SearchHistoryEntry]