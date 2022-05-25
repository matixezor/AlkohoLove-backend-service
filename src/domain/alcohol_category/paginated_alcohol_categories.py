from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.alcohol_category import AlcoholCategory


class PaginatedAlcoholCategories(BaseModel):
    categories: list[AlcoholCategory]
    page_info: PageInfo
