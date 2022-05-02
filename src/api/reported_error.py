from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.domain.reported_error import PaginatedReportedErrorInfo, ReportedErrorBase
from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.reported_error import ReportedErrorDatabaseHandler as DatabaseHandler, ReportedError

router = APIRouter(prefix='/reported_error', tags=['reported_error'])


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
        reported_errors=[ReportedErrorBase.from_orm(reported_error) for reported_error in reported_errors],
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/{error_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete reported error'
)
async def delete_self(
        reported_error_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete reported error by reported error id
    """
    await DatabaseHandler.delete_reported_error(db, reported_error_id)

# @router.get(
#     path='/{user_id}',
#     response_model=ReportedError,
#     status_code=status.HTTP_200_OK,
#     summary='Read full reported error information'
# )
# async def get_reported_errors(
#         user_id: int,
#         limit: int = 10,
#         offset: int = 0,
#         db: AsyncSession = Depends(get_db)
# ) -> PaginatedReportedErrorInfo:
#     """
#     Read reported error by user id with pagination
#     """
#     reported_errors = await DatabaseHandler.get_reported_errors(db, limit, offset)
#     total = await DatabaseHandler.count_reported_errors(db)
#     return PaginatedReportedErrorInfo(
#         reported_errors=[ReportedError.from_orm(reported_error) for reported_error in reported_errors],
#         page_info=PageInfo(
#             limit=limit,
#             offset=offset,
#             total=total
#         )
#     )

# @router.get(
#     path='/{error_id}',
#     response_model=ReportedError,
#     status_code=status.HTTP_200_OK,
#     summary='Read full reported error information'
# )
# async def get_reported_error(
#         error_id: int,
#         db: AsyncSession = Depends(get_db)
# ) -> PaginatedReportedErrorInfo:
#     """
#     Read reported error by reported error id
#     """
#     reported_error = await DatabaseHandler.get_reported_error_by_id(db, error_id)
#     if not reported_error:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Reported error not found'
#         )
#     return reported_error


# @router.post(
#     '',
#     response_class=Response,
#     status_code=status.HTTP_201_CREATED,
#     dependencies=[Depends(is_admin)],
#     summary='Create reported error'
# )
# async def create_reported_error(
#         reported_error_create_payload: ReportedError,
#         db: AsyncSession = Depends(get_db)
# ) -> None:
#     try:
#         await DatabaseHandler.create_reported_error(db, reported_error_create_payload)
#     except IntegrityError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')
