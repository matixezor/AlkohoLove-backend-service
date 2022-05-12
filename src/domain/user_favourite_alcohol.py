from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.alcohol import AlcoholBasicInfo


class UserFavouriteAlcohol(BaseModel):
    user_id: int
    alcohol_ids: list[int] = []

    class Config:
        orm_mode = True




class PaginatedUserFavouriteAlcohol(BaseModel):
    alcohols: list[AlcoholBasicInfo] | None
    page_info: PageInfo

    class Config:
        orm_mode = True


