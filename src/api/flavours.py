from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.flavour import Flavour, PaginatedFlavour
from src.database.models.flavour import FlavourDatabaseHandler as DatabaseHandler


router = APIRouter(
    prefix='/flavours',
    tags=['[For admin] flavour'],
    dependencies=[Depends(is_admin)]
)


def raise_flavour_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Flavour with given name already exists'
    )


@router.get(
    path='',
    response_model=PaginatedFlavour,
    status_code=status.HTTP_200_OK,
    summary='Search for flavours',
)
async def get_flavours(
        limit: int = 10,
        offset: int = 0,
        flavour_name: str = "",
        db: AsyncSession = Depends(get_db)
) -> PaginatedFlavour:
    """
    Search for flavours with pagination
    Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **flavour_name**: str - default ''
    """
    flavours = await DatabaseHandler.get_paginated_flavours(db, flavour_name, limit, offset)
    total = await DatabaseHandler.count_flavours(db, flavour_name)
    return PaginatedFlavour(
        flavours=flavours,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{flavour_id}',
    response_model=Flavour,
    status_code=status.HTTP_200_OK,
    summary='Search for flavours'
)
async def get_flavour(
        flavour_id: int,
        db: AsyncSession = Depends(get_db)
) -> Flavour:
    """
    Get flavour by id
    """
    db_flavour = await DatabaseHandler.get_flavour_by_id(db, flavour_id)
    if not db_flavour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Flavour not found'
        )
    return db_flavour


@router.post(
    path='',
    summary='Create flavour',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def create_flavour(
        flavour_name: str,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Create flavour with query param:
    - **flavour_name**: required
    """
    if await DatabaseHandler.check_if_flavour_exists(db, flavour_name):
        raise_flavour_already_exists()
    await DatabaseHandler.create_flavour(db, flavour_name)


@router.put(
    path='/{flavour_id}',
    response_model=Flavour,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Update flavour'
)
async def update_flavour(
        flavour_id: int,
        flavour_name: str,
        db: AsyncSession = Depends(get_db)
) -> Flavour:
    """
    Update flavour by id. Required query param:
    - **flavour_name**: str
    """
    if await DatabaseHandler.check_if_flavour_exists(db, flavour_name, flavour_id):
        raise_flavour_already_exists()
    return await DatabaseHandler.update_flavour(db, flavour_id, flavour_name)


@router.delete(
    path='/{flavour_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete flavour'
)
async def delete_flavour(
        flavour_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete flavour by id
    """
    await DatabaseHandler.delete_flavour(db, flavour_id)
