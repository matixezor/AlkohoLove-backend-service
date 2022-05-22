from pymongo.database import Database
from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.user import User, UserUpdate
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user import User as UserDb, UserDatabaseHandler as DatabaseHandler


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
        current_user['_id'],
        update_payload,
        db.users
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
    await DatabaseHandler.delete_user(current_user['_id'], db.users)


# @router.post(
#     '/tags',
#     response_class=Response,
#     status_code=status.HTTP_201_CREATED,
#     summary='Create user tag'
# )
# async def create_user_tag(
#         payload: UserTagCreate,
#         db: AsyncSession = Depends(get_db),
#         current_user: UserInDb = Depends(get_valid_user),
# ) -> None:
#     if await UserTagDatabaseHandler.check_if_user_tag_exists(db, payload.tag_name, current_user.user_id):
#         raise_user_tag_already_exists()
#     await UserTagDatabaseHandler.create_user_tag(db, payload, current_user.user_id)
#
#
# @router.get(
#     path='/tags',
#     response_model=PaginatedUserTag,
#     status_code=status.HTTP_200_OK,
#     summary='Read all your user tags',
# )
# async def get_user_tags(
#         limit: int = 10,
#         offset: int = 0,
#         current_user: UserInDb = Depends(get_valid_user),
#         db: AsyncSession = Depends(get_db)
# ) -> PaginatedUserTag:
#     """
#     Get all user tags with pagination. Query params:
#     - **limit**: int - default 10
#     - **offset**: int - default 0
#     """
#     user_tags = await UserTagDatabaseHandler.get_user_tags_by_user_id(db, limit, offset, current_user.user_id)
#     total = await UserTagDatabaseHandler.count_user_tags(db, current_user.user_id)
#     return PaginatedUserTag(
#         user_tags=user_tags,
#         page_info=PageInfo(
#             limit=limit,
#             offset=offset,
#             total=total
#         )
#     )
#
#
# @router.get(
#     path='/tags/{tag_id}',
#     response_model=PaginatedUserTagAlcohols,
#     status_code=status.HTTP_200_OK,
#     summary='Read your user tag alcohols'
# )
# async def get_user_tag_alcohols(
#         tag_id: int,
#         limit: int = 10,
#         offset: int = 0,
#         current_user: UserInDb = Depends(get_valid_user),
#         db: AsyncSession = Depends(get_db)
# ) -> PaginatedUserTagAlcohols:
#     """
#     Get all alcohols from user tag with pagination. Query params:
#     - **tag id**: int - required
#     - **limit**: int - default 10
#     - **offset**: int - default 0
#     """
#     if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
#         raise_item_not_found('User tag')
#
#     if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
#         raise_item_does_not_belong_to_user()
#
#     alcohols = await UserTagDatabaseHandler.get_user_tag_alcohols(db, limit, offset, tag_id)
#     total = await UserTagDatabaseHandler.count_user_tag_alcohols(db, tag_id)
#
#     return PaginatedUserTagAlcohols(
#         alcohols=alcohols,
#         page_info=PageInfo(
#             limit=limit,
#             offset=offset,
#             total=total
#         )
#     )
#
#
# @router.post(
#     path='/tags/{tag_id}',
#     response_class=Response,
#     status_code=status.HTTP_201_CREATED,
#     summary='Add alcohol to your user tag'
# )
# async def add_alcohol_to_user_tag(
#         tag_id: int,
#         alcohol_id: int,
#         current_user: UserInDb = Depends(get_valid_user),
#         db: AsyncSession = Depends(get_db)
# ) -> None:
#     """
#     Add alcohol to user tag by tag id and alcohol id
#     """
#     if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
#         raise_item_not_found('User tag')
#
#     if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
#         raise_item_does_not_belong_to_user()
#
#     if not await AlcoholDatabaseHandler.check_if_alcohol_exists_by_id(db, alcohol_id):
#         raise_item_not_found('Alcohol')
#
#     if await UserTagDatabaseHandler.check_if_alcohol_exists_in_user_tag(db, tag_id, alcohol_id):
#         raise_alcohol_already_exists()
#
#     await UserTagDatabaseHandler.add_alcohol_to_user_tag(db, tag_id, alcohol_id)
#
#
# @router.delete(
#     path='/tags/{tag_id}',
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary='Delete your user tag',
# )
# async def delete_user_tag(
#         tag_id: int,
#         current_user: UserInDb = Depends(get_valid_user),
#         db: AsyncSession = Depends(get_db)
# ) -> None:
#     """
#     Delete user tag by tag id
#     """
#     if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
#         raise_item_does_not_belong_to_user()
#
#     await UserTagDatabaseHandler.delete_user_tag(db, tag_id)
#
#
# @router.delete(
#     path='/tags/{tag_id}/alcohol',
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary='Delete alcohol from your user tag'
# )
# async def delete_alcohol_from_user_tag(
#         tag_id: int,
#         alcohol_id: int,
#         current_user: UserInDb = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db)
# ) -> None:
#     """
#     Delete alcohol from user tag by tag id and alcohol id
#     """
#     if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
#         raise_item_does_not_belong_to_user()
#
#     await UserTagDatabaseHandler.delete_alcohol_from_user_tag(db, tag_id, alcohol_id)
#
#
# @router.put(
#     path='/tags/{tag_id}',
#     response_model=UserTag,
#     status_code=status.HTTP_200_OK,
#     summary='Update your user tag'
# )
# async def update_user_tag(
#         tag_id: int,
#         tag_name: str,
#         current_user: UserInDb = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db)
# ) -> UserTag:
#     """
#     Update user tag name by tag id
#     """
#     if not await UserTagDatabaseHandler.check_if_user_tag_exists_by_id(db, tag_id):
#         raise_item_not_found('User tag')
#
#     if not await UserTagDatabaseHandler.check_if_user_tag_belongs_to_user(db, tag_id, current_user.user_id):
#         raise_item_does_not_belong_to_user()
#
#     if await UserTagDatabaseHandler.check_if_user_tag_exists(db, tag_name, current_user.user_id):
#         raise_user_tag_already_exists()
#
#     return await UserTagDatabaseHandler.update_user_tag(db, tag_id, tag_name)
