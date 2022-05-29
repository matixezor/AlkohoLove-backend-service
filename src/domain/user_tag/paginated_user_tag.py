from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.user_tag import UserTag


class PaginatedUserTags(BaseModel):
    user_tags: list[UserTag]
    page_info: PageInfo
