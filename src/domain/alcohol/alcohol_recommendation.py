from src.domain.alcohol import Alcohol
from src.domain.common.base_model import BaseModel


class AlcoholRecommendation(BaseModel):
    alcohols: list[Alcohol]
