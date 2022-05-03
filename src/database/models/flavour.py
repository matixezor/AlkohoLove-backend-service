from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select
from fastapi import HTTPException, status

from src.database.database_metadata import Base
from src.domain.flavour import FlavourCreate


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
    def raise_flavour_already_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'flavour already exists'
        )

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
    async def get_all_flavours(db: AsyncSession) -> list[Flavour]:
        query = select(Flavour)
        db_flavours = await db.execute(query)
        return db_flavours.scalars().all()

    @staticmethod
    async def create_flavour(db: AsyncSession, flavour_create_payload: FlavourCreate) -> Flavour:
        db_flavour = Flavour(
            **flavour_create_payload.dict(),
        )

        db.add(db_flavour)
        await db.commit()
        await db.refresh(db_flavour)

        return db_flavour

    @staticmethod
    async def check_if_flavour_exists(db: AsyncSession, flavour_name: str, ) -> None:
        if await FlavourDatabaseHandler.get_flavour_by_name(db, flavour_name):
            FlavourDatabaseHandler.raise_flavour_already_exists()
