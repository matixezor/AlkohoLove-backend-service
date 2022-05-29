from starlette import status
from pymongo.database import Database
from fastapi import APIRouter, Depends

from src.domain.common import PageInfo
from src.domain.alcohol import PaginatedAlcohol
from src.domain.user_list import PaginatedSearchHistory
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserWishlistHandler
from src.infrastructure.database.models.user_list.favourites_database_handler import UserFavouritesHandler
from src.infrastructure.database.models.user_list.search_history_database_handler import SearchHistoryHandler


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
    alcohols = await UserWishlistHandler.get_user_wishlist_by_user_id(
        limit, offset, db.user_wishlist, db.alcohols, user_id
    )
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    path='/favourites/{user_id}',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user favourite alcohol list with pagination',
    response_model_by_alias=False
)
async def get_favourites(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedAlcohol:
    """
    Show user favourite alcohol list with pagination
    """
    alcohols = await UserFavouritesHandler.get_user_favourites_by_user_id(
        limit, offset, db.user_favourites, db.alcohols, user_id
    )
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    path='/search_history/{user_id}',
    response_model=PaginatedSearchHistory,
    status_code=status.HTTP_200_OK,
    summary='Read user search history list with pagination',
    response_model_by_alias=False
)
async def get_search_history(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db)
) -> PaginatedSearchHistory:
    """
    Show user search history alcohol list with pagination
    """
    alcohols = await SearchHistoryHandler.get_user_search_history_user_id(
        limit, offset, db.user_search_history, db.alcohols, user_id
    )
    return PaginatedSearchHistory(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )
