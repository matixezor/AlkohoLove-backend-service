from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.review.user_review import UserReview


class PaginatedUserReview(BaseModel):
    reviews: list[UserReview]
    page_info: PageInfo
