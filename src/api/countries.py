from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.country_and_region import Country, PaginatedCountry
from src.database.models.country import CountryDatabaseHandler as DatabaseHandler


router = APIRouter(
    prefix='/countries',
    tags=['[For admin] country'],
    dependencies=[Depends(is_admin)]
)


def raise_country_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Country with given name already exists'
    )


@router.get(
    path='',
    response_model=PaginatedCountry,
    status_code=status.HTTP_200_OK,
    summary='Search for countries',
)
async def get_countries(
        limit: int = 10,
        offset: int = 0,
        name: str = "",
        db: AsyncSession = Depends(get_db)
) -> PaginatedCountry:
    """
    Search for countries with pagination
    Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **name**: str - default ''
    """
    countries = await DatabaseHandler.get_paginated_countries(db, name, limit, offset)
    total = await DatabaseHandler.count_countries(db, name)
    return PaginatedCountry(
        countries=countries,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{country_id}',
    response_model=Country,
    status_code=status.HTTP_200_OK,
    summary='Search for countries'
)
async def get_country(
        country_id: int,
        db: AsyncSession = Depends(get_db)
) -> Country:
    """
    Get country by id
    """
    db_country = await DatabaseHandler.get_country_by_id(db, country_id)
    if not db_country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Country not found'
        )
    return db_country


@router.post(
    path='',
    summary='Create country',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def create_country(
        name: str,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Create country with query param:
    - **name**: required
    """
    if await DatabaseHandler.check_if_country_exists(db, name):
        raise_country_already_exists()
    await DatabaseHandler.create_country(db, name)


@router.put(
    path='/{country_id}',
    response_model=Country,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Update country'
)
async def update_country(
        country_id: int,
        name: str,
        db: AsyncSession = Depends(get_db)
) -> Country:
    """
    Update country by id with query param:
    - **name**: required
    """
    if await DatabaseHandler.check_if_country_exists(db, name, country_id):
        raise_country_already_exists()
    return await DatabaseHandler.update_country(db, country_id, name)


@router.delete(
    path='/{country_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete country'
)
async def delete_country(
        country_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete country by country_id
    """
    await DatabaseHandler.delete_country(db, country_id)
