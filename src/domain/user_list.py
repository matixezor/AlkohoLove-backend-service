from datetime import datetime
from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBase


class UserList(BaseModel):
    alcohol: AlcoholBase

    class Config:
        orm_mode = True


class UserSearchHistory(UserList):
    date: datetime

    class Config:
        orm_mode = True


class PaginatedUserSearchHistory(BaseModel):
    alcohols: list[UserSearchHistory]
    page_info: PageInfo

    class Config:
        orm_mode = True


class PaginatedUserList(BaseModel):
    alcohols: list[UserList]
    page_info: PageInfo

    class Config:
        orm_mode = True
