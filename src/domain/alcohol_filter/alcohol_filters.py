from src.domain.common.base_model import BaseModel


class AlcoholFilters(BaseModel):
    kind: str | None
    type: list[str] | None
    color: list[str] | None
    country: list[str] | None
