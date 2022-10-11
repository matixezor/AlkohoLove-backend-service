from src.domain.common import PageInfo
from src.domain.user import UserAdminInfo
from src.domain.common.base_model import BaseModel


class PaginatedUserAdminInfo(BaseModel):
    users: list[UserAdminInfo]
    page_info: PageInfo
