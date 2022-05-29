from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user.user_basic_info import UserBasicInfo


class PaginatedUserInfo(BaseModel):
    users: list[UserBasicInfo]
    page_info: PageInfo