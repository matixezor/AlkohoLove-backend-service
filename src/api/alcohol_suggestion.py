from pymongo.database import Database
from fastapi import APIRouter, Depends, status, Response

from src.infrastructure.database.models.user import User
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholExistsException
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
        payload: AlcoholSuggestionCreate,
        current_user: User = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    if (
            await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, list(payload.barcode))
    ):
        raise AlcoholExistsException()

    suggestion = await AlcoholSuggestionDatabaseHandler.get_suggestion_by_barcode(db.alcohol_suggestion,
                                                                                  payload.barcode)

    if suggestion:
        if current_user['_id'] in suggestion['user_ids']:
            raise SuggestionAlreadyMadeException()
        else:
            await DatabaseHandler.append_to_suggestion(
                db.alcohol_suggestion, current_user['_id'], payload.descriptions[0], suggestion)
    else:
        await DatabaseHandler.create_suggestion(
            db.alcohol_suggestion, current_user['_id'], payload
        )
