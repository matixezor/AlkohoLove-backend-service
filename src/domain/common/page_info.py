from pydantic import BaseModel


class PageInfo(BaseModel):
    offset: int
    limit: int
    total: int
