from pydantic import BaseModel


class AlcoholFilters(BaseModel):
    kind: str
    type: list[str] | None
    color: list[str] | None
    country: list[str] | None
