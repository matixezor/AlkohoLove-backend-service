from src.domain.common import PageInfo
from src.domain.common.base_model import BaseModel
from src.domain.user.user_social import UserSocial, ExtendedUserSocial


class PaginatedUserSocial(BaseModel):
    users: list[UserSocial]
    page_info: PageInfo


class PaginatedExtendedUserSocial(PaginatedUserSocial):
    users: list[ExtendedUserSocial]

