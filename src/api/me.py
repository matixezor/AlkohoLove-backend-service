from datetime import datetime
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
from src.domain.user.paginated_user_info import PaginatedFollowUserInfo
from src.infrastructure.database.models.user_tag import UserTagDatabaseHandler
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.domain.user_list.paginated_search_history import PaginatedSearchHistory
from src.infrastructure.exceptions.list_exceptions import AlcoholAlreadyInListException
from src.infrastructure.exceptions.followers_exceptions import UserAlreadyInFollowingException
from src.infrastructure.database.models.user_list.wishlist_database_handler import UserWishlistHandler
from src.infrastructure.database.models.user_list.favourites_database_handler import UserFavouritesHandler
from src.infrastructure.database.models.followers.following_database_handler import FollowingDatabaseHandler
from src.infrastructure.database.models.followers.followers_database_handler import FollowersDatabaseHandler
from src.infrastructure.database.models.user_list.search_history_database_handler import SearchHistoryHandler
from src.infrastructure.database.models.user import User as UserDb, UserDatabaseHandler as DatabaseHandler, \
    UserDatabaseHandler
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
    path='/tags/{tag_id}',
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
    '/tags/{tag_id}/alcohol/{alcohol_id}',
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
    path='/tags/{tag_id}/alcohol/{alcohol_id}',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Remove alcohol from tag'
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
    path='/tags/{tag_id}',
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
    path='/tags/{tag_id}/alcohols',
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


@router.get(
    path='/wishlist',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user wishlist with pagination',
    response_model_by_alias=False
)
async def get_wishlist(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user wishlist with pagination
    """
    user_id = str(current_user['_id'])
    alcohols = await UserWishlistHandler.get_user_wishlist_by_user_id(
        limit, offset, db.user_wishlist, db.alcohols, user_id)
    total = await UserWishlistHandler.count_alcohols_in_wishlist(db.user_wishlist, db.alcohols, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/favourites',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user favourite alcohol list with pagination',
    response_model_by_alias=False
)
async def get_favourites(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user favourite alcohol list with pagination
    """
    user_id = str(current_user['_id'])
    alcohols = await UserFavouritesHandler.get_user_favourites_by_user_id(
        limit, offset, db.user_favourites, db.alcohols, user_id
    )
    total = await UserFavouritesHandler.count_alcohols_in_favourites(db.user_favourites, db.alcohols, user_id)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/search_history',
    response_model=PaginatedSearchHistory,
    status_code=status.HTTP_200_OK,
    summary='Read user search history list with pagination',
    response_model_by_alias=False
)
async def get_search_history(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedSearchHistory:
    """
    Show user search history alcohol list with pagination
    """
    user_id = str(current_user['_id'])
    alcohols_and_dates = await SearchHistoryHandler.get_user_search_history_user_id(
        limit, offset, db.user_search_history, db.alcohols, user_id
    )
    total = await SearchHistoryHandler.count_alcohols_in_search_history(db.user_search_history, db.alcohols, user_id)
    return PaginatedSearchHistory(
        alcohols_and_dates=alcohols_and_dates,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from wishlist'
)
async def delete_alcohol_form_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserWishlistHandler.delete_alcohol_from_wishlist(db.user_wishlist, user_id, alcohol_id)


@router.delete(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from favourites'
)
async def delete_alcohol_form_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserFavouritesHandler.delete_alcohol_from_favourites(db.user_favourites, user_id, alcohol_id)


@router.delete(
    path='/search_history/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from search history'
)
async def delete_alcohol_form_search_history(
        alcohol_id: str,
        date: datetime,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.delete_alcohol_from_search_history(db.user_search_history, user_id, alcohol_id, date)


@router.post(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your wishlist'
)
async def add_alcohol_to_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to your wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserWishlistHandler.check_if_alcohol_in_wishlist(db.user_wishlist, user_id, alcohol_id):
        await UserWishlistHandler.add_alcohol_to_wishlist(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your favourites'
)
async def add_alcohol_to_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserFavouritesHandler.check_if_alcohol_in_favourites(db.user_wishlist, user_id, alcohol_id):
        await UserFavouritesHandler.add_alcohol_to_favourites(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/search_history/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to search_history'
)
async def add_alcohol_to_search_history(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.add_alcohol_to_search_history(db.user_search_history, user_id, alcohol_id)


@router.get(
    path='/wishlist',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user wishlist with pagination',
    response_model_by_alias=False
)
async def get_wishlist(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user wishlist with pagination
    """
    user_id = str(current_user['_id'])
    alcohols = await UserWishlistHandler.get_user_wishlist_by_user_id(
        limit, offset, db.user_wishlist, db.alcohols, user_id
    )
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    path='/favourites',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Read user favourite alcohol list with pagination',
    response_model_by_alias=False
)
async def get_favourites(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedAlcohol:
    """
    Show user favourite alcohol list with pagination
    """
    user_id = str(current_user['_id'])
    alcohols = await UserFavouritesHandler.get_user_favourites_by_user_id(
        limit, offset, db.user_favourites, db.alcohols, user_id
    )
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.get(
    path='/search_history',
    response_model=PaginatedSearchHistory,
    status_code=status.HTTP_200_OK,
    summary='Read user search history list with pagination',
    response_model_by_alias=False
)
async def get_search_history(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedSearchHistory:
    """
    Show user search history alcohol list with pagination
    """
    user_id = str(current_user['_id'])
    alcohols = await SearchHistoryHandler.get_user_search_history_user_id(
        limit, offset, db.user_search_history, db.alcohols, user_id
    )
    return PaginatedSearchHistory(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(alcohols)
        )
    )


@router.delete(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from wishlist'
)
async def delete_alcohol_form_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserWishlistHandler.delete_alcohol_from_wishlist(db.user_wishlist, user_id, alcohol_id)


@router.delete(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from favourites'
)
async def delete_alcohol_form_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    await UserFavouritesHandler.delete_alcohol_from_favourites(db.user_favourites, user_id, alcohol_id)


@router.delete(
    path='/search_history/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol from search history'
)
async def delete_alcohol_form_favourites(
        alcohol_id: str,
        date: datetime,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol from search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.delete_alcohol_from_search_history(db.user_search_history, user_id, alcohol_id, date)


@router.post(
    path='/wishlist/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your wishlist'
)
async def add_alcohol_to_wishlist(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to your wishlist by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserWishlistHandler.check_if_alcohol_in_wishlist(db.user_wishlist, user_id, alcohol_id):
        await UserWishlistHandler.add_alcohol_to_wishlist(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/favourites/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to your favourites'
)
async def add_alcohol_to_favourites(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to favourites by alcohol id
    """
    user_id = str(current_user['_id'])
    if not await UserFavouritesHandler.check_if_alcohol_in_favourites(db.user_wishlist, user_id, alcohol_id):
        await UserFavouritesHandler.add_alcohol_to_favourites(db.user_wishlist, user_id, alcohol_id)
    else:
        raise AlcoholAlreadyInListException()


@router.post(
    path='/search_history/{alcohol_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol to search_history'
)
async def add_alcohol_to_search_history(
        alcohol_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add alcohol to search history by alcohol id
    """
    user_id = str(current_user['_id'])
    await SearchHistoryHandler.add_alcohol_to_search_history(db.user_search_history, user_id, alcohol_id)


@router.get(
    path='/followers',
    response_model=PaginatedFollowUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read user followers with pagination',
    response_model_by_alias=False
)
async def get_followers(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedFollowUserInfo:
    """
    Get user followers with pagination
    """
    user_id = str(current_user['_id'])
    users = await FollowersDatabaseHandler.get_followers_by_user_id(
        limit, offset, db.followers, db.users, user_id
    )
    return PaginatedFollowUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(users)
        )
    )


@router.get(
    path='/following',
    response_model=PaginatedFollowUserInfo,
    status_code=status.HTTP_200_OK,
    summary='Read following users with pagination',
    response_model_by_alias=False
)
async def get_following(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        current_user: UserDb = Depends(get_valid_user)
) -> PaginatedFollowUserInfo:
    """
    Get following users with pagination
    """
    user_id = str(current_user['_id'])
    users = await FollowingDatabaseHandler.get_following_by_user_id(limit, offset, db.following, db.users, user_id)
    return PaginatedFollowUserInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=len(users)
        )
    )


@router.delete(
    path='/following/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete user from following'
)
async def delete_user_from_following(
        user_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Delete user from following by following user id
    """
    current_user_id = str(current_user['_id'])
    if await UserDatabaseHandler.get_user_by_id(db.users, user_id):
        await FollowingDatabaseHandler.delete_user_from_following(db.following, current_user_id, user_id)
        await FollowersDatabaseHandler.delete_user_from_followers(db.followers, user_id, current_user_id)
    else:
        raise UserNotFoundException


@router.post(
    path='/following/{user_id}',
    status_code=status.HTTP_201_CREATED,
    summary='Add user to following'
)
async def add_user_to_following(
        user_id: str,
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db)
) -> None:
    """
    Add user to following by user id
    """
    current_user_id = str(current_user['_id'])
    if not await FollowingDatabaseHandler.check_if_user_in_following(db.following, current_user_id, user_id):
        await FollowingDatabaseHandler.add_user_to_following(db.following, current_user_id, user_id)
        await FollowersDatabaseHandler.add_user_to_followers(db.followers, user_id, current_user_id)
    else:
        raise UserAlreadyInFollowingException()
