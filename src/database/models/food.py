from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select

from src.database.database_metadata import Base


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
    async def get_foods(db: AsyncSession, foods: list[int]) -> list[Food]:
        query = select(Food).where(Food.food_id.in_(foods))
        db_foods = await db.execute(query)
        return db_foods.scalars().all()
