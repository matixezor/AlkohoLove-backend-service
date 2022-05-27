from pymongo.database import Database
from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.alcohol import PaginatedAlcohol
from src.domain.common import PageInfo
from src.domain.user import User, UserUpdate
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user import User as UserDb, UserDatabaseHandler as DatabaseHandler
from src.infrastructure.database.models.user_list.favourites_database_handler import UserFavouritesHandler
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserWishlistHandler

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
    total = await UserWishlistHandler.count_alcohols_in_wishlist(db.user_wishlist, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
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
    total = await UserFavouritesHandler.count_alcohols_in_favourites(db.user_favourites, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


