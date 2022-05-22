from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user import UserAdminInfo


class PaginatedUserAdminInfo(BaseModel):
    users: list[UserAdminInfo]
    page_info: PageInfo
