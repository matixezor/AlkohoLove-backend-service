from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.user_tag import UserTagDatabaseHandler
from src.domain.user_tag import PaginatedUserTag, PaginatedUserTagAlcohols
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.domain.user import UserAdminUpdate, UserAdminInfo, PaginatedUserAdminInfo


router = APIRouter(prefix='/users', tags=['users'])


def raise_user_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


def raise_item_not_found(item: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{item} not found'
    )


@router.get(
    path='',
    response_model=PaginatedUserAdminInfo,
    status_code=status.HTTP_200_OK,
    summary='[For Admin] Read users',
    dependencies=[Depends(is_admin)]
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
    summary='[For Admin] Read user information',
    dependencies=[Depends(is_admin)]
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
    summary='[For Admin] Update user',
    response_model=UserAdminInfo,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)]
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
    path='/tags/{username}',
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
    user = await DatabaseHandler.get_user_by_username(db, username)
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
    path='/tags/{tag_id}/alcohols',
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
