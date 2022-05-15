from datetime import datetime

from pydantic import BaseModel
from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBase


class Date(BaseModel):
    date: datetime


class UserSearchHistory(BaseModel):
    date: datetime
    alcohol: AlcoholBase

    class Config:
        orm_mode = True


class PaginatedUserSearchHistory(BaseModel):
    alcohols: list[UserSearchHistory]
    page_info: PageInfo

    class Config:
        orm_mode = True


class PaginatedUserList(BaseModel):
    alcohols: list[AlcoholBase]
    page_info: PageInfo

    class Config:
        orm_mode = True



