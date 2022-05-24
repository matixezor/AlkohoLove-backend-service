from src.domain.user import UserBase
from src.domain.common import MongoBaseModel


class User(MongoBaseModel, UserBase):
    pass
