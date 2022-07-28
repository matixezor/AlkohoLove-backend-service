import cloudinary
import cloudinary.uploader
from pymongo.database import Database
from fastapi import APIRouter, Depends, status, Response, UploadFile, File, HTTPException


from src.infrastructure.database.models.user import User
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.config.app_config import ApplicationSettings, get_settings
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholExistsException
from src.infrastructure.common.file_utils import image_size, get_suggestion_image_name
from src.domain.alcohol_suggestion.alcohol_suggestion_create import AlcoholSuggestionCreate
from src.infrastructure.exceptions.alcohol_suggestion_exception import SuggestionAlreadyMadeException
from src.infrastructure.database.models.alcohol_suggestion import AlcoholSuggestionDatabaseHandler as DatabaseHandler, \
    AlcoholSuggestionDatabaseHandler

router = APIRouter(prefix='/suggestions', tags=['alcohol_suggestions'])


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Add alcohol suggestion'
)
async def create_suggestion(
        payload: AlcoholSuggestionCreate = Depends(),
        file: UploadFile | None = File(default=None),
        current_user: User = Depends(get_valid_user),
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
):
    payload = payload.dict()
    if (
            await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, list(payload['barcode']))
    ):
        raise AlcoholExistsException()

    suggestion = await AlcoholSuggestionDatabaseHandler.get_suggestion_by_barcode(db.alcohol_suggestion,
                                                                                  payload['barcode'])

    if suggestion:
        if current_user['_id'] in suggestion['user_ids']:
            raise SuggestionAlreadyMadeException()
        else:
            await DatabaseHandler.append_to_suggestion(
                db.alcohol_suggestion, current_user['_id'], payload['description'], suggestion)
    else:
        suggestion = await DatabaseHandler.create_suggestion(
            db.alcohol_suggestion, current_user['_id'], payload
        )
    if file:
        if file.content_type not in ['image/png', 'image/jpeg']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only .png and .jpg files allowed')

        if image_size(file.file) > 9000000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='File size too large. Maximum is 9 mb'
            )
        image_name = get_suggestion_image_name(payload['name'], str(suggestion.inserted_id))

        try:
            cloudinary.uploader.upload(
                file.file,
                folder=settings.ALCOHOL_SUGGESTION_IMAGES_DIR,
                public_id=image_name,
                resource_type='image',
                overwrite=False,
                invalidate=True
            )
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
