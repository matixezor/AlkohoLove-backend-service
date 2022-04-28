from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select

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
    async def get_flavours(db: AsyncSession, flavour_ids: list[int]) -> list[Flavour]:
        query = select(Flavour).where(Flavour.flavour_id.in_(flavour_ids))
        db_flavours = await db.execute(query)
        return db_flavours.scalars().all()
