import cloudinary
import cloudinary.api
import cloudinary.uploader
from datetime import datetime
from pymongo.database import Database
from pymongo.errors import OperationFailure
from src.domain.review import ReportedReview
from src.domain.alcohol import PaginatedAlcohol
from src.domain.common.page_info import PageInfo
from src.domain.banned_review import BannedReview
from src.domain.alcohol_filter import AlcoholFilters
from src.domain.banned_review.review_ban import ReviewBan
from src.domain.alcohol_suggestion import AlcoholSuggestion
from src.infrastructure.common.file_utils import image_size
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.auth.auth_utils import admin_permission
from src.domain.user import UserAdminInfo, PaginatedUserAdminInfo
from src.infrastructure.database.models.user import User as UserDb
from src.domain.alcohol import AlcoholCreate, Alcohol, AlcoholUpdate
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.common.validate_object_id import validate_object_id
from src.infrastructure.database.models.review import ReviewDatabaseHandler
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.domain.review.paginated_reported_review import PaginatedReportedReview
from src.domain.reported_errors import ReportedError, PaginatedReportedErrorInfo
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.infrastructure.alcohol.alcohol_mappers import map_alcohols, map_alcohol
from src.domain.banned_review.paginated_banned_review import PaginatedBannedReview
from src.infrastructure.config.app_config import get_settings, ApplicationSettings
from src.infrastructure.exceptions.review_exceptions import ReviewNotFoundException
from src.domain.alcohol_category import AlcoholCategoryDelete, AlcoholCategoryCreate
from src.infrastructure.exceptions.validation_exceptions import ValidationErrorException
from src.infrastructure.database.models.reported_error import ReportedErrorDatabaseHandler
from src.infrastructure.database.models.alcohol_filter import AlcoholFilterDatabaseHandler
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler
from src.infrastructure.database.models.alcohol_category.mappers import map_to_alcohol_category
from src.domain.alcohol_suggestion.paginated_alcohol_suggestion import PaginatedAlcoholSuggestion
from src.infrastructure.exceptions.reported_error_exceptions import ReportedErrorNotFoundException
from src.infrastructure.exceptions.alcohol_suggestion_exception import SuggestionNotFoundException
from fastapi import APIRouter, Depends, status, HTTPException, Response, File, UploadFile, Body, Query
from src.domain.alcohol_category import AlcoholCategory, AlcoholCategoryUpdate, PaginatedAlcoholCategories
from src.infrastructure.exceptions.alcohol_categories_exceptions import AlcoholCategoryExistsException, \
    AlcoholCategoryNotFoundException, PropertiesAlreadyExistException, PropertiesNotExistException
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholExistsException, WrongFileTypeException, \
    FileTooBigException
from src.infrastructure.database.models.alcohol_suggestion.alcohol_suggestion_database_handler import \
    AlcoholSuggestionDatabaseHandler

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
    users = await UserDatabaseHandler.get_users(db.users, limit, offset, username, None)
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
    response_class=Response,
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
        raise ReportedErrorNotFoundException()
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
    response_class=Response,
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
    response_class=Response,
    summary='Delete alcohol',
)
async def delete_alcohol(
        alcohol_id: str,
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
) -> None:
    """
    Delete alcohol by id
    """
    alcohol_id = validate_object_id(alcohol_id)
    alcohol = await AlcoholDatabaseHandler.get_alcohol_by_id(db.alcohols, alcohol_id)
    await AlcoholDatabaseHandler.delete_alcohol(db.alcohols, alcohol_id)
    image_name = alcohol['_id']
    image_path = f'{settings.ALCOHOL_IMAGES_DIR}/{image_name}'
    cloudinary.uploader.destroy(f'{image_path}_md', invalidate=True)
    cloudinary.uploader.destroy(f'{image_path}_sm', invalidate=True)


@router.put(
    path='/alcohols/{alcohol_id}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    summary='Update alcohol',
    response_model_by_alias=False
)
async def update_alcohol(
        alcohol_id: str,
        payload: AlcoholUpdate = Body(...),
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings),
        sm: UploadFile | None = None,
        md: UploadFile | None = None
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
        db.alcohol_filters,
        db_alcohol['kind'],
        db_alcohol['type'],
        db_alcohol['country'],
        db_alcohol['color'],
        db_alcohol['food'],
        db_alcohol['taste'],
        db_alcohol['aroma']
    )

    if sm and md:
        if sm.content_type not in ['image/png', 'image/jpeg'] or md.content_type not in ['image/png', 'image/jpeg']:
            raise WrongFileTypeException()
        try:
            sm_name = f'{alcohol_id}_sm'
            md_name = f'{alcohol_id}_md'
            cloudinary.uploader.upload(
                sm.file,
                folder=settings.ALCOHOL_IMAGES_DIR,
                public_id=sm_name,
                resource_type='image',
                overwrite=True,
                invalidate=True
            )
            cloudinary.uploader.upload(
                md.file,
                folder=settings.ALCOHOL_IMAGES_DIR,
                public_id=md_name,
                resource_type='image',
                overwrite=True,
                invalidate=True
            )
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return map_alcohol(db_alcohol, db.alcohol_categories)


@router.post(
    path='/alcohols',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create alcohol'
)
async def create_alcohol(
        payload: AlcoholCreate = Body(...),
        current_user: UserDb = Depends(get_valid_user),
        db: Database = Depends(get_db),
        sm: UploadFile = File(...),
        md: UploadFile = File(...),
        settings: ApplicationSettings = Depends(get_settings)
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

    if sm.content_type not in ['image/png', 'image/jpeg'] or md.content_type not in ['image/png', 'image/jpeg']:
        await AlcoholDatabaseHandler.revert_by_removal(db.alcohols, payload.name)
        raise WrongFileTypeException()

    payload = AlcoholCreate(
        **payload.dict(),
        username=current_user["username"],
        date=datetime.now()
    )

    alcohol = await AlcoholDatabaseHandler.add_alcohol(db.alcohols, payload)
    if image_size(sm.file) > 1000000 and image_size(md.file) > 1000000:
        await AlcoholDatabaseHandler.revert_by_removal(db.alcohols, payload.name)
        raise FileTooBigException()

    try:
        sm_name = f'{alcohol.inserted_id}_sm'
        md_name = f'{alcohol.inserted_id}_md'
        cloudinary.uploader.upload(
            sm.file,
            folder=settings.ALCOHOL_IMAGES_DIR,
            public_id=sm_name,
            resource_type='image',
            overwrite=False,
            invalidate=True
        )
        cloudinary.uploader.upload(
            md.file,
            folder=settings.ALCOHOL_IMAGES_DIR,
            public_id=md_name,
            resource_type='image',
            overwrite=False,
            invalidate=True
        )
    except Exception as error:
        await AlcoholDatabaseHandler.revert_by_removal(db.alcohols, payload.name)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    await AlcoholFilterDatabaseHandler.update_filters(
        db.alcohol_filters,
        payload.kind,
        payload.type,
        payload.country,
        payload.color,
        payload.food,
        payload.taste,
        payload.aroma
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
        raise AlcoholCategoryNotFoundException()
    if any(_key in list(db_category['properties'].keys()) for _key in list(payload.properties.keys())):
        raise PropertiesAlreadyExistException()
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
        raise AlcoholCategoryNotFoundException()
    if any(_key not in list(db_category['properties'].keys()) for _key in payload.properties):
        raise PropertiesNotExistException()
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
        await AlcoholFilterDatabaseHandler.create_init_entry(db.alcohol_filters, payload.title)
    except OperationFailure as ex:
        await AlcoholCategoryDatabaseHandler.revert_by_removal(db.alcohol_categories, payload.title)
        raise ValidationErrorException(ex.args[0])


@router.get(
    path='/alcohols/metadata/categories/search',
    response_model=PaginatedAlcoholCategories,
    status_code=status.HTTP_200_OK,
    summary='Search alcohol categories by phrase',
    response_model_by_alias=False
)
async def search_alcohol_categories_by_phrase(
        limit: int = 10,
        offset: int = 0,
        phrase: str = Query(default='', min_length=3),
        db: Database = Depends(get_db),
) -> PaginatedAlcoholCategories:
    """
       Search for categories with pagination. Query params:
       - **limit**: int - default 10
       - **offset**: int - default 0
       - **phrase**: str - default '', at least 3 characters
    """
    alcohol_categories = [
        map_to_alcohol_category(db_alcohol_category) for db_alcohol_category in
        await AlcoholCategoryDatabaseHandler.search_categories_by_phrase(db.alcohol_categories, limit, offset, phrase)
    ]
    total = await AlcoholCategoryDatabaseHandler.count_categories_by_phrase(db.alcohol_categories, phrase)
    return PaginatedAlcoholCategories(
        categories=alcohol_categories,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.post(
    path='/alcohols/search',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Search for alcohols by phrase',
    response_model_by_alias=False,
)
async def search_alcohols(
        limit: int = 10,
        offset: int = 0,
        filters: AlcoholFilters | None = None,
        phrase: str | None = '',
        db: Database = Depends(get_db)
):
    """
    Search for alcohols with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default ''
    """
    alcohols, total = await AlcoholDatabaseHandler.search_alcohols(db.alcohols, limit, offset, phrase, filters)
    alcohols = map_alcohols(alcohols, db.alcohol_categories)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/suggestions',
    response_model=PaginatedAlcoholSuggestion,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol suggestions with pagination',
    response_model_by_alias=False
)
async def get_suggestions(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
):
    suggestions = await AlcoholSuggestionDatabaseHandler.get_suggestions(db.alcohol_suggestion, limit, offset)
    total = await AlcoholSuggestionDatabaseHandler.count_suggestions(db.alcohol_suggestion, '')
    return PaginatedAlcoholSuggestion(
        suggestions=suggestions,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/suggestions/total',
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary='Get total number of suggestions',
    response_model_by_alias=False
)
async def get_suggestions(
        db: Database = Depends(get_db)
) -> int:
    total = await AlcoholSuggestionDatabaseHandler.count_suggestions(db.alcohol_suggestion, '')
    return total


@router.get(
    path='/suggestions/search',
    response_model=PaginatedAlcoholSuggestion,
    status_code=status.HTTP_200_OK,
    summary='Search for alcohol suggestions by phrase',
    response_model_by_alias=False,
)
async def search_suggestions_by_phrase(
        limit: int = 10,
        offset: int = 0,
        phrase: str = Query(default='', min_length=3),
        db: Database = Depends(get_db)
):
    """
    Search for suggestions with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default '', at least 3 characters
    """
    suggestions = await AlcoholSuggestionDatabaseHandler.search_suggestions_by_phrase(
        db.alcohol_suggestion, limit, offset, phrase)
    total = await AlcoholSuggestionDatabaseHandler.count_suggestions(db.alcohol_suggestion, phrase)
    return PaginatedAlcoholSuggestion(
        suggestions=suggestions,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/suggestions/{suggestion_id}',
    response_model=AlcoholSuggestion,
    status_code=status.HTTP_200_OK,
    summary='Get alcohol suggestion by id',
    response_model_by_alias=False
)
async def get_suggestion_by_id(
        suggestion_id: str,
        db: Database = Depends(get_db)
) -> AlcoholSuggestion:
    suggestion_id = validate_object_id(suggestion_id)
    db_suggestions = await AlcoholSuggestionDatabaseHandler.get_suggestion_by_id(db.alcohol_suggestion,
                                                                                 suggestion_id)
    if not db_suggestions:
        raise SuggestionNotFoundException()
    return db_suggestions


@router.delete(
    path='/suggestions/{suggestion_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary='Delete alcohol suggestion'
)
async def delete_suggestion(
        suggestion_id: str,
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
) -> None:
    """
    Delete alcohol suggestion by suggestion id
    """
    suggestion_id = validate_object_id(suggestion_id)
    suggestion = await AlcoholSuggestionDatabaseHandler.get_suggestion_by_id(db.alcohol_suggestion, suggestion_id)
    await AlcoholSuggestionDatabaseHandler.delete_suggestion(db.alcohol_suggestion, suggestion_id)
    image_prefix = suggestion['barcode'] + '_'
    image_path = f'{settings.ALCOHOL_SUGGESTION_IMAGES_DIR}/{image_prefix}'
    cloudinary.api.delete_resources_by_prefix(prefix=f'{image_path}')


@router.delete(
    path='/reviews/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary='[For admin] Delete review',
    dependencies=[Depends(admin_permission)],
)
async def delete_review(
        review_id: str,
        db: Database = Depends(get_db)
) -> None:
    """
    Delete review by id
    """
    review_id = validate_object_id(review_id)
    review = await ReviewDatabaseHandler.get_review_by_id(db.reviews, review_id)
    alcohol_id = review['alcohol_id']

    if await ReviewDatabaseHandler.delete_review(db.reviews, review_id, alcohol_id):
        await ReviewDatabaseHandler.remove_rating_from_alcohol(db.alcohols, alcohol_id, review['rating'])
        await ReviewDatabaseHandler.remove_rating_from_user(db.users, review['user_id'], review['rating'])


@router.get(
    path='/reviews',
    response_model=PaginatedReportedReview,
    status_code=status.HTTP_200_OK,
    summary='Get reported reviews',
    response_model_by_alias=False
)
async def get_reported_reviews(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedReportedReview:
    db_reported_reviews = await ReviewDatabaseHandler.get_reported_reviews(db.reviews, limit, offset)
    total = await ReviewDatabaseHandler.count_reported_reviews(db.reviews)

    return PaginatedReportedReview(
        reviews=db_reported_reviews,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/reviews/search',
    response_model=PaginatedReportedReview,
    status_code=status.HTTP_200_OK,
    summary='Get reported reviews by phrase (username)',
    response_model_by_alias=False
)
async def get_reported_reviews_by_phrase(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db),
        phrase: str = Query(default='', min_length=3),
) -> PaginatedReportedReview:
    db_reported_reviews = await ReviewDatabaseHandler.get_reported_reviews_by_phrase(db.reviews, phrase, limit, offset)
    total = await ReviewDatabaseHandler.count_reported_reviews_by_phrase(db.reviews, phrase)

    return PaginatedReportedReview(
        reviews=db_reported_reviews,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/reviews/{review_id}',
    response_model=ReportedReview,
    status_code=status.HTTP_200_OK,
    summary='Get reported review by id',
    response_model_by_alias=False
)
async def get_reported_review(
        review_id: str,
        db: Database = Depends(get_db)
) -> ReportedReview:
    review_id = validate_object_id(review_id)
    db_reported_review = await ReviewDatabaseHandler.get_review_by_id(db.reviews, review_id)
    if db_reported_review:
        return db_reported_review
    else:
        raise ReviewNotFoundException()


@router.put(
    path='/reviews/{review_id}',
    response_model=BannedReview,
    status_code=status.HTTP_200_OK,
    summary='[For Admin] Ban review by id'
)
async def ban_review(
        review_id: str,
        reason_payload: ReviewBan,
        db: Database = Depends(get_db)
):
    review_id = validate_object_id(review_id)
    db_review = await ReviewDatabaseHandler.get_review_by_id(db.reviews, review_id)
    if db_review:
        db_banned_review = await ReviewDatabaseHandler.copy_review_to_banned_collection(
            db.reviews,
            db.banned_reviews,
            review_id,
            reason_payload.reason
        )
        if await ReviewDatabaseHandler.delete_review(db.reviews, review_id, db_review['alcohol_id']):
            await ReviewDatabaseHandler.remove_rating_from_alcohol(
                db.alcohols,
                db_review['alcohol_id'],
                db_review['rating']
            )
            await ReviewDatabaseHandler.remove_rating_from_user(db.users, db_review['user_id'], db_review['rating'])
    else:
        raise ReviewNotFoundException()
    return db_banned_review


@router.get(
    path='/reviews/ban/{user_id}',
    response_model=PaginatedBannedReview,
    status_code=status.HTTP_200_OK,
    summary='Read user banned reviews',
)
async def get_user_banned_reviews(
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedBannedReview:
    user_id = validate_object_id(user_id)
    if not await UserDatabaseHandler.check_if_user_exists(
            db.users,
            user_id=user_id,
    ):
        raise UserNotFoundException()

    reviews = await ReviewDatabaseHandler.get_user_banned_reviews(
        db.banned_reviews, limit, offset, user_id
    )
    print(reviews)
    total = await ReviewDatabaseHandler.count_user_banned_reviews(db.banned_reviews, user_id)
    return PaginatedBannedReview(
        reviews=reviews,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/alcohols/{username}',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Get alcohols created by user',
    response_model_by_alias=False
)
async def get_alcohols_created_by_user(
        username: str,
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedAlcohol:

    db_alcohols = await AlcoholDatabaseHandler.get_alcohols_created_by_user(db.alcohols, limit, offset, username)
    total = await AlcoholDatabaseHandler.count_alcohols_created_by_user(db.alcohols, username)

    return PaginatedAlcohol(
        alcohols=db_alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/alcohols/total/{username}',
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary='Get number of alcohols created by user',
    response_model_by_alias=False
)
async def get_alcohols_created_by_user(
        username: str,
        db: Database = Depends(get_db)
) -> int:
    return await AlcoholDatabaseHandler.count_alcohols_created_by_user(db.alcohols, username)
