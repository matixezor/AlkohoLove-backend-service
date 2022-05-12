from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBasicInfo


class UserWishlist(BaseModel):
    user_id: int
    alcohol_ids: list[int] = []

    class Config:
        orm_mode = True


class PaginatedUserWishlist(BaseModel):
    alcohols: list[AlcoholBasicInfo]
    page_info: PageInfo

    class Config:
        orm_mode = True
