from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from src.api.users import get_user
from src.database.models.user_list import UserListHandler, UserWishlist, UserFavouriteAlcohol, UserSearchHistory
from src.domain.user_list import PaginatedUserList, PaginatedUserSearchHistory
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.user import UserAdminInfo


router = APIRouter(prefix='/lists', tags=['lists'])


@router.get(
    '/{user_id}/favourites',
    summary='Read User favourite alcohols',
    response_model=PaginatedUserList,
    status_code=status.HTTP_200_OK
)
async def get_user_favourite_alcohols(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserList:
    """
    Read your favourite alcohols with pagination
    """
    alcohols = await UserListHandler.get_user_list_by_id(user_id=user.user_id, db=db,
                                                         limit=limit,
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
    '/{user_id}/wishlist',
    summary='Read User wishlist',
    response_model=PaginatedUserList,
    status_code=status.HTTP_200_OK
)
async def get_user_wishlist(
        user: UserAdminInfo = Depends(get_user),
        db: AsyncSession = Depends(get_db),
        limit: int = 10,
        offset: int = 0
) -> PaginatedUserList:
    """
    Read user's wishlist with pagination
    """
    alcohols = await UserListHandler.get_user_list_by_id(user_id=user.user_id, db=db, limit=limit,
                                                         offset=offset, model=UserWishlist)
    return PaginatedUserList(
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

        alcohols=[UserSearchHistory.from_orm(alcohol) for alcohol in alcohols],
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )






