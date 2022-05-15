from pydantic import BaseModel, Field, root_validator

from src.domain.page_info import PageInfo


class BaseCountry(BaseModel):
    country_id: int = Field(alias='id')
    country_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BaseRegion(BaseModel):
    region_id: int = Field(alias='id')
    region_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Country(BaseCountry):
    regions: list[BaseRegion]


class Region(BaseRegion):
    country: BaseCountry


class PaginatedCountry(BaseModel):
    countries: list[Country]
    page_info: PageInfo


class PaginatedRegion(BaseModel):
    regions: list[Region]
    page_info: PageInfo


class RegionCreate(BaseModel):
    name: str
    country_id: int


class RegionUpdate(RegionCreate):
    name: str | None = Field(default=None, alias='region_name')
    country_id: int | None = None

    @root_validator(pre=True)
    def any_of(cls, values: dict):
        if not any(values.values()):
            raise ValueError('At least one value needs to be provided')
        return values

    class Config:
        allow_population_by_field_name = True
