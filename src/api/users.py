from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.database.models.user_favourite_alcohol import UserFavouriteAlcoholDatabaseHandler
from src.database.models.user_wishlist import WishlistDatabaseHandler
from src.domain.user_favourite_alcohol import PaginatedUserFavouriteAlcohol
from src.domain.user_wishlist import PaginatedUserWishlist
from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.domain.user import UserAdminUpdate, UserAdminInfo, PaginatedUserAdminInfo


router = APIRouter(prefix='/users', tags=['[for admin] users'], dependencies=[Depends(is_admin)])


def raise_user_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get(
    path='',
    response_model=PaginatedUserAdminInfo,
    status_code=status.HTTP_200_OK,
    summary='Read users'
)
async def get_users(
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserAdminInfo:
    """
    Read users with pagination
    """
    users = await DatabaseHandler.get_users(db, limit, offset)
    total = await DatabaseHandler.count_users(db)
    return PaginatedUserAdminInfo(
        users=[UserAdminInfo.from_orm(user) for user in users],
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{user_id}',
    response_model=UserAdminInfo,
    status_code=status.HTTP_200_OK,
    summary='Read user information'
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserAdminInfo:
    """
    Read user information
    """
    db_user = await DatabaseHandler.get_user_by_id(db, user_id)
    if not db_user:
        raise_user_not_found()
    return db_user


@router.put(
    path='/{user_id}',
    summary='Update user',
    response_model=UserAdminInfo,
    status_code=status.HTTP_200_OK
)
async def update_user(
        user_id: int,
        user_update_payload: UserAdminUpdate,
        db: AsyncSession = Depends(get_db)
) -> UserAdminInfo:
    """
    Update user with request Body:
    - **email**: optional
    validated with regex `[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}`
    - **name**: optional
    - **password**: optional
     validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    - **is_banned**: optional
    """
    db_user = await DatabaseHandler.get_user_by_id(db, user_id)
    if not db_user:
        raise_user_not_found()
    if user_update_payload.password:
        user_update_payload.password = DatabaseHandler.get_password_hash(
            password=user_update_payload.password,
            salt=db_user.password_salt
        )
    return await DatabaseHandler.update_user_by_id(db, user_id, user_update_payload)


@router.get(
    '/{user_id}/favourites',
    summary='Read User favourite alcohols',
    response_model=PaginatedUserFavouriteAlcohol,
    status_code=status.HTTP_200_OK
)
async def get_user_favourite_alcohols(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
):
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await UserFavouriteAlcoholDatabaseHandler.get_user_favourite_alcohols_by_id(user_id=user.user_id, db=db, limit=limit,
                                                                                     offset=offset)
    return PaginatedUserWishlist(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )

@router.get(
    '/{user_id}/wishlist',
    summary='Read User wishlist',
    response_model=PaginatedUserFavouriteAlcohol,
    status_code=status.HTTP_200_OK
)
async def get_user_wishlist(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
):
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await WishlistDatabaseHandler.get_user_wishlist_by_id(user_id=user.user_id, db=db, limit=limit,
                                                                                     offset=offset)
    return PaginatedUserWishlist(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )
