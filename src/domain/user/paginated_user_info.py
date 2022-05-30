from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user.user_basic_info import FollowUserBasicInfo


class PaginatedFollowUserInfo(BaseModel):
    users: list[FollowUserBasicInfo]
    page_info: PageInfo
