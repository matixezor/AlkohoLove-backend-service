from src.domain.common import PageInfo
from src.domain.common.base_model import BaseModel
from src.domain.alcohol_category import AlcoholCategory


class PaginatedAlcoholCategories(BaseModel):
    categories: list[AlcoholCategory]
    page_info: PageInfo
