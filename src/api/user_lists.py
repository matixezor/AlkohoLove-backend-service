from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from src.api.me import get_self
from src.api.users import get_user
from src.database.models.user_list import UserListHandler, UserWishlist, UserFavouriteAlcohol
from src.domain.user_favourite_alcohol import PaginatedUserFavouriteAlcohol
from src.domain.user_search_history import PaginatedUserSearchHistory
from src.domain.user_wishlist import PaginatedUserWishlist
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.user import UserAdminInfo

router = APIRouter(prefix='/lists', tags=['lists'])


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
) -> PaginatedUserFavouriteAlcohol:
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await UserListHandler.get_user_list_by_id(user_id=user.user_id, db=db,
                                                         limit=limit,
                                                         offset=offset, model=UserFavouriteAlcohol)
    return PaginatedUserFavouriteAlcohol(
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
    response_model=PaginatedUserWishlist,
    status_code=status.HTTP_200_OK
)
async def get_user_wishlist(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserWishlist:
    """
    Read user's wishlist with pagination
    """
    alcohols = await UserListHandler.get_user_list_by_id(user_id=user.user_id, db=db, limit=limit,
                                                         offset=offset, model=UserWishlist)
    return PaginatedUserWishlist(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )

@router.get(
    '/{user_id}/search_history',
    summary='Read User search history',
    response_model=PaginatedUserSearchHistory,
    status_code=status.HTTP_200_OK
)
async def get_user_search_history(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserSearchHistory:
    """
    Read user's search history with pagination
    """
    alcohols = await UserListHandler.get_user_search_history_by_id(user_id=user.user_id, db=db,
                                                                   limit=limit,
                                                                   offset=offset)
    return PaginatedUserSearchHistory(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


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
    alcohols = await UserListHandler.get_user_list(user=user, db=db, limit=limit, offset=offset, model=UserWishlist)
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
    alcohols = await UserListHandler.get_user_list(user=user, db=db, limit=limit,
                                                   offset=offset, model=UserFavouriteAlcohol)
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
    path='/wishlist',
    summary='Delete User wishlist',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_from_user_wishlist(
        alcohol_id: int,
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_from_user_list(user=current_user, alcohol_id=alcohol_id, db=db, model=UserWishlist)


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
    await UserListHandler.delete_from_user_list(user=current_user,
                                                alcohol_id=alcohol_id, db=db, model=UserFavouriteAlcohol)


@router.delete(
    path='/search_history',
    summary='Delete User search history',
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
    summary='Delete whole User search history',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_whole_search_history(
        current_user: UserAdminInfo = Depends(get_self),
        db: AsyncSession = Depends(get_db)
) -> None:
    await UserListHandler.delete_whole_user_search_history(user=current_user, db=db)
