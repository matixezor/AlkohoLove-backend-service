from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.domain.page_info import PageInfo
from src.domain.user import User, UserUpdate
from src.database.database_config import get_db
from src.database.models.user import User as UserInDb
from src.database.models.alcohol import AlcoholDatabaseHandler
from src.database.models.user_tag import UserTagDatabaseHandler
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.utils.auth_utils import get_current_user, get_current_user_username
from src.domain.user_tag import UserTagCreate, PaginatedUserTag, UserTag, PaginatedUserTagAlcohols, UserTagUpdate


router = APIRouter(prefix='/me', tags=['me'])


def raise_user_tag_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User tag with given name already exists'
    )


def raise_item_not_found(item: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{item} not found'
    )


def raise_alcohol_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Alcohol already exists in given user tag'
    )


def raise_item_does_not_belong_to_user():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User tag does not belong to user'
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


@router.post(
    '/user_tags',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create user tag'
)
async def create_user_tag(
        payload: UserTagCreate,
        db: AsyncSession = Depends(get_db),
        current_user: UserInDb = Depends(get_current_user),
) -> None:
    if await UserTagDatabaseHandler.check_if_user_tag_exists(db, payload.tag_name, current_user.user_id):
        raise_user_tag_already_exists()
    await UserTagDatabaseHandler.create_user_tag(db, payload, current_user.user_id)


@router.get(
    path='/user_tags',
    response_model=PaginatedUserTag,
    status_code=status.HTTP_200_OK,
    summary='Read all your user tags',
)
async def get_user_tags(
        limit: int = 10,
        offset: int = 0,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTag:
    """
    Get all user tags with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    """
    user_tags = await UserTagDatabaseHandler.get_user_tags_by_user_id(db, limit, offset, current_user.user_id)
    total = await UserTagDatabaseHandler.count_user_tags(db, current_user.user_id)
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
    summary='Read your user tag alcohols'
)
async def get_user_tag_alcohols(
        tag_id: int,
        limit: int = 10,
        offset: int = 0,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> PaginatedUserTagAlcohols:
    """
    Get all alcohols from user tag with pagination. Query params:
    - **tag id**: int - required
    - **limit**: int - default 10
    - **offset**: int - default 0
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
        raise_item_does_not_belong_to_user()

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


@router.post(
    path='/user_tags/alcohols/{tag_id}',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your user tag'
)
async def add_alcohol_to_user_tag(
        tag_id: int,
        alcohol_id: int,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Add alcohol to user tag by tag id and alcohol id
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
        raise_item_does_not_belong_to_user()

    if not await AlcoholDatabaseHandler.check_if_alcohol_exists_by_id(db, alcohol_id):
        raise_item_not_found('Alcohol')

    if await UserTagDatabaseHandler.check_if_alcohol_exists_in_user_tag(db, tag_id, alcohol_id):
        raise_alcohol_already_exists()

    await UserTagDatabaseHandler.add_alcohol_to_user_tag(db, tag_id, alcohol_id)


@router.delete(
    path='/user_tags/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your user tag',
)
async def delete_user_tag(
        tag_id: int,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete user tag by tag id
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
        raise_item_does_not_belong_to_user()

    await UserTagDatabaseHandler.delete_user_tag(db, tag_id)


@router.delete(
    path='/user_tags/alcohol/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from your user tag'
)
async def delete_alcohol_from_user_tag(
        tag_id: int,
        alcohol_id: int,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol from user tag by tag id and alcohol id
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
        raise_item_does_not_belong_to_user()

    await UserTagDatabaseHandler.delete_alcohol_from_user_tag(db, tag_id, alcohol_id)


@router.put(
    path='/user_tags/{tag_id}',
    response_model=UserTag,
    status_code=status.HTTP_200_OK,
    summary='Update your user tag'
)
async def update_user_tag(
        tag_id: int,
        payload: UserTagUpdate,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> UserTag:
    """
    Update user tag name by tag id
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
        raise_item_not_found('User tag')

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
        raise_item_does_not_belong_to_user()

    if await UserTagDatabaseHandler.check_if_user_tag_exists(db, payload.tag_name, current_user.user_id):
        raise_user_tag_already_exists()

    return await UserTagDatabaseHandler.update_user_tag(db, tag_id, payload)
