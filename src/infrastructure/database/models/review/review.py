from bson import ObjectId
from typing import TypedDict
from datetime import datetime


class Review(TypedDict):
    _id: ObjectId
    username: str
    user_id: ObjectId
    alcohol_id: ObjectId
    review: str
    rating: int
    date: datetime
    report_count: int
    reporters: list[ObjectId]
    helpful_count: int
    helpful_reporters: list[ObjectId]
