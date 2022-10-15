from src.domain.common import PageInfo
from src.domain.user_tag import UserTag
from src.domain.common.base_model import BaseModel


class PaginatedUserTags(BaseModel):
    user_tags: list[UserTag]
    page_info: PageInfo
