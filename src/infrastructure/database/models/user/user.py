from bson import ObjectId
from typing import TypedDict
from datetime import datetime


class User(TypedDict):
    _id: ObjectId
    username: str
    password: str
    password_salt: str
    email: str
    created_on: datetime
    last_login: datetime | None
    is_admin: bool
    is_banned: bool
    avg_rating: float
    rate_count: int
    followers_count: int
    following_count: int
    favourites_count: int
    rate_value: int
    is_verified: bool
    updated_at: datetime
    verification_code: str | None
    change_password_code: str | None
