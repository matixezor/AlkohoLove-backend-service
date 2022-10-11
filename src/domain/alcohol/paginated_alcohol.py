from src.domain.common import PageInfo
from src.domain.alcohol import Alcohol
from src.domain.common.base_model import BaseModel


class PaginatedAlcohol(BaseModel):
    alcohols: list[Alcohol]
    page_info: PageInfo
