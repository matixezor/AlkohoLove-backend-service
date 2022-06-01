from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.review import Review


class PaginatedReview(BaseModel):
    reviews: list[Review]
    page_info: PageInfo
