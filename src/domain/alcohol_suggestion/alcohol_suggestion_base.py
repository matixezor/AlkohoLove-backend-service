from src.domain.common.base_model import BaseModel


class AlcoholSuggestionBase(BaseModel):
    barcode: str
    kind: str
    name: str
