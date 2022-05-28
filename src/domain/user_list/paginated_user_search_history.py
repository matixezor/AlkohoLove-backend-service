from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user_list.user_search_history import UserSearchHistoryEntry


class PaginatedUserSearchHistory(BaseModel):
    alcohols: list[UserSearchHistoryEntry]
    page_info: PageInfo
