from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    ingredient_id: int
    ingredient_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
