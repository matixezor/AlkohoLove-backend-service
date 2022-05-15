from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.database.models.region import RegionDatabaseHandler as DatabaseHandler
from src.domain.country_and_region import Region, PaginatedRegion, RegionCreate, RegionUpdate


router = APIRouter(prefix='/regions', tags=['[For admin] region'], dependencies=[Depends(is_admin)])


def raise_region_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Region with given name already exists'
    )


@router.get(
    path='',
    response_model=PaginatedRegion,
    status_code=status.HTTP_200_OK,
    summary='Search for regions',
)
async def get_regions(
        limit: int = 10,
        offset: int = 0,
        name: str = "",
        db: AsyncSession = Depends(get_db)
) -> PaginatedRegion:
    """
    Search for regions with pagination
    Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **name**: str - default ''
    """
    regions = await DatabaseHandler.get_paginated_regions(db, name, limit, offset)
    total = await DatabaseHandler.count_regions(db, name)
    return PaginatedRegion(
        regions=regions,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{region_id}',
    response_model=Region,
    status_code=status.HTTP_200_OK,
    summary='Search for regions'
)
async def get_region(
        region_id: int,
        db: AsyncSession = Depends(get_db)
) -> Region:
    """
    Get region by id
    """
    db_region = await DatabaseHandler.get_region_by_id(db, region_id)
    if not db_region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Region not found'
        )
    return db_region


@router.post(
    path='',
    summary='Create region',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def create_region(
        region_create_payload: RegionCreate,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Create region with body:
    - **name**: required str
    - **country_id**:  required int
    """
    if await DatabaseHandler.check_if_region_exists(db, region_create_payload.name):
        raise_region_already_exists()
    await DatabaseHandler.create_region(db, region_create_payload)


@router.put(
    path='/{region_id}',
    response_model=Region,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Update region'
)
async def update_region(
        region_id: int,
        region_update_payload: RegionUpdate,
        db: AsyncSession = Depends(get_db)
) -> Region:
    """
    Update region by id. Required body:
    - **name**: str
    - **country_id**:  int
    """
    if await DatabaseHandler\
            .check_if_region_exists(db, region_update_payload.name, region_id):
        raise_region_already_exists()
    return await DatabaseHandler.update_region(db, region_id, region_update_payload)


@router.delete(
    path='/{region_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete region'
)
async def delete_region(
        region_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete region by id
    """
    await DatabaseHandler.delete_region(db, region_id)
