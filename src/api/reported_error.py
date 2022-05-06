from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response
from src.domain.reported_error import PaginatedReportedErrorInfo, ReportedError
from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.reported_error import ReportedErrorDatabaseHandler as DatabaseHandler
from src.database.models.reported_error import ReportedErrorCreate
from src.utils.reported_error_utils import raise_reported_error_not_found

router = APIRouter(prefix='/reported_error', tags=['reported_error'])


@router.get(
    path='/{error_id}',
    response_model=ReportedError,
    status_code=status.HTTP_200_OK,
    summary='Read full reported error information'
)
async def get_reported_error(error_id: int, db: AsyncSession = Depends(get_db)) -> ReportedError:
    """
    Read reported error by reported error id
    """
    db_reported_error = await DatabaseHandler.get_reported_error_by_id(db, error_id)
    if not db_reported_error:
        raise_reported_error_not_found()
    return db_reported_error


@router.get(
    path='',
    response_model=PaginatedReportedErrorInfo,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Read full reported error information',
    dependencies=[Depends(is_admin)]
)
async def get_reported_errors(
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedReportedErrorInfo:
    """
    Read reported errors with pagination
    """
    reported_errors = await DatabaseHandler.get_reported_errors(db, limit, offset)
    total = await DatabaseHandler.count_reported_errors(db)
    return PaginatedReportedErrorInfo(
        reported_errors=reported_errors,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/{reported_error_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete reported error'
)
async def delete_reported_error_by_id(
        reported_error_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete reported error by reported error id
    """
    await DatabaseHandler.delete_reported_error(db, reported_error_id)


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    summary='Create reported error'
)
async def create_reported_error(
        reported_error_create_payload: ReportedErrorCreate,
        db: AsyncSession = Depends(get_db)
) -> None:
    try:
        await DatabaseHandler.create_reported_error(db, reported_error_create_payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')
