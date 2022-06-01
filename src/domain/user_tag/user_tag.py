from src.domain.user_tag import UserTagBase
from src.domain.common import MongoBaseModel


class UserTag(MongoBaseModel, UserTagBase):
    pass
