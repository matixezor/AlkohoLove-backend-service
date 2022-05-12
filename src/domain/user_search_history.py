import datetime

from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBasicInfo


class UserSearchHistory(BaseModel):
    user_id: int
    alcohol_ids: list[int] = []
    date: datetime.date

    class Config:
        orm_mode = True


class PaginatedUserSearchHistory(BaseModel):
    alcohols: list[AlcoholBasicInfo]
    date: datetime.date
    page_info: PageInfo
