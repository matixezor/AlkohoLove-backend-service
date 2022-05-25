from pydantic import BaseModel

from src.domain.alcohol import AlcoholBase


class UserWishlist(BaseModel):
    alcohol: AlcoholBase
