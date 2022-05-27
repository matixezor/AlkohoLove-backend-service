from pydantic import BaseModel

from src.domain.alcohol import Alcohol
from src.domain.common import PageInfo


class PaginatedUserWishlist(BaseModel):
    alcohols: list[Alcohol]
    page_info: PageInfo
