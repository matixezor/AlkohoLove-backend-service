from pydantic import BaseModel

from src.domain.common import MongoBaseModel
from src.domain.user.user_social_base import UserSocialBase


class UserSocial(MongoBaseModel, UserSocialBase):
    pass
