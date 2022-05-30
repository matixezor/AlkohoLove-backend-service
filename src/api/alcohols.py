from pymongo.database import Database
from fastapi import APIRouter, status, HTTPException, Depends

from src.domain.common import PageInfo
from src.domain.alcohol import Alcohol, PaginatedAlcohol
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler

router = APIRouter(prefix='/alcohols', tags=['alcohol'])


@router.get(
    path='',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Search for alcohols by phrase',
    response_model_by_alias=False,
)
async def search_alcohols(
        limit: int = 10,
        offset: int = 0,
        phrase: str = None,
        db: Database = Depends(get_db)
):
    """
    Search for alcohols with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default ''
    """
    alcohols, total = await AlcoholDatabaseHandler.search_alcohols(db.alcohols, limit, offset, phrase)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{barcode}',
    response_model=Alcohol,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol information by barcode'
)
async def get_alcohol_by_barcode(barcode: str, db: Database = Depends(get_db)):
    """
    Read alcohol by barcode
    """
    db_alcohol = await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, [barcode])
    if not db_alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Alcohol not found'
        )
    return db_alcohol
