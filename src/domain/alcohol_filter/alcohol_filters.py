from pydantic import BaseModel


class AlcoholFilters(BaseModel):
    filters: list[dict]
