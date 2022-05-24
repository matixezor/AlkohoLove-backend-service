from pymongo.database import Database
from fastapi import APIRouter, Depends, status, Response

from src.infrastructure.database.models.user import User
from src.domain.reported_errors import ReportedErrorCreate
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.reported_error import ReportedErrorDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/errors', tags=['errors'])


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Report an error'
)
async def create_error(
        reported_error_create_payload: ReportedErrorCreate,
        current_user: User = Depends(get_valid_user),
        db: Database = Depends(get_db)
):
    await DatabaseHandler.create_reported_error(
        db.reported_errors, str(current_user['_id']), reported_error_create_payload
    )
