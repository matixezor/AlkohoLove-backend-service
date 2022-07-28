from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.review import ReportedReview


class PaginatedReportedReview(BaseModel):
    reviews: list[ReportedReview]
    page_info: PageInfo