from src.domain.common.base_model import BaseModel


class AlcoholFiltersMetadata(BaseModel):
    filters: list[dict]
