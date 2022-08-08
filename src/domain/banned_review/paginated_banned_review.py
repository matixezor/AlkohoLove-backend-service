from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.banned_review import BannedReview


class PaginatedBannedReview(BaseModel):
    reviews: list[BannedReview]
    page_info: PageInfo
