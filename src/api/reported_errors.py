from fastapi import APIRouter, Depends, status, Response

from src.infrastructure.database.models.user import User
from src.domain.reported_errors import ReportedErrorCreate
from src.infrastructure.auth.auth_utils import get_valid_user
from src.infrastructure.database.models.reported_error import ReportedErrorDatabaseHandler as DatabaseHandler


router = APIRouter(prefix='/reported_errors', tags=['reported_errors'])


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Report an error'
)
async def create_reported_error(
    reported_error_create_payload: ReportedErrorCreate,
    current_user: User = Depends(get_valid_user)
):
    await DatabaseHandler.create_reported_error(str(current_user['_id']), reported_error_create_payload)
