from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.database.models.user_favourite_alcohol import UserFavouriteAlcoholDatabaseHandler
from src.database.models.user_search_history import UserSearchHistoryDatabaseHandler
from src.database.models.user_wishlist import WishlistDatabaseHandler
from src.domain.page_info import PageInfo
from src.domain.user import User, UserUpdate, UserAdminInfo
from src.database.database_config import get_db
from src.database.models.user import User as UserInDb
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.domain.user_favourite_alcohol import PaginatedUserFavouriteAlcohol
from src.domain.user_search_history import PaginatedUserSearchHistory
from src.domain.user_wishlist import PaginatedUserWishlist
from src.utils.auth_utils import get_current_user, get_current_user_username

router = APIRouter(prefix='/me', tags=['me'])


@router.get(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Read information about your account'
)
async def get_self(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.put(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update your account data'
)
async def update_self(
        update_payload: UserUpdate,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> User:
    if (update_payload.password and not update_payload.new_password) \
            or (not update_payload.password and update_payload.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Both passwords must be provided'
        )
    elif update_payload.password:
        password_verified = DatabaseHandler.verify_password(
            current_user.password_salt + update_payload.password,
            current_user.password
        )
        if not password_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Passwords do not match'
            )
        update_payload.password = DatabaseHandler.get_password_hash(
            password=update_payload.new_password,
            salt=current_user.password_salt
        )
        update_payload.new_password = None
    try:
        return await DatabaseHandler.update_user(
            db,
            current_user,
            update_payload
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Account with given email already exists'
        )


@router.delete(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your account'
)
async def delete_self(
        current_user: str = Depends(get_current_user_username),
        db: AsyncSession = Depends(get_db)
) -> None:
    await DatabaseHandler.delete_user(db, current_user)


@router.get(
    '/wishlist',
    summary='Read User wishlist',
    response_model=PaginatedUserWishlist,
    status_code=status.HTTP_200_OK
)
async def get_user_wishlist(
        user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserWishlist:
    """
    Read your wishlist with pagination
    """
    alcohols = await WishlistDatabaseHandler.get_user_wishlist(user=user, db=db, limit=limit, offset=offset)
    return PaginatedUserWishlist(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    '/favourites',
    summary='Read User favourite alcohols',
    response_model=PaginatedUserFavouriteAlcohol,
    status_code=status.HTTP_200_OK
)
async def get_user_favourite_alcohols(
        user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserFavouriteAlcohol:
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await UserFavouriteAlcoholDatabaseHandler.get_self_favourite_alcohols(user=user, db=db, limit=limit,
                                                                                     offset=offset)
    return PaginatedUserFavouriteAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    '/search_history',
    summary='Read User search history',
    response_model=PaginatedUserSearchHistory,
    status_code=status.HTTP_200_OK
)
async def get_user_search_history(
        user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserSearchHistory:
    """
    Read your search history with pagination
    """
    alcohols = await UserSearchHistoryDatabaseHandler.get_user_search_history(user=user, db=db, limit=limit,
                                                                              offset=offset)
    return PaginatedUserSearchHistory(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.delete(
    path='/wishlist',
    summary='Delete User wishlist',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_user_wishlist(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await WishlistDatabaseHandler.delete_from_user_wishlist(user=current_user, alcohol_id=alcohol_id, db=db)


@router.delete(
    path='/favourites',
    summary='Delete User favourites list',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_favourite_alcohol_list(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserFavouriteAlcoholDatabaseHandler.delete_from_user_favourite_alcohols(user=current_user,
                                                                                  alcohol_id=alcohol_id, db=db)
