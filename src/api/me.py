from pymongo.database import Database
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.domain.common import PageInfo
from src.domain.user_tag import UserTag
from src.domain.user import User, UserUpdate
from src.domain.alcohol import PaginatedAlcohol
from src.domain.user_tag.user_tag_create import UserTagCreate
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.domain.user_tag.paginated_user_tag import PaginatedUserTags
from src.infrastructure.database.models.user_tag import UserTagDatabaseHandler
from src.infrastructure.database.models.user import User as UserDb, UserDatabaseHandler as DatabaseHandler
from src.infrastructure.exceptions.user_tag_exceptions import TagDoesNotBelongToUser, TagAlreadyExists, AlcoholIsInTag,\
    AlcoholDoesNotExist, TagNotFound

router = APIRouter(prefix='/me', tags=['me'])


@router.get(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Read information about your account',
    response_model_by_alias=False
)
async def get_self(current_user: UserDb = Depends(get_valid_user)):
    return current_user


@router.put(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update your account data'
)
async def update_self(
        update_payload: UserUpdate,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    await DatabaseHandler.check_if_user_exists(db.users, email=update_payload.email)

    if (
            (update_payload.password and not update_payload.new_password)
            or (not update_payload.password and update_payload.new_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Both passwords must be provided'
        )

    elif update_payload.password:
        password_verified = DatabaseHandler.verify_password(
            current_user['password_salt'] + update_payload.password,
            current_user['password']
        )
        if not password_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Old password is invalid'
            )

        update_payload.password = DatabaseHandler.get_password_hash(
            password=update_payload.new_password,
            salt=current_user['password_salt']
        )
        update_payload.new_password = None

    return await DatabaseHandler.update_user(
        db.users,
        current_user['_id'],
        update_payload
    )


@router.delete(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your account'
)
async def delete_self(
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    await DatabaseHandler.delete_user(db.users, current_user['_id'])


@router.get(
    path='/tags',
    response_model=PaginatedUserTags,
    status_code=status.HTTP_200_OK,
    summary='Read your tags',
    response_model_by_alias=False
)
async def get_tags(
        limit: int = 10,
        offset: int = 0,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> PaginatedUserTags:
    """
    Search your tags with pagination.
    """
    user_tags = await UserTagDatabaseHandler.get_user_tags(
        db.user_tags, limit, offset, str(current_user['_id'])
    )
    total = await UserTagDatabaseHandler.count_user_tags(db.user_tags, str(current_user['_id']))
    return PaginatedUserTags(
        user_tags=user_tags,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/tags',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your tag'
)
async def delete_tag(
        tag_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete your tag by tag id
    """
    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(
            db.user_tags,
            tag_id,
            str(current_user['_id'])):
        raise TagDoesNotBelongToUser()

    await UserTagDatabaseHandler.delete_user_tag(db.user_tags, tag_id)


@router.post(
    '/tags',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create a tag'
)
async def create_tag(
        user_tag_create_payload: UserTagCreate,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    if await UserTagDatabaseHandler.check_if_user_tag_exists(
            db.user_tags,
            user_tag_create_payload.tag_name,
            str(current_user['_id'])):
        raise TagAlreadyExists()

    await UserTagDatabaseHandler.create_user_tag(
        db.user_tags, str(current_user['_id']), user_tag_create_payload
    )


@router.post(
    '/tags/alcohol',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to tag'
)
async def add_alcohol(
        tag_id: str,
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    if not await UserTagDatabaseHandler.check_if_tag_exists_by_id(
            db.user_tags,
            tag_id,
    ):
        raise TagNotFound()

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(
            db.user_tags,
            tag_id,
            str(current_user['_id'])):
        raise TagDoesNotBelongToUser()

    if not await UserTagDatabaseHandler.check_if_alcohol_exists(
            db.alcohols,
            alcohol_id):
        raise AlcoholDoesNotExist()

    if await UserTagDatabaseHandler.check_if_alcohol_is_in_user_tag(
            db.user_tags,
            tag_id,
            alcohol_id):
        raise AlcoholIsInTag()

    await UserTagDatabaseHandler.add_alcohol(
        db.user_tags,
        tag_id,
        alcohol_id)


@router.delete(
    path='/tags/alcohol',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from tag'
)
async def remove_alcohol(
        tag_id: str,
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(
            db.user_tags,
            tag_id,
            str(current_user['_id'])):
        raise TagDoesNotBelongToUser()

    await UserTagDatabaseHandler.remove_alcohol(
        db.user_tags,
        tag_id,
        alcohol_id)


@router.put(
    path='/tags',
    response_model=UserTag,
    status_code=status.HTTP_200_OK,
    summary='Change your tag name'
)
async def update_tag(
        tag_id: str,
        tag_name: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    if not await UserTagDatabaseHandler.check_if_tag_exists_by_id(
            db.user_tags,
            tag_id,
    ):
        raise TagNotFound()

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(
            db.user_tags,
            tag_id,
            str(current_user['_id'])):
        raise TagDoesNotBelongToUser()

    if await UserTagDatabaseHandler.check_if_user_tag_exists(
            db.user_tags,
            tag_name,
            str(current_user['_id'])
    ):
        raise TagAlreadyExists()

    return await UserTagDatabaseHandler.update_tag(
        db.user_tags,
        tag_id,
        tag_name,
    )


@router.get(
    path='/tags/alcohols',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read your tag alcohols',
    response_model_by_alias=False
)
async def get_alcohols(
        tag_id: str,
        limit: int = 10,
        offset: int = 0,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> PaginatedAlcohol:
    if not await UserTagDatabaseHandler.check_if_tag_exists_by_id(
            db.user_tags,
            tag_id,
    ):
        raise TagNotFound()

    if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(
            db.user_tags,
            tag_id,
            str(current_user['_id'])):
        raise TagDoesNotBelongToUser()

    total = await UserTagDatabaseHandler.count_alcohols(
        tag_id,
        db.user_tags,
        db.alcohols,
    )

    alcohols = await UserTagDatabaseHandler.get_tag_alcohols(
        tag_id,
        limit,
        offset,
        db.user_tags,
        db.alcohols,
    )

    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
