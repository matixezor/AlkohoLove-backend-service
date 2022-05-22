from pydantic import BaseModel

from src.domain.alcohol import AlcoholBase
from src.domain.common.page_info import PageInfo


class UserTag(BaseModel):
    tag_id: int
    tag_name: str

    class Config:
        orm_mode = True


class UserTagCreate(BaseModel):
    tag_name: str
    alcohol_ids: list[int] = []


class UserTagUpdate(BaseModel):
    tag_name: str


class PaginatedUserTag(BaseModel):
    user_tags: list[UserTag]
    page_info: PageInfo


class PaginatedUserTagAlcohols(BaseModel):
    alcohols: list[AlcoholBase]
    page_info: PageInfo
