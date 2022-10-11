from src.domain.common.base_model import BaseModel


class BannedReviewBase(BaseModel):
    review: str
    rating: int
