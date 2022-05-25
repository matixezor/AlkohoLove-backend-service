from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user.lists.user_list import UserWishlist


class PaginatedUserWishlist(BaseModel):
    alcohols: list[UserWishlist]
    page_info: PageInfo
