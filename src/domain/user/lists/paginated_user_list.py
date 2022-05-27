from src.domain.alcohol import Alcohol, AlcoholBase
from src.domain.common import PageInfo


class PaginatedUserWishlist(AlcoholBase):
    alcohols: list[AlcoholBase]
    page_info: PageInfo
