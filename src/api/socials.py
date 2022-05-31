from starlette import status
from pymongo.database import Database
from fastapi import APIRouter, Depends

from src.domain.common import PageInfo
from src.infrastructure.database.database_config import get_db
from src.domain.user.paginated_user_info import PaginatedFollowUserInfo
from src.infrastructure.database.models.socials.following_database_handler import FollowingDatabaseHandler
from src.infrastructure.database.models.socials.followers_database_handler import FollowersDatabaseHandler

router = APIRouter(prefix='/socials', tags=['socials'])


@router.get(
    path='/followers/{user_id}',
    response_model=PaginatedFollowUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read user followers with pagination',
    response_model_by_alias=False
)
async def get_followers(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedFollowUserInfo:
    """
    Get user followers with pagination
    """
    users = await FollowersDatabaseHandler.get_followers_by_user_id(
        limit, offset, db.followers, db.users, user_id
    )
    total = await FollowersDatabaseHandler.count_followers(db.followers, db.users, user_id)
    return PaginatedFollowUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/following/{user_id}',
    response_model=PaginatedFollowUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read following users with pagination',
    response_model_by_alias=False
)
async def get_following(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db),
) -> PaginatedFollowUserInfo:
    """
    Get following users with pagination
    """
    users = await FollowingDatabaseHandler.get_following_by_user_id(limit, offset, db.following, db.users, user_id)
    total = await FollowingDatabaseHandler.count_following(db.following, db.users, user_id)

    return PaginatedFollowUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
