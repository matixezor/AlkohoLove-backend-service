from starlette import status
from pymongo.database import Database
from fastapi import APIRouter, Depends, Body

from src.domain.common import PageInfo
from src.domain.alcohol import PaginatedAlcohol
from src.domain.user_list import SearchHistoryEntry
from src.domain.user_list import PaginatedSearchHistory
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.common.validate_object_id import validate_object_id
from src.infrastructure.alcohol.alcohol_mappers import map_alcohols, map_alcohol
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
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
    user_id = validate_object_id(user_id)
    if not await UserDatabaseHandler.check_if_user_exists(db.users, user_id=user_id):
        raise UserNotFoundException()
    alcohols = await UserWishlistHandler.get_user_wishlist_by_user_id(
        limit, offset, db.user_wishlist, db.alcohols, user_id
    )
    alcohols = map_alcohols(alcohols, db.alcohol_categories)
    total = await UserWishlistHandler.count_alcohols_in_wishlist(db.user_wishlist, db.alcohols, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
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
    user_id = validate_object_id(user_id)
    if not await UserDatabaseHandler.check_if_user_exists(db.users, user_id=user_id):
        raise UserNotFoundException()
    alcohols = await UserFavouritesHandler.get_user_favourites_by_user_id(
        limit, offset, db.user_favourites, db.alcohols, user_id
    )
    alcohols = map_alcohols(alcohols, db.alcohol_categories)
    total = await UserFavouritesHandler.count_alcohols_in_favourites(db.user_favourites, db.alcohols, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
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
    user_id = validate_object_id(user_id)
    if not await UserDatabaseHandler.check_if_user_exists(db.users, user_id=user_id):
        raise UserNotFoundException()
    alcohols_and_dates = await SearchHistoryHandler.get_user_search_history_user_id(
        limit, offset, db.user_search_history, db.alcohols, user_id
    )
    alcohols_and_dates = [
        SearchHistoryEntry(
            alcohol=map_alcohol(alcohol_and_date.alcohol.dict(), db.alcohol_categories),
            date=alcohol_and_date.date
        ) for alcohol_and_date in alcohols_and_dates
    ]
    total = await SearchHistoryHandler.count_alcohols_in_search_history(db.user_search_history, db.alcohols, user_id)
    return PaginatedSearchHistory(
        alcohols=alcohols_and_dates,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.post(
    path='/guest',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read guest alcohol list with pagination',
    response_model_by_alias=False
)
async def get_guest_list(
        limit: int = 10,
        offset: int = 0,
        alcohol_list: list[str] = Body(...),
        db: Database = Depends(get_db),
) -> PaginatedAlcohol:
    """
    Show guest alcohol list with pagination
    """
    alcohol_list = [validate_object_id(alcohol_id) for alcohol_id in alcohol_list]

    alcohols = await AlcoholDatabaseHandler.get_guest_list(
        db.alcohols, limit, offset, alcohol_list
    )
    alcohols = map_alcohols(alcohols, db.alcohol_categories)
    total = len(alcohol_list)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
