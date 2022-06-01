from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user.user_social import UserSocial


class PaginatedUserSocial(BaseModel):
    users: list[UserSocial]
    page_info: PageInfo
