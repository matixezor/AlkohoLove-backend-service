from pydantic import validator

from src.domain.review import ReviewBase
from src.infrastructure.exceptions.review_exceptions import WrongRatingValueException


class ReviewCreate(ReviewBase):

    @validator('rating')
    def rating_validator(cls, value: int) -> int:
        if not 1 <= value <= 5:
            raise WrongRatingValueException()
        return value
