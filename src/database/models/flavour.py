from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select, func, update, delete

from src.database.database_metadata import Base


class Flavour(Base):
    __tablename__ = 'flavour'

    flavour_id = Column(Integer, primary_key=True, index=True)
    flavour_name = Column(String)


class AlcoholAroma(Base):
    __tablename__ = 'alcohol_aroma'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    flavour_id = Column(Integer, ForeignKey('flavour.flavour_id'), primary_key=True)


class AlcoholTaste(Base):
    __tablename__ = 'alcohol_taste'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    flavour_id = Column(Integer, ForeignKey('flavour.flavour_id'), primary_key=True)


class AlcoholFinish(Base):
    __tablename__ = 'alcohol_finish'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    flavour_id = Column(Integer, ForeignKey('flavour.flavour_id'), primary_key=True)


class FlavourDatabaseHandler:
    @staticmethod
    async def get_flavour_by_id(db: AsyncSession, flavour_id: int) -> Flavour | None:
        return await db.get(Flavour, flavour_id)

    @staticmethod
    async def get_flavour_by_name(db: AsyncSession, flavour_name: str) -> Flavour | None:
        query = select(Flavour).filter(Flavour.flavour_name == flavour_name).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_flavours(db: AsyncSession, flavour_ids: list[int]) -> list[Flavour]:
        query = select(Flavour).where(Flavour.flavour_id.in_(flavour_ids))
        db_flavours = await db.execute(query)
        return db_flavours.scalars().all()

    @staticmethod
    async def get_paginated_flavours(
            db: AsyncSession,
            flavour_name: str,
            limit: int, offset: int
    ) -> list[Flavour]:
        query = select(Flavour).order_by(Flavour.flavour_id)\
            .where(Flavour.flavour_name.contains(flavour_name)).offset(offset).limit(limit)
        db_flavours = await db.execute(query)
        return db_flavours.scalars().all()

    @staticmethod
    async def count_flavours(db: AsyncSession, flavour_name: str) -> int:
        query = select(func.count()).select_from(
            select(Flavour).where(Flavour.flavour_name.contains(flavour_name)).subquery()
        )
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def create_flavour(db: AsyncSession, flavour_name: str) -> None:
        db_flavour = Flavour(flavour_name=flavour_name)
        db.add(db_flavour)

    @staticmethod
    async def update_flavour(db: AsyncSession, flavour_id: int, flavour_name: str) -> Flavour:
        query = update(Flavour)\
            .where(Flavour.flavour_id == flavour_id)\
            .values(flavour_name=flavour_name)

        await db.execute(query)
        await db.commit()

        return await FlavourDatabaseHandler.get_flavour_by_id(db, flavour_id)

    @staticmethod
    async def delete_flavour(db: AsyncSession, flavour_id: int) -> None:
        query = delete(Flavour).\
            where(Flavour.flavour_id == flavour_id)
        await db.execute(query)

    @staticmethod
    async def check_if_flavour_exists(
            db: AsyncSession,
            flavour_name: str,
            flavour_id: int | None = None
    ) -> bool:
        db_flavour = await FlavourDatabaseHandler.get_flavour_by_name(db, flavour_name)
        if db_flavour:
            return True if db_flavour.flavour_id != flavour_id else False
        else:
            return False
