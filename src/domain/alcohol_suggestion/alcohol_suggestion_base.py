from pydantic import BaseModel


class AlcoholSuggestionBase(BaseModel):
    barcode: str
    kind: str
    name: str
    descriptions: list[str]
