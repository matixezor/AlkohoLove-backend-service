from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.domain.page_info import PageInfo
from src.domain.user_tag import UserTagCreate, PaginatedUserTag, UserTagAlcohols, UserTag
from src.database.database_config import get_db
from src.database.models.user_tag import UserTagDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/user_tags', tags=['user_tags'])


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create user tag'
)
async def create_user_tag(
        payload: UserTagCreate,
        db: AsyncSession = Depends(get_db),
) -> None:
    await DatabaseHandler.check_if_user_tag_exists(
        db,
        payload.tag_name,
        payload.user_id
    )
    await DatabaseHandler.create_user_tag(db, payload)


@router.get(
    path='',
    response_model=PaginatedUserTag,
    status_code=status.HTTP_200_OK,
    summary='Read all tags of user',
)
async def get_user_tags(
        limit: int = 10,
        offset: int = 0,
        user_id: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTag:
    """
    Search for alcohols with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **flavour_name**: str - default ''
    """
    user_tags = await DatabaseHandler.get_user_tags_by_user_id(db, limit, offset, user_id)
    total = await DatabaseHandler.count_user_tags(db, user_id)
    return PaginatedUserTag(
        user_tags=user_tags,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{tag_id}',
    response_model=UserTagAlcohols,
    status_code=status.HTTP_200_OK,
    summary='Read user tag with alcohols'
)
async def get_user_tag_with_alcohols(
        tag_id: int,
        db: AsyncSession = Depends(get_db)
) -> UserTagAlcohols:
    """
    Read user tag with alcohols
    """
    user_tag = await DatabaseHandler.get_user_tag_with_alcohols(db, tag_id)
    if not user_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User tag not found'
        )
    return user_tag


@router.delete(
    path='/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete user tag',
)
async def delete_alcohol(
        tag_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol by id
    """
    await DatabaseHandler.delete_user_tag(db, tag_id)