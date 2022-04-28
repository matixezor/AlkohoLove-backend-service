from pydantic import BaseModel, Field

from src.domain.country import Country


class Region(BaseModel):
    region_id: int
    region_name: str = Field(alias='name')
    country: Country

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
