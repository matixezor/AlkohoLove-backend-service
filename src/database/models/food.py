from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select
from fastapi import HTTPException, status

from src.database.database_metadata import Base
from src.domain.food import FoodCreate


class Food(Base):
    __tablename__ = 'food'

    food_id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)


class AlcoholFood(Base):
    __tablename__ = 'alcohol_food'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    food_id = Column(Integer, ForeignKey('food.food_id'), primary_key=True)


class FoodDatabaseHandler:

    @staticmethod
    def raise_food_already_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Food already exists'
        )

    @staticmethod
    async def get_food_by_name(db: AsyncSession, food_name: str) -> Food | None:
        query = select(Food).filter(Food.food_name == food_name).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_foods(db: AsyncSession, foods: list[int]) -> list[Food]:
        query = select(Food).where(Food.food_id.in_(foods))
        db_foods = await db.execute(query)
        return db_foods.scalars().all()

    @staticmethod
    async def get_all_foods(db: AsyncSession) -> list[Food]:
        query = select(Food)
        db_foods = await db.execute(query)
        return db_foods.scalars().all()

    @staticmethod
    async def create_food(db: AsyncSession, food_create_payload: FoodCreate) -> Food:
        db_food = Food(
            **food_create_payload.dict(),
        )

        db.add(db_food)
        await db.commit()
        await db.refresh(db_food)

        return db_food

    @staticmethod
    async def check_if_food_exists(db: AsyncSession, food_name: str, ) -> None:
        if await FoodDatabaseHandler.get_food_by_name(db, food_name):
            FoodDatabaseHandler.raise_food_already_exists()
