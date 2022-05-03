from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response, FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.food import Food, AllFood, FoodCreate
from src.database.models.food import FoodDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/food', tags=['food'])


@router.get(
    path='/{food}',
    response_model=AllFood,
    status_code=status.HTTP_200_OK,
    summary='Read all food',
    dependencies=[Depends(is_admin)]
)
async def get_food(
        db: AsyncSession = Depends(get_db)
) -> AllFood:

    food = await DatabaseHandler.get_all_foods(db)

    return AllFood(
        food=food,
    )

@router.post(
    path='',
    summary='Create food',
    response_model=Food,
    status_code=status.HTTP_201_CREATED
)
async def post_food(food_create_payload: FoodCreate, db: AsyncSession = Depends(get_db)) -> Food:
    """
    Create food with request body:
    - **food_name**: required
    """
    await DatabaseHandler.check_if_food_exists(
        db,
        food_create_payload.food_name
    )
    return await DatabaseHandler.create_food(db, food_create_payload)
