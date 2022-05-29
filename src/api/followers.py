from starlette import status
from pymongo.database import Database
from fastapi import APIRouter, Depends

from src.domain.common import PageInfo
from src.domain.user.paginated_user_info import PaginatedUserInfo
from src.infrastructure.database.models.followers.following_database_handler import FollowingDatabaseHandler
from src.infrastructure.database.models.followers.followers_database_handler import FollowersDatabaseHandler
from src.infrastructure.database.database_config import get_db


router = APIRouter(prefix='/followers', tags=['followers'])


@router.get(
    path='/followers/{user_id}',
    response_model=PaginatedUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read user followers with pagination',
    response_model_by_alias=False
)
async def get_followers(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedUserInfo:
    """
    Get user followers with pagination
    """
    users = await FollowersDatabaseHandler.get_followers_by_user_id(
        limit, offset, db.followers, db.users, user_id
    )
    return PaginatedUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(users)
        )
    )


@router.get(
    path='/following/{user_id}',
    response_model=PaginatedUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read following users with pagination',
    response_model_by_alias=False
)
async def get_following(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedUserInfo:
    """
    Get following users with pagination
    """
    users = await FollowingDatabaseHandler.get_following_by_user_id(limit, offset, db.following, db.users, user_id)
    return PaginatedUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(users)
        )
    )