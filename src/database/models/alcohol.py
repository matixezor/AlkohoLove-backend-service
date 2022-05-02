from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy import Column, Integer, String, Float, delete, select, func, Boolean, ForeignKey


from src.domain.alcohol import AlcoholCreate
from src.database.database_metadata import Base
from src.database.models.barcode import Barcode
from src.database.models.food import FoodDatabaseHandler
from src.database.models.flavour import FlavourDatabaseHandler
from src.database.models.ingredient import IngredientDatabaseHandler


class Alcohol(Base):
    __tablename__ = 'alcohol'

    alcohol_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    rating = Column(Float)
    type = Column(String)
    description = Column(String)
    region_id = Column(Integer, ForeignKey('region.region_id'))
    alcohol_by_volume = Column(Float)
    color = Column(String)
    year = Column(Integer)
    age = Column(Integer)
    bitterness_ibu = Column(Integer)
    srm = Column(Float)
    extract = Column(Float)
    fermentation = Column(String)
    is_filtered = Column(Boolean)
    is_pasteurized = Column(Boolean)
    serving_temperature = Column(String)
    manufacturer = Column(String)
    vine_stock = Column(String)
    image_name = Column(String)

    barcodes = relationship('Barcode', backref='alcohol')
    region = relationship('Region', uselist=False)
    foods = relationship('Food', secondary='alcohol_food')
    aromas = relationship('Flavour', secondary='alcohol_aroma')
    tastes = relationship('Flavour', secondary='alcohol_taste')
    finishes = relationship('Flavour', secondary='alcohol_finish')
    ingredients = relationship('Ingredient', secondary='alcohol_ingredient')


class AlcoholDatabaseHandler:
    @staticmethod
    async def create_alcohol(db: AsyncSession, payload: AlcoholCreate) -> None:
        fields_to_exclude =\
            {'aroma_ids', 'taste_ids', 'finish_ids', 'food_ids', 'barcode_list', 'ingredient_ids'}
        db_alcohol = Alcohol(**payload.dict(exclude_none=True, exclude=fields_to_exclude))

        db_barcodes = [Barcode(barcode=barcode) for barcode in payload.barcode_list]
        db_alcohol.barcodes = db_barcodes

        if payload.aroma_ids:
            db_aromas = await FlavourDatabaseHandler.get_flavours(db, payload.aroma_ids)
            db_alcohol.aromas = db_aromas

        if payload.taste_ids:
            db_tastes = await FlavourDatabaseHandler.get_flavours(db, payload.taste_ids)
            db_alcohol.tastes = db_tastes

        if payload.finish_ids:
            db_finish = await FlavourDatabaseHandler.get_flavours(db, payload.finish_ids)
            db_alcohol.finishes = db_finish

        if payload.food_ids:
            db_foods = await FoodDatabaseHandler.get_foods(db, payload.food_ids)
            db_alcohol.foods = db_foods

        if payload.ingredient_ids:
            db_ingredients =\
                await IngredientDatabaseHandler.get_ingredients(db, payload.ingredient_ids)
            db_alcohol.ingredients = db_ingredients

        db.add(db_alcohol)

    @staticmethod
    async def get_alcohol(db: AsyncSession, barcode: str) -> Alcohol | None:
        query = select(Alcohol).\
            where(Alcohol.barcodes.any(barcode=barcode))\
            .options(
                selectinload(Alcohol.barcodes),
                selectinload(Alcohol.aromas),
                selectinload(Alcohol.foods),
                selectinload(Alcohol.tastes),
                selectinload(Alcohol.finishes),
                selectinload(Alcohol.region),
                selectinload(Alcohol.ingredients)
            )
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def get_alcohols(db: AsyncSession, limit: int, offset: int) -> list[Alcohol]:
        query = select(Alcohol).offset(offset).limit(limit)\
            .options(
                selectinload(Alcohol.barcodes),
                selectinload(Alcohol.aromas),
                selectinload(Alcohol.foods),
                selectinload(Alcohol.tastes),
                selectinload(Alcohol.finishes),
                selectinload(Alcohol.region),
                selectinload(Alcohol.ingredients)
            )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_alcohols(db: AsyncSession) -> int:
        query = select(func.count()).select_from(select(Alcohol).subquery())
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def delete_alcohol(db: AsyncSession, alcohol_id: int) -> None:
        query = delete(Alcohol).\
            where(Alcohol.alcohol_id == alcohol_id)
        await db.execute(query)
