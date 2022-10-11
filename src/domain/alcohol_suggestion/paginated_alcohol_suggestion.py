from src.domain.common import PageInfo
from src.domain.common.base_model import BaseModel
from src.domain.alcohol_suggestion.alcohol_suggestion import AlcoholSuggestion


class PaginatedAlcoholSuggestion(BaseModel):
    suggestions: list[AlcoholSuggestion]
    page_info: PageInfo
