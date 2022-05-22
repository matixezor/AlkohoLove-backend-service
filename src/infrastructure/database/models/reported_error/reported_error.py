from bson import ObjectId
from typing import TypedDict


class ReportedError(TypedDict):
    _id: ObjectId
    user_id: ObjectId
    description: str
