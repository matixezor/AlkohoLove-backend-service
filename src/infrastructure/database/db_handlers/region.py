# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy import Column, Integer, String, ForeignKey, select, func, update, delete
#
# from src.database.database_metadata import Base
# from src.domain.country_and_region import RegionCreate, RegionUpdate
#
#
# class Region(Base):
#     __tablename__ = 'region'
#
#     region_id = Column(Integer, primary_key=True, index=True)
#     region_name = Column(String)
#     country_id = Column(Integer, ForeignKey('country.country_id'))
#
#     country = relationship('Country', backref=backref('regions', lazy='joined'), lazy='joined')
#
#
# class RegionDatabaseHandler:
#     @staticmethod
#     async def get_region_by_id(db: AsyncSession, region_id: int) -> Region | None:
#         return await db.get(Region, region_id)
#
#     @staticmethod
#     async def get_region_by_name(db: AsyncSession, region_name: str) -> Region | None:
#         query = select(Region).filter(Region.region_name == region_name).limit(1)
#         result = await db.execute(query)
#         return result.scalars().first()
#
#     @staticmethod
#     async def get_regions(db: AsyncSession, regions: list[int]) -> list[Region]:
#         query = select(Region).where(Region.region_id.in_(regions))
#         db_regions = await db.execute(query)
#         return db_regions.scalars().unique().all()
#
#     @staticmethod
#     async def get_paginated_regions(
#             db: AsyncSession,
#             region_name: str,
#             limit: int,
#             offset: int
#     ) -> list[Region]:
#         query = select(Region).order_by(Region.region_id)\
#             .where(Region.region_name.contains(region_name)).offset(offset).limit(limit)
#         db_regions = await db.execute(query)
#         return db_regions.scalars().unique().all()
#
#     @staticmethod
#     async def count_regions(db: AsyncSession, region_name: str) -> int:
#         query = select(func.count()).select_from(
#             select(Region).where(Region.region_name.contains(region_name)).subquery()
#         )
#         result = await db.execute(query)
#         return result.scalar_one()
#
#     @staticmethod
#     async def create_region(db: AsyncSession, payload: RegionCreate) -> None:
#         db_region = Region(region_name=payload.name, country_id=payload.country_id)
#         db.add(db_region)
#
#     @staticmethod
#     async def update_region(
#             db: AsyncSession,
#             region_id: int,
#             payload: RegionUpdate
#     ) -> Region:
#         query = update(Region)\
#             .where(Region.region_id == region_id)\
#             .values(payload.dict(exclude_none=True, by_alias=True))
#
#         await db.execute(query)
#         await db.commit()
#
#         return await RegionDatabaseHandler.get_region_by_id(db, region_id)
#
#     @staticmethod
#     async def delete_region(db: AsyncSession, region_id: int) -> None:
#         query = delete(Region).\
#             where(Region.region_id == region_id)
#         await db.execute(query)
#
#     @staticmethod
#     async def check_if_region_exists(
#             db: AsyncSession,
#             region_name: str,
#             region_id: int = None
#     ) -> bool:
#         db_region = await RegionDatabaseHandler.get_region_by_name(db, region_name)
#         if db_region:
#             return True if db_region.region_id != region_id else False
#         else:
#             return False
