from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler
from src.database.models.user_tag import UserTagDatabaseHandler
from src.domain.user_tag import PaginatedUserTagAlcohols, PaginatedUserTag

router = APIRouter(prefix='/followers', tags=['followers'])


def raise_item_not_found(item: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{item} not found'
    )


@router.get(
    path='/user_tags',
    response_model=PaginatedUserTag,
    status_code=status.HTTP_200_OK,
    summary='Read all tags of user',
)
async def get_user_tags(
        username: str,
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTag:
    """
    Get all user tags of user with pagination. Query params:
    - **username**: str - required
    - **limit**: int - default 10
    - **offset**: int - default 0
    """
    user = await UserDatabaseHandler.get_user_by_username(db, username)
    if not user:
        raise_item_not_found('User')
    user_tags = await UserTagDatabaseHandler.get_user_tags_by_user_id(db, limit, offset, user.user_id)
    total = await UserTagDatabaseHandler.count_user_tags(db, user.user_id)
    return PaginatedUserTag(
        user_tags=user_tags,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/user_tags/alcohols/{tag_id}',
    response_model=PaginatedUserTagAlcohols,
    status_code=status.HTTP_200_OK,
    summary='Read user tag alcohols'
)
async def get_user_tag_alcohols(
        tag_id: int,
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTagAlcohols:
    """
    Get all alcohols from user tag with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **tag id**: int - required
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    alcohols = await UserTagDatabaseHandler.get_user_tag_alcohols(db, limit, offset, tag_id)
    total = await UserTagDatabaseHandler.count_user_tag_alcohols(db, tag_id)

    return PaginatedUserTagAlcohols(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
