from datetime import datetime

from pymongo.database import Database
from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.alcohol import PaginatedAlcohol
from src.domain.common import PageInfo
from src.domain.user import User, UserUpdate
from src.domain.user_list.paginated_search_history import PaginatedSearchHistory
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user import User as UserDb, UserDatabaseHandler as DatabaseHandler
from src.infrastructure.database.models.user_list.favourites_database_handler import UserFavouritesHandler
from src.infrastructure.database.models.user_list.search_history_database_handler import SearchHistoryHandler
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserWishlistHandler
from src.infrastructure.exceptions.list_exceptions import AlcoholAlreadyInListException

router = APIRouter(prefix='/me', tags=['me'])


@router.get(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Read information about your account',
    response_model_by_alias=False
)
async def get_self(current_user: UserDb = Depends(get_valid_user)):
    return current_user


@router.put(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update your account data'
)
async def update_self(
        update_payload: UserUpdate,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    await DatabaseHandler.check_if_user_exists(db.users, email=update_payload.email)

    if (
            (update_payload.password and not update_payload.new_password)
            or (not update_payload.password and update_payload.new_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Both passwords must be provided'
        )

    elif update_payload.password:
        password_verified = DatabaseHandler.verify_password(
            current_user['password_salt'] + update_payload.password,
            current_user['password']
        )
        if not password_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Old password is invalid'
            )

        update_payload.password = DatabaseHandler.get_password_hash(
            password=update_payload.new_password,
            salt=current_user['password_salt']
        )
        update_payload.new_password = None

    return await DatabaseHandler.update_user(
        db.users,
        current_user['_id'],
        update_payload
    )


@router.delete(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your account'
)
async def delete_self(
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    await DatabaseHandler.delete_user(db.users, current_user['_id'])


@router.get(
    path='/wishlist',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user wishlist with pagination',
    response_model_by_alias=False
)
async def get_wishlist(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user wishlist with pagination
    """
    user_id = str(current_user['_id'])
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
    path='/favourites',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user favourite alcohol list with pagination',
    response_model_by_alias=False
)
async def get_favourites(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user favourite alcohol list with pagination
    """
    user_id = str(current_user['_id'])
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
    path='/search_history',
    response_model=PaginatedSearchHistory,
    status_code=status.HTTP_200_OK,
    summary='Read user search history list with pagination',
    response_model_by_alias=False
)
async def get_search_history(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedSearchHistory:
    """
    Show user search history alcohol list with pagination
    """
    user_id = str(current_user['_id'])
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


@router.delete(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from wishlist'
)
async def delete_alcohol_form_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserWishlistHandler.delete_alcohol_from_wishlist(db.user_wishlist, user_id, alcohol_id)


@router.delete(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from favourites'
)
async def delete_alcohol_form_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserFavouritesHandler.delete_alcohol_from_favourites(db.user_favourites, user_id, alcohol_id)


@router.delete(
    path='/search_history/{alcohol_id}/{date}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from search history'
)
async def delete_alcohol_form_favourites(
        alcohol_id: str,
        date: datetime,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.delete_alcohol_from_search_history(db.user_search_history, user_id, alcohol_id, date)


@router.post(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your wishlist'
)
async def add_alcohol_to_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to your wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserWishlistHandler.check_if_alcohol_in_wishlist(db.user_wishlist, user_id, alcohol_id):
        await UserWishlistHandler.add_alcohol_to_wishlist(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your favourites'
)
async def add_alcohol_to_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserFavouritesHandler.check_if_alcohol_in_favourites(db.user_wishlist, user_id, alcohol_id):
        await UserFavouritesHandler.add_alcohol_to_favourites(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/search_history/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to search_history'
)
async def add_alcohol_to_search_history(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.add_alcohol_to_search_history(db.user_search_history, user_id, alcohol_id)
