from datetime import datetime

from src.domain.alcohol import AlcoholBase
from src.domain.common import MongoBaseModel


class Alcohol(MongoBaseModel, AlcoholBase):
    avg_rating: float
    rate_count: int
    rate_value: int
    username: str | None
    date: datetime | None
