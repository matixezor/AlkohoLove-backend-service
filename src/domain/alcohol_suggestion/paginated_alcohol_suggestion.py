from pydantic import BaseModel

from src.domain.alcohol_suggestion.alcohol_suggestion import AlcoholSuggestion
from src.domain.common import PageInfo


class PaginatedAlcoholSuggestion(BaseModel):
    suggestions: list[AlcoholSuggestion]
    page_info: PageInfo
