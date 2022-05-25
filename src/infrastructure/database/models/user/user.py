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
