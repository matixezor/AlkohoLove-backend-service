from src.domain.common.base_model import BaseModel


class PageInfo(BaseModel):
    offset: int
    limit: int
    total: int
