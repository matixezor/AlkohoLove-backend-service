from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select

from src.database.database_metadata import Base


class Ingredient(Base):
    __tablename__ = 'ingredient'

    ingredient_id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String)


class AlcoholIngredient(Base):
    __tablename__ = 'alcohol_ingredient'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'), primary_key=True)


class IngredientDatabaseHandler:
    @staticmethod
    async def get_ingredients(db: AsyncSession, ingredient_ids: list[int]) -> list[Ingredient]:
        query = select(Ingredient).where(Ingredient.ingredient_id.in_(ingredient_ids))
        db_flavours = await db.execute(query)
        return db_flavours.scalars().all()
