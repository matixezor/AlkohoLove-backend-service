from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.alcohol import AlcoholDatabaseHandler as DatabaseHandler
from src.domain.alcohol import PaginatedAlcoholInfo, Alcohol, AlcoholCreate, AlcoholUpdate


router = APIRouter(prefix='/alcohols', tags=['alcohol'])


def raise_alcohol_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Alcohol with given name already exists'
    )


@router.get(
    path='/admin',
    response_model=PaginatedAlcoholInfo,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Read full alcohol information',
    dependencies=[Depends(is_admin)]
)
async def get_alcohols(
        limit: int = 10,
        offset: int = 0,
        name: str = "",
        db: AsyncSession = Depends(get_db)
) -> PaginatedAlcoholInfo:
    """
    Search for alcohols with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **flavour_name**: str - default ''
    """
    alcohols = await DatabaseHandler.get_alcohols(db, limit, offset, name)
    total = await DatabaseHandler.count_alcohols(db, name)
    return PaginatedAlcoholInfo(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/admin/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete alcohol',
    dependencies=[Depends(is_admin)]
)
async def delete_alcohol(
        alcohol_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol by id
    """
    await DatabaseHandler.delete_alcohol(db, alcohol_id)


@router.get(
    path='/{barcode}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    summary='Read full alcohol information'
)
async def get_alcohol_by_barcode(
        barcode: str,
        db: AsyncSession = Depends(get_db)
) -> Alcohol:
    """
    Read alcohol by barcode
    """
    alcohol = await DatabaseHandler.get_alcohol_by_barcode(db, barcode)
    if not alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Alcohol not found'
        )
    return alcohol


@router.post(
    '/admin',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)],
    summary='[For admin] Create alcohol'
)
async def create_alcohol(
        alcohol_create_payload: AlcoholCreate,
        db: AsyncSession = Depends(get_db),
) -> None:
    if await DatabaseHandler\
            .check_if_alcohol_exists(db, alcohol_create_payload.name):
        raise_alcohol_already_exists()
    try:
        await DatabaseHandler.create_alcohol(db, alcohol_create_payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')


@router.put(
    '/admin/{alcohol_id}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)],
    summary='[For admin] Update alcohol'
)
async def update_alcohol(
        alcohol_id: int,
        alcohol_update_payload: AlcoholUpdate,
        db: AsyncSession = Depends(get_db),
) -> Alcohol:
    if await DatabaseHandler\
            .check_if_alcohol_exists(db, alcohol_update_payload.name, alcohol_id):
        raise_alcohol_already_exists()
    try:
        return await DatabaseHandler.update_alcohol(db, alcohol_id, alcohol_update_payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')
