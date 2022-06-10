from pydantic import validator

from src.domain.review import ReviewBase


class ReviewUpdate(ReviewBase):

    @validator('rating')
    def rating_validator(cls, value: int) -> int:
        if (value > 5) or (value < 1):
            raise ValueError('Rating should be number from 1 to 5')
        return value
