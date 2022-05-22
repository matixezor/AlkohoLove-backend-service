from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.alcohol import Alcohol


class PaginatedAlcohol(BaseModel):
    alcohols: list[Alcohol]
    page_info: PageInfo
