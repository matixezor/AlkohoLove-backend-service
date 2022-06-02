from bson import ObjectId
from typing import TypedDict

from src.domain.user_list.search_history_entry import SearchHistoryEntry


class UserSearchHistory(TypedDict):
    _id: ObjectId
    user_id: ObjectId
    alcohols: list[SearchHistoryEntry]
