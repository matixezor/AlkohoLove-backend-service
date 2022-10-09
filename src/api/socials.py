from starlette import status
from pymongo.database import Database
from fastapi import APIRouter, Depends, Query

from src.domain.common import PageInfo
from src.infrastructure.database.models.user import User
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.domain.user.paginated_user_info import PaginatedUserSocial
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.common.validate_object_id import validate_object_id
from src.infrastructure.database.models.socials.following_database_handler import FollowingDatabaseHandler
from src.infrastructure.database.models.socials.followers_database_handler import FollowersDatabaseHandler

router = APIRouter(prefix='/socials', tags=['socials'])


@router.get(
    path='/followers/{user_id}',
    response_model=PaginatedUserSocial,
    status_code=status.HTTP_200_OK,
    summary='Read user followers with pagination',
    response_model_by_alias=False
)
async def get_followers(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedUserSocial:
    """
    Get user followers with pagination
    """
    user_id = validate_object_id(user_id)
    users = await FollowersDatabaseHandler.get_followers_by_user_id(
        limit, offset, db.followers, db.users, user_id
    )
    total = await FollowersDatabaseHandler.count_followers(db.followers, db.users, user_id)
    return PaginatedUserSocial(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/following/{user_id}',
    response_model=PaginatedUserSocial,
    status_code=status.HTTP_200_OK,
    summary='Read following users with pagination',
    response_model_by_alias=False
)
async def get_following(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedUserSocial:
    """
    Get following users with pagination
    """
    user_id = validate_object_id(user_id)
    users = await FollowingDatabaseHandler.get_following_by_user_id(limit, offset, db.following, db.users, user_id)
    total = await FollowingDatabaseHandler.count_following(db.following, db.users, user_id)

    return PaginatedUserSocial(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/users',
    response_model=PaginatedUserSocial,
    status_code=status.HTTP_200_OK,
    summary='Search for users by phrase',
    response_model_by_alias=False,
)
async def search_users_by_phrase(
        limit: int = 10,
        offset: int = 0,
        phrase: str = Query(default=..., min_length=3),
        db: Database = Depends(get_db),
        current_user: User = Depends(get_valid_user),
):
    """
    Search for users with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default '', at least 3 characters
    """
    users = await UserDatabaseHandler.search_users_by_phrase(db.users, limit, offset, phrase, current_user)
    total = await UserDatabaseHandler.count_users_without_current(db.users, phrase, current_user)
    return PaginatedUserSocial(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
