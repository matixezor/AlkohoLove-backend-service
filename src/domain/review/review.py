from src.domain.review import ReviewBase
from src.domain.common import MongoBaseModel
from datetime import datetime


class Review(MongoBaseModel, ReviewBase):
    user_name: str
    date: datetime
