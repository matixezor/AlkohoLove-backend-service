from src.domain.common import PageInfo
from src.domain.common.base_model import BaseModel
from src.domain.user_list.search_history_entry import SearchHistoryEntry


class PaginatedSearchHistory(BaseModel):
    alcohols: list[SearchHistoryEntry]
    page_info: PageInfo
