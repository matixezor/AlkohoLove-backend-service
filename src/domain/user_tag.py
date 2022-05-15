from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBasicInfo, Alcohol


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
    alcohols: list[AlcoholBasicInfo]
    page_info: PageInfo
