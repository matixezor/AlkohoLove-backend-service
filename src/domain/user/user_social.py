from datetime import datetime

from src.domain.common import MongoBaseModel
from src.domain.user.user_social_base import UserSocialBase


class UserSocial(MongoBaseModel, UserSocialBase):
    pass


class ExtendedUserSocial(UserSocial):
    created_on: datetime
    favourites_count: int
