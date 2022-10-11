from src.domain.common.base_model import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
