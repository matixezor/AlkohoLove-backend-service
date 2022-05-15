import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.database.models.user_list import UserListHandler, UserFavouriteAlcohol, UserWishlist
from src.domain.page_info import PageInfo
from src.domain.user import User, UserUpdate, UserAdminInfo
from src.database.database_config import get_db
from src.database.models.user import User as UserInDb
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.domain.user_list import PaginatedUserList, PaginatedUserSearchHistory, UserSearchHistory
from src.utils.auth_utils import get_current_user, get_current_user_username


router = APIRouter(prefix='/me', tags=['me'])


def raise_alcohol_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Alcohol already exists in list'
    )


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
    summary='Read your wishlist',
    response_model=PaginatedUserList,
    status_code=status.HTTP_200_OK
)
async def get_user_wishlist(
        user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserList:
    """
    Read your wishlist with pagination
    """
    alcohols = await UserListHandler.get_user_list(user=user, db=db, limit=limit, offset=offset, model=UserWishlist)
    return PaginatedUserList(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    '/favourites',
    summary='Read your favourite alcohols',
    response_model=PaginatedUserList,
    status_code=status.HTTP_200_OK
)
async def get_user_favourite_alcohols(
        user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserList:
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await UserListHandler.get_user_list(user=user, db=db, limit=limit,
                                                   offset=offset, model=UserFavouriteAlcohol)
    return PaginatedUserList(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    '/search_history',
    summary='Read your search history',
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
    alcohols = await UserListHandler.get_user_search_history(user=user, db=db, limit=limit,
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
    path='/wishlist/{alcohol_id}',
    summary='Delete entry from your wishlist',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_user_wishlist(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_from_user_list(user=current_user, alcohol_id=alcohol_id, db=db, model=UserWishlist)


@router.delete(
    path='/favourites/{alcohol_id}',
    summary='Delete entry from your favourites list',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_favourite_alcohol_list(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_from_user_list(user=current_user,
                                                alcohol_id=alcohol_id, db=db, model=UserFavouriteAlcohol)


@router.delete(
    path='/search_history/{alcohol_id}',
    summary='Delete entry from your search history',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_search_history(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_from_user_search_history(user=current_user, alcohol_id=alcohol_id, db=db)


@router.delete(
    path='/search_history/all',
    summary='Delete your whole search history',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_whole_search_history(
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_whole_user_search_history(user=current_user, db=db)


@router.post(
    path='/wishlist',
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    summary='Update your list'
)
async def create_wishlist_entry(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Update wishlist. Required query param:
    - **alcohol_id**: int
    """
    if await UserListHandler.check_if_alcohol_in_list(UserWishlist,db, alcohol_id, current_user.user_id):
        raise_alcohol_already_exists()
    await UserListHandler.create_list_entry(db, current_user.user_id, alcohol_id, UserWishlist)


@router.post(
    path='/favourites',
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    summary='Update your list'
)
async def create_favourites_entry(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Update wishlist. Required query param:
    - **alcohol_id**: int
    """
    if await UserListHandler.check_if_alcohol_in_list(UserFavouriteAlcohol,db, alcohol_id, current_user.user_id):
        raise_alcohol_already_exists()
    await UserListHandler.create_list_entry(db, current_user.user_id, alcohol_id, UserFavouriteAlcohol)


@router.post(
    path='/search_history',
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    summary='Add an entry to search history'
)
async def create_search_history_entry(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db),
) -> None:
    """
    Update wishlist. Required query param:
    - **alcohol_id**: int
    """
    await UserListHandler.create_search_history_entry(db, current_user.user_id, alcohol_id, datetime.datetime.today())