from pydantic import BaseModel


class AlcoholFiltersMetadata(BaseModel):
    filters: list[dict]
