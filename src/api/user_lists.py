from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users import get_user
from src.domain.user import UserAdminInfo
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.user_list import UserListHandler, UserSearchHistory
from src.domain.user_list import PaginatedUserList, PaginatedUserSearchHistory

router = APIRouter(prefix='/lists', tags=['lists'])


@router.get(
    '/{user_id}/favourites',
    summary='Read user favourite alcohols',
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
    Read user favourite alcohols with pagination
    """
    alcohols = await UserListHandler.get_user_favourites_by_user_id(user_id=user.user_id, db=db,
                                                                    limit=limit,
                                                                    offset=offset)
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
    alcohols = await UserListHandler.get_user_wishlist_by_user_id(user_id=user.user_id, db=db, limit=limit,
                                                                  offset=offset)
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
    summary='Read user search history',
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
