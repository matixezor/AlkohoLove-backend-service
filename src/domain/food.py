from pydantic import BaseModel, Field

from src.domain.page_info import PageInfo


class Food(BaseModel):
    food_id: int = Field(alias='id')
    food_name: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PaginatedFood(BaseModel):
    foods: list[Food]
    page_info: PageInfo
