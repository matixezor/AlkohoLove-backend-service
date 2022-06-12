from pydantic import BaseModel


class ReviewBase(BaseModel):
    review: str
    rating: int
