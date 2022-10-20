from datetime import datetime
from src.domain.common import MongoBaseModel
from src.domain.user.user_social_base import UserSocialBase


class UserInfo(MongoBaseModel, UserSocialBase):
    created_on: datetime
    avg_rating: float
    rate_count: int
    followers_count: int
    following_count: int
    favourites_count: int
