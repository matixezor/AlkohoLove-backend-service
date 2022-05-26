from fastapi import APIRouter, Depends
from pymongo.database import Database
from starlette import status

from src.domain.common import PageInfo
from src.domain.user.lists import PaginatedUserWishlist
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserListHandler

router = APIRouter(prefix='/list', tags=['list'])


@router.get(
    path='/wishlist/{user_id}',
    response_model=PaginatedUserWishlist,
    status_code=status.HTTP_200_OK,
    summary='Read user wishlist',
    response_model_by_alias=False
)
async def get_user_wishlist(
        user_id: str = None,
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedUserWishlist:
    """
    Read your wishlist with pagination
    """
    alcohols = await UserListHandler.get_user_wishlist_by_user_id(user_id=user_id, limit=limit, offset=offset,
                                                       collection=db.user_wishlist)
    return PaginatedUserWishlist(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )
