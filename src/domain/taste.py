from pydantic import BaseModel, Field


class Taste(BaseModel):
    flavour_id: int
    flavour_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
