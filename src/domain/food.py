from pydantic import BaseModel, Field


class Food(BaseModel):
    food_id: int
    food_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
