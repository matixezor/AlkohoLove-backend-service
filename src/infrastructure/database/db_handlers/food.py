# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import Column, Integer, String, ForeignKey, select, func, delete, update
#
# from src.database.database_metadata import Base
#
#
# class Food(Base):
#     __tablename__ = 'food'
#
#     food_id = Column(Integer, primary_key=True, index=True)
#     food_name = Column(String)
#
#
# class AlcoholFood(Base):
#     __tablename__ = 'alcohol_food'
#
#     alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
#     food_id = Column(Integer, ForeignKey('food.food_id'), primary_key=True)
#
#
# class FoodDatabaseHandler:
#     @staticmethod
#     async def get_food_by_id(db: AsyncSession, food_id: int) -> Food | None:
#         return await db.get(Food, food_id)
#
#     @staticmethod
#     async def get_food_by_name(db: AsyncSession, food_name: str) -> Food | None:
#         query = select(Food).filter(Food.food_name == food_name).limit(1)
#         result = await db.execute(query)
#         return result.scalars().first()
#
#     @staticmethod
#     async def get_foods(db: AsyncSession, foods: list[int]) -> list[Food]:
#         query = select(Food).where(Food.food_id.in_(foods))
#         db_foods = await db.execute(query)
#         return db_foods.scalars().all()
#
#     @staticmethod
#     async def get_paginated_foods(
#             db: AsyncSession,
#             food_name: str,
#             limit: int,
#             offset: int
#     ) -> list[Food]:
#         query = select(Food).order_by(Food.food_id)\
#             .where(Food.food_name.contains(food_name)).offset(offset).limit(limit)
#         db_foods = await db.execute(query)
#         return db_foods.scalars().all()
#
#     @staticmethod
#     async def count_foods(db: AsyncSession, food_name: str) -> int:
#         query = select(func.count()).select_from(
#             select(Food).where(Food.food_name.contains(food_name)).subquery()
#         )
#         result = await db.execute(query)
#         return result.scalar_one()
#
#     @staticmethod
#     async def create_food(db: AsyncSession, food_name: str) -> None:
#         db_food = Food(food_name=food_name)
#         db.add(db_food)
#
#     @staticmethod
#     async def update_food(db: AsyncSession, food_id: int, food_name: str) -> Food:
#         query = update(Food)\
#             .where(Food.food_id == food_id)\
#             .values(food_name=food_name)
#
#         await db.execute(query)
#         await db.commit()
#
#         return await FoodDatabaseHandler.get_food_by_id(db, food_id)
#
#     @staticmethod
#     async def delete_food(db: AsyncSession, food_id: int) -> None:
#         query = delete(Food).\
#             where(Food.food_id == food_id)
#         await db.execute(query)
#
#     @staticmethod
#     async def check_if_food_exists(db: AsyncSession, food_name: str, food_id: int = None) -> bool:
#         db_food = await FoodDatabaseHandler.get_food_by_name(db, food_name)
#         if db_food:
#             return True if db_food.food_id != food_id else False
#         else:
#             return False
