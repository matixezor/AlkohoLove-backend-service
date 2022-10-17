from pydantic import Extra

from src.domain.common.base_model import BaseModel


class AlcoholBase(BaseModel):
    name: str
    kind: str
    type: str
    alcohol_by_volume: float
    description: str
    color: str
    manufacturer: str
    country: str
    region: str | None
    food: list[str]
    finish: list[str]
    aroma: list[str]
    taste: list[str]
    barcode: list[str]
    keywords: list[str]

    class Config:
        extra = Extra.allow
