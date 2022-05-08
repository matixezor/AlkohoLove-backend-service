from pydantic import BaseModel, Field


class Finish(BaseModel):
    flavour_id: int = Field(alias='id')
    flavour_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
