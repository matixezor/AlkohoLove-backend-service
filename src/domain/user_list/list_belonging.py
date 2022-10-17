from src.domain.common.base_model import BaseModel


class ListsBelonging(BaseModel):
    is_in_favourites: bool
    is_in_wishlist: bool
    alcohol_tags: list[str]
