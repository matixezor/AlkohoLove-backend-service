from src.domain.common.base_model import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
