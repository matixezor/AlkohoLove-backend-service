from pydantic import BaseModel

from src.domain.food import Food
from src.domain.taste import Taste
from src.domain.aroma import Aroma
from src.domain.finish import Finish
from src.domain.region import Region
from src.domain.barcode import Barcode
from src.domain.page_info import PageInfo
from src.domain.ingredient import Ingredient


class AlcoholBase(BaseModel):
    alcohol_id: int
    barcodes: list[Barcode]
    name: str
    kind: str
    type: str
    alcohol_by_volume: float
    manufacturer: str
    rating: float | None
    image_name: str

    class Config:
        orm_mode = True


class Alcohol(AlcoholBase):
    description: str
    color: str | None
    serving_temperature: str | None
    region: Region
    foods: list[Food] = []
    aromas: list[Aroma] = []
    tastes: list[Taste] = []
    finishes: list[Finish] = []
    ingredients: list[Ingredient] = []
    bitterness_ibu: int | None
    srm: float | None
    extract: float | None
    fermentation: str | None
    is_filtered: bool | None
    is_pasteurized: bool | None
    age: int | None
    year: int | None
    vine_stock: str | None


class PaginatedAlcoholInfo(BaseModel):
    alcohols: list[Alcohol]
    page_info: PageInfo


class AlcoholCreate(BaseModel):
    barcode_list: list[str]
    name: str
    kind: str
    type: str
    alcohol_by_volume: float
    manufacturer: str
    alcohol_by_volume: float
    manufacturer: str
    description: str
    color: str | None = None
    serving_temperature: str | None = None
    region_id: int
    food_ids: list[int] = []
    aroma_ids: list[int] = []
    taste_ids: list[int] = []
    finish_ids: list[int] = []
    ingredient_ids: list[int] = []
    bitterness_ibu: int | None = None
    srm: float | None = None
    extract: float | None = None
    fermentation: str | None = None
    is_filtered: bool | None = None
    is_pasteurized: bool | None = None
    age: int | None = None
    year: int | None = None
    vine_stock: str | None = None
    image_name: str | None = None
