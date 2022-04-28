from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.alcohol import PaginatedAlcoholInfo, Alcohol, AlcoholCreate
from src.database.models.alcohol import AlcoholDatabaseHandler as DatabaseHandler


router = APIRouter(prefix='/alcohol', tags=['alcohol'])


@router.get(
    path='',
    response_model=PaginatedAlcoholInfo,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Read full alcohol information',
    dependencies=[Depends(is_admin)]
)
async def get_alcohols(
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedAlcoholInfo:
    """
    Read alcohols with pagination
    """
    alcohols = await DatabaseHandler.get_alcohols(db, limit, offset)
    total = await DatabaseHandler.count_alcohols(db)
    return PaginatedAlcoholInfo(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol'
)
async def delete_self(
        alcohol_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol by alcohol_id
    """
    await DatabaseHandler.delete_alcohol(db, alcohol_id)


@router.get(
    path='/{barcode}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    summary='Read full alcohol information'
)
async def get_alcohol(
        barcode: str,
        db: AsyncSession = Depends(get_db)
) -> PaginatedAlcoholInfo:
    """
    Read alcohol by barcode
    """
    alcohol = await DatabaseHandler.get_alcohol(db, barcode)
    if not alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Alcohol not found'
        )
    return alcohol


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)],
    summary='Create alcohol'
)
async def create_alcohol(
        alcohol_create_payload: AlcoholCreate,
        db: AsyncSession = Depends(get_db)
) -> None:
    try:
        await DatabaseHandler.create_alcohol(db, alcohol_create_payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')
