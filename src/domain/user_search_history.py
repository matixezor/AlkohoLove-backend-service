from datetime import datetime

from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholSearchHistoryInfo


class UserSearchHistory(BaseModel):
    user_id: int
    alcohol_ids: list[int] = []
    date: datetime | None = None

    class Config:
        orm_mode = True


class PaginatedUserSearchHistory(BaseModel):
    alcohols: list[AlcoholSearchHistoryInfo]
    page_info: PageInfo

    class Config:
        orm_mode = True
