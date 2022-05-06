from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.food import Food, PaginatedFood
from src.database.models.food import FoodDatabaseHandler as DatabaseHandler


router = APIRouter(prefix='/foods', tags=['[For admin] food'], dependencies=[Depends(is_admin)])


def raise_food_already_exists():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Food with given name already exists'
    )


@router.get(
    path='',
    response_model=PaginatedFood,
    status_code=status.HTTP_200_OK,
    summary='Search for foods',
)
async def get_foods(
        limit: int = 10,
        offset: int = 0,
        food_name: str = "",
        db: AsyncSession = Depends(get_db)
) -> PaginatedFood:
    """
    Search for foods with pagination
    Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **food_name**: str - default ''
    """
    foods = await DatabaseHandler.get_paginated_foods(db, food_name, limit, offset)
    total = await DatabaseHandler.count_foods(db, food_name)
    return PaginatedFood(
        foods=foods,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{food_id}',
    response_model=Food,
    status_code=status.HTTP_200_OK,
    summary='Search for foods'
)
async def get_food(
        food_id: int,
        db: AsyncSession = Depends(get_db)
) -> Food:
    """
    Get food by id
    """
    db_food = await DatabaseHandler.get_food_by_id(db, food_id)
    if not db_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Food not found'
        )
    return db_food


@router.post(
    path='',
    summary='Create food',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def create_food(
        food_name: str,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Create food with query param:
    - **food_name**: required
    """
    if await DatabaseHandler.check_if_food_exists(db, food_name):
        raise_food_already_exists()
    await DatabaseHandler.create_food(db, food_name)


@router.put(
    path='/{food_id}',
    response_model=Food,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Update food'
)
async def update_food(
        food_id: int,
        food_name: str,
        db: AsyncSession = Depends(get_db)
) -> Food:
    """
    Update food by id. Required query param:
    - **food_name**: str
    """
    if await DatabaseHandler.check_if_food_exists(db, food_name, food_id):
        raise_food_already_exists()
    return await DatabaseHandler.update_food(db, food_id, food_name)


@router.delete(
    path='/{food_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete food'
)
async def delete_food(
        food_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete food by id
    """
    await DatabaseHandler.delete_food(db, food_id)
