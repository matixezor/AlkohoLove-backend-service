from typing import TypedDict
from bson import ObjectId

from src.domain.alcohol import AlcoholBase


class UserWishlist(TypedDict):
    _id: ObjectId
    user_id: ObjectId
    alcohols: list[AlcoholBase]
