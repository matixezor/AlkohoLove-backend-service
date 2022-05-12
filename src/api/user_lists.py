from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from src.api.users import get_user
from src.database.models.user_list import UserListHandler, UserWishlist, UserFavouriteAlcohol
from src.domain.user_favourite_alcohol import PaginatedUserFavouriteAlcohol
from src.domain.user_search_history import PaginatedUserSearchHistory
from src.domain.user_wishlist import PaginatedUserWishlist
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.user import UserAdminInfo

router = APIRouter(prefix='/user_lists', tags=['user_lists'])


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
