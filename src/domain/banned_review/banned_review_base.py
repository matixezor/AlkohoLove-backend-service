from pydantic import BaseModel


class BannedReviewBase(BaseModel):
    review: str
    rating: int
