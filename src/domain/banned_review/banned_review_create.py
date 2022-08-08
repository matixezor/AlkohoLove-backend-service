from pydantic import validator

from src.domain.banned_review import BannedReviewBase


class BannedReviewCreate(BannedReviewBase):
    pass
