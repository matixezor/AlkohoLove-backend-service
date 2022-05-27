from fastapi import APIRouter, Depends
from pymongo.database import Database
from starlette import status

from src.domain.alcohol import PaginatedAlcohol
from src.domain.common import PageInfo
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserListHandler

router = APIRouter(prefix='/list', tags=['list'])


@router.get(
    path='/wishlist/{user_id}',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user wishlist with pagination',
    response_model_by_alias=False
)
async def get_wishlist(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db)
) -> PaginatedAlcohol:
    """
    Show user wishlist with pagination
    """
    alcohols = await UserListHandler.get_user_wishlist_by_user_id(
        limit, offset, db.user_wishlist, db.alcohols, user_id
    )
    total = await UserListHandler.count_alcohols_in_wishlist(db.user_wishlist, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
