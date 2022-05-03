from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, select
from fastapi import HTTPException, status

from src.database.database_metadata import Base
from src.domain.region import RegionCreate

class Region(Base):
    __tablename__ = 'region'

    region_id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String)
    country_id = Column(Integer, ForeignKey('country.country_id'))

    country = relationship('Country', backref=backref('region', uselist=False), lazy='joined')

class RegionDatabaseHandler:

    @staticmethod
    def raise_region_already_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Region already exists'
        )

    @staticmethod
    async def get_region_by_name(db: AsyncSession, region_name: str) -> Region | None:
        query = select(Region).filter(Region.region_name == region_name).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_regions(db: AsyncSession, regions: list[int]) -> list[Region]:
        query = select(Region).where(Region.region_id.in_(regions))
        db_regions = await db.execute(query)
        return db_regions.scalars().all()

    @staticmethod
    async def get_all_regions(db: AsyncSession) -> list[Region]:
        query = select(Region)
        db_regions = await db.execute(query)
        return db_regions.scalars().all()

    @staticmethod
    async def create_region(db: AsyncSession, region_create_payload: RegionCreate) -> Region:
        db_region = Region(
            **region_create_payload.dict(),
        )

        db.add(db_region)
        await db.commit()
        await db.refresh(db_region)

        return db_region

    @staticmethod
    async def check_if_region_exists(db: AsyncSession, region_name: str, ) -> None:
        if await RegionDatabaseHandler.get_region_by_name(db, region_name):
            RegionDatabaseHandler.raise_region_already_exists()
