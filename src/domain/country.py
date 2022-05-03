from pydantic import BaseModel, Field


class Country(BaseModel):
    country_id: int
    country_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AllCountries(BaseModel):
    country: list[Country]


class CountryCreate(BaseModel):
    country_name: str

    class Config:
        orm_mode = True
