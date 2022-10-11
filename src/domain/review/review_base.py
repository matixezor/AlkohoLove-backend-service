from src.domain.common.base_model import BaseModel


class ReviewBase(BaseModel):
    review: str
    rating: int
