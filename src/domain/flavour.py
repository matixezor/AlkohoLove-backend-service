from pydantic import BaseModel, Field

from src.domain.page_info import PageInfo


class Flavour(BaseModel):
    flavour_id: int = Field(alias='id')
    flavour_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PaginatedFlavour(BaseModel):
    flavours: list[Flavour]
    page_info: PageInfo
