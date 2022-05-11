from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.alcohol import AlcoholDatabaseHandler
from src.database.models.user_tag import UserTagDatabaseHandler as DatabaseHandler
from src.domain.user_tag import UserTagCreate, PaginatedUserTag, UserTag, PaginatedUserTagAlcohols, UserTagUpdate

router = APIRouter(prefix='/user_tags', tags=['user_tag'])


def raise_user_tag_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User tag with given name and user id already exists'
    )


def raise_item_not_found(reason: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{reason} not found'
    )


def raise_alcohol_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Alcohol already exists in user tag'
    )


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
    if await DatabaseHandler.check_if_user_tag_exists(db, payload.tag_name, payload.user_id):
        raise_user_tag_already_exists()
    try:
        await DatabaseHandler.create_user_tag(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')


@router.get(
    path='/{user_id}',
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
    Get all user tags of user with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **user id**: int - required
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
    path='/alcohols/{tag_id}',
    response_model=PaginatedUserTagAlcohols,
    status_code=status.HTTP_200_OK,
    summary='Read user tag alcohols'
)
async def get_user_tag_alcohols(
        limit: int = 10,
        offset: int = 0,
        tag_id: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTagAlcohols:
    """
    Get all alcohols from user tag with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **tag id**: int - required
    """
    if not await DatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    alcohols = await DatabaseHandler.get_user_tag_alcohols(db, limit, offset, tag_id)
    total = await DatabaseHandler.count_user_tag_alcohols(db, tag_id)

    return PaginatedUserTagAlcohols(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.put(
    path='/alcohols/{tag_id}',
    response_model=UserTag,
    status_code=status.HTTP_200_OK,
    summary='Add alcohol to user tag'
)
async def add_alcohol_to_user_tag(
        tag_id: int,
        alcohol_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Add alcohol to user tag by tag id and alcohol id
    """
    if not await DatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    if not await AlcoholDatabaseHandler.check_if_alcohol_exists_by_id(db, alcohol_id):
        raise_item_not_found('Alcohol')

    if await DatabaseHandler.check_if_alcohol_exists_in_user_tag(db, tag_id, alcohol_id):
        raise_alcohol_already_exists()

    await DatabaseHandler.add_alcohol_to_user_tag(db, tag_id, alcohol_id)


@router.delete(
    path='/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete user tag',
)
async def delete_user_tag(
        tag_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete user tag by id
    """
    await DatabaseHandler.delete_user_tag(db, tag_id)


@router.delete(
    path='/alcohol/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from user tag'
)
async def delete_alcohol_from_user_tag(
        tag_id: int,
        alcohol_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol from user tag by tag id
    """
    await DatabaseHandler.delete_alcohol_from_user_tag(db, tag_id, alcohol_id)


@router.put(
    path='/{tag_id}',
    response_model=UserTag,
    status_code=status.HTTP_200_OK,
    summary='Update user tag'
)
async def update_user_tag(
        tag_id: int,
        payload: UserTagUpdate,
        db: AsyncSession = Depends(get_db)
) -> UserTag:
    if not await DatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')
    return await DatabaseHandler.update_user_tag(db, tag_id, payload)
