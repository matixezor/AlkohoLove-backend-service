from PIL import Image
from os import remove
from os.path import exists
from pymongo.database import Database
from pymongo.errors import OperationFailure
from fastapi import APIRouter, Depends, status, HTTPException, Response, File, UploadFile, Form

from src.domain.common.page_info import PageInfo
from src.infrastructure.config.app_config import STATIC_DIR
from src.utils.validate_object_id import validate_object_id
from src.infrastructure.database.database_config import get_db
from src.infrastructure.auth.auth_utils import admin_permission
from src.domain.user import UserAdminInfo, PaginatedUserAdminInfo
from src.domain.alcohol import AlcoholCreate, Alcohol, AlcoholUpdate
from src.infrastructure.database.models.review import ReviewDatabaseHandler
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.domain.reported_errors import ReportedError, PaginatedReportedErrorInfo
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholExistsException
from src.domain.alcohol_category import AlcoholCategoryDelete, AlcoholCategoryCreate
from src.infrastructure.exceptions.validation_exceptions import ValidationErrorException
from src.infrastructure.database.models.reported_error import ReportedErrorDatabaseHandler
from src.infrastructure.database.models.alcohol_filter import AlcoholFilterDatabaseHandler
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler
from src.infrastructure.database.models.alcohol_category.mappers import map_to_alcohol_category
from src.infrastructure.exceptions.alcohol_categories_exceptions import AlcoholCategoryExistsException
from src.domain.alcohol_category import PaginatedAlcoholCategories, AlcoholCategory, AlcoholCategoryUpdate

router = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(admin_permission)])


@router.get(
    path='/users',
    response_model=PaginatedUserAdminInfo,
    status_code=status.HTTP_200_OK,
    summary='[For Admin] Read users',
    response_model_by_alias=False
)
async def search_users(
        limit: int = 10,
        offset: int = 0,
        username: str = '',
        db: Database = Depends(get_db)
):
    """
    Search for users with pagination by optional username
    """
    users = await UserDatabaseHandler.get_users(db.users, limit, offset, username)
    total = await UserDatabaseHandler.count_users(db.users, username)
    return PaginatedUserAdminInfo(
        users=users,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/users/{user_id}',
    response_model=UserAdminInfo,
    status_code=status.HTTP_200_OK,
    summary='[For Admin] Read user information',
    response_model_by_alias=False,
)
async def get_user(
        user_id: str,
        db: Database = Depends(get_db)
):
    """
    Read user information
    """
    user_id = validate_object_id(user_id)
    db_user = await UserDatabaseHandler.get_user_by_id(db.users, user_id)
    if not db_user:
        raise UserNotFoundException()
    return db_user


@router.put(
    path='/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For Admin] Ban or unban user',
)
async def ban_user(
        user_id: str,
        to_ban: bool = True,
        db: Database = Depends(get_db)
):
    """
    Ban user by id.
    *to_ban: bool = True* - query param that specifies if the user should be banned or unbanned
    """
    user_id = validate_object_id(user_id)
    if to_ban:
        await UserDatabaseHandler.ban_user(db.users, user_id)
    else:
        await UserDatabaseHandler.unban_user(db.users, user_id)


@router.get(
    path='/errors/{error_id}',
    response_model=ReportedError,
    status_code=status.HTTP_200_OK,
    summary='Read full reported error information',
    response_model_by_alias=False
)
async def get_error(error_id: str, db: Database = Depends(get_db)):
    """
    Read reported error by id
    """
    error_id = validate_object_id(error_id)
    db_reported_error = await ReportedErrorDatabaseHandler.get_reported_error_by_id(db.reported_errors, error_id)
    if not db_reported_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reported error not found')
    return db_reported_error


@router.get(
    path='/errors',
    response_model=PaginatedReportedErrorInfo,
    status_code=status.HTTP_200_OK,
    summary='Read full reported error information',
    response_model_by_alias=False
)
async def get_errors(
        limit: int = 10,
        offset: int = 0,
        user_id: str = None,
        db: Database = Depends(get_db)
) -> PaginatedReportedErrorInfo:
    """
    Search reported errors with pagination.
    You can specify user_id to fetch errors reported by given user
    """
    if user_id is not None:
        user_id = validate_object_id(user_id)
    reported_errors = await ReportedErrorDatabaseHandler.get_reported_errors(
        db.reported_errors, limit, offset, user_id
    )
    total = await ReportedErrorDatabaseHandler.count_reported_errors(db.reported_errors, user_id)
    return PaginatedReportedErrorInfo(
        reported_errors=reported_errors,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/errors/{error_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete reported error'
)
async def delete_error(
        error_id: str,
        db: Database = Depends(get_db)
) -> None:
    """
    Delete reported error by reported error id
    """
    error_id = validate_object_id(error_id)
    await ReportedErrorDatabaseHandler.delete_reported_error(db.reported_errors, error_id)


@router.delete(
    path='/alcohols/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol',
)
async def delete_alcohol(
        alcohol_id: str,
        db: Database = Depends(get_db)
) -> None:
    """
    Delete alcohol by id
    """
    alcohol_id = validate_object_id(alcohol_id)
    await AlcoholDatabaseHandler.delete_alcohol(db.alcohols, alcohol_id)


@router.put(
    path='/alcohols/{alcohol_id}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    summary='Update alcohol',
    response_model_by_alias=False
)
async def update_alcohol(
        alcohol_id: str,
        payload: AlcoholUpdate,
        db: Database = Depends(get_db)
):
    """
    Update alcohol by id
    """
    alcohol_id = validate_object_id(alcohol_id)
    if (
            payload.barcode
            and (alcohol := await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, payload.barcode))
    ):
        if not alcohol['_id'] == alcohol_id:
            raise AlcoholExistsException()
    if alcohol := await AlcoholDatabaseHandler.get_alcohol_by_name(db.alcohols, payload.name):
        if not alcohol['_id'] == alcohol_id:
            raise AlcoholExistsException()
    db_alcohol = await AlcoholDatabaseHandler.update_alcohol(db.alcohols, alcohol_id, payload)
    await AlcoholFilterDatabaseHandler.update_filters(
        db.alcohol_filters, db_alcohol['kind'], db_alcohol['type'], db_alcohol['country'], db_alcohol['color']
    )
    return db_alcohol


@router.post(
    path='/alcohols',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create alcohol'
)
async def create_alcohol(
        payload: AlcoholCreate,
        db: Database = Depends(get_db)
):
    """
    Create alcohol
    """
    if (
            await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, payload.barcode)
            or await AlcoholDatabaseHandler.get_alcohol_by_name(db.alcohols, payload.name)
    ):
        raise AlcoholExistsException()
    if not await AlcoholCategoryDatabaseHandler.check_if_category_exist(db.alcohol_categories, payload.kind):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Alcohol category does not exist. Create one first!'
        )

    await AlcoholDatabaseHandler.add_alcohol(db.alcohols, payload)
    await AlcoholFilterDatabaseHandler.update_filters(
        db.alcohol_filters, payload.kind, payload.type, payload.country, payload.color
    )


@router.get(
    path='/alcohols/metadata/categories',
    response_model=PaginatedAlcoholCategories,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol categories schema',
    response_model_by_alias=False
)
async def get_schemas(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
):
    alcohol_categories = [
        map_to_alcohol_category(db_alcohol_category) for db_alcohol_category in
        await AlcoholCategoryDatabaseHandler.get_categories(db.alcohol_categories, limit, offset)
    ]
    total = await AlcoholCategoryDatabaseHandler.count_categories(db.alcohol_categories)
    return PaginatedAlcoholCategories(
        categories=alcohol_categories,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.put(
    path='/alcohols/metadata/categories/{category_id}',
    response_model=AlcoholCategory,
    status_code=status.HTTP_200_OK,
    summary='Add alcohol traits',
    response_model_by_alias=False
)
async def add_category_traits(
        category_id: str,
        payload: AlcoholCategoryUpdate,
        db: Database = Depends(get_db)
):
    category_id = validate_object_id(category_id)
    db_category = await AlcoholCategoryDatabaseHandler.get_category_by_id(db.alcohol_categories, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    if any(_key in list(db_category['properties'].keys()) for _key in list(payload.properties.keys())):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Properties already exist'
        )
    try:
        updated_category = await AlcoholCategoryDatabaseHandler.update_category(
            db.alcohol_categories, db_category, payload
        )
        await AlcoholDatabaseHandler.update_validation(db)
        return map_to_alcohol_category(updated_category)
    except OperationFailure as ex:
        await AlcoholCategoryDatabaseHandler.revert(db.alcohol_categories, db_category)
        raise ValidationErrorException(ex.args[0])


@router.delete(
    path='/alcohols/metadata/categories/{category_id}',
    response_model=AlcoholCategory,
    status_code=status.HTTP_200_OK,
    summary='Remove alcohol traits',
    response_model_by_alias=False
)
async def remove_category_traits(
        category_id: str,
        payload: AlcoholCategoryDelete,
        db: Database = Depends(get_db)
):
    category_id = validate_object_id(category_id)
    db_category = await AlcoholCategoryDatabaseHandler.get_category_by_id(db.alcohol_categories, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    if any(_key not in list(db_category['properties'].keys()) for _key in payload.properties):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Properties do not exist'
        )
    try:
        updated_category = await AlcoholCategoryDatabaseHandler.remove_properties(
            db.alcohol_categories, db_category, payload
        )
        await AlcoholDatabaseHandler.update_validation(db)
        await AlcoholDatabaseHandler.remove_fields_for_kind(
            db.alcohols, updated_category['title'], payload.properties
        )
        return map_to_alcohol_category(updated_category)
    except OperationFailure as ex:
        await AlcoholCategoryDatabaseHandler.revert(db.alcohol_categories, db_category)
        raise ValidationErrorException(ex.args[0])


@router.post(
    path='/alcohols/metadata/categories',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol category',
    response_model_by_alias=False
)
async def add_category(
        payload: AlcoholCategoryCreate,
        db: Database = Depends(get_db)
):
    if await AlcoholCategoryDatabaseHandler.check_if_category_exist(db.alcohol_categories, payload.title):
        raise AlcoholCategoryExistsException()
    try:
        await AlcoholCategoryDatabaseHandler.add_category(db.alcohol_categories, payload)
        await AlcoholDatabaseHandler.update_validation(db)
    except OperationFailure as ex:
        await AlcoholCategoryDatabaseHandler.revert_by_removal(db.alcohol_categories, payload.title)
        raise ValidationErrorException(ex.args[0])


@router.post(
    '/static',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_permission)],
    summary='[For admin] Upload image'
)
async def upload_image(
        image_name: str = Form(...),
        file: UploadFile = File(...),
):
    """
    Upload file with:
    *image_name* - name for the image, it should contain `_sm` or `_md` to
    specify size if multiple variants are to be uploaded
    *file*: - image
    """
    if file.content_type != 'image/png':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only .png files allowed')

    image = Image.open(file.file)
    image.save(f'{STATIC_DIR}/{image_name}.png')


@router.delete(
    '/static',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete image',
    dependencies=[Depends(admin_permission)],
)
async def delete_image(image_name: str):
    """
    Delete image by name. It should contain `_sm` or `_md` if there are multiple variants
    """
    image_path = f'{STATIC_DIR}/{image_name}.png'
    if exists(image_path):
        remove(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')


@router.delete(
    path='/reviews/{review_id}/alcohol/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete review',
    dependencies=[Depends(admin_permission)],
)
async def delete_review(
        review_id: str,
        alcohol_id: str,
        db: Database = Depends(get_db)
) -> None:
    """
    Delete review by id
    """

    rating = await ReviewDatabaseHandler.get_rating(db.reviews, review_id)

    if await ReviewDatabaseHandler.delete_review(db.reviews, review_id):
        await ReviewDatabaseHandler.remove_rating_from_alcohol(db.alcohols, alcohol_id, rating)
