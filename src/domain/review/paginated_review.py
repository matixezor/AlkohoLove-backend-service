from src.domain.review import Review
from src.domain.common import PageInfo
from src.domain.common.base_model import BaseModel


class PaginatedReview(BaseModel):
    reviews: list[Review]
    page_info: PageInfo
