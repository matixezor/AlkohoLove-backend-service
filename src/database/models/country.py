from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, select, func, delete, update

from src.database.database_metadata import Base


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String)


class CountryDatabaseHandler:
    @staticmethod
    async def get_country_by_id(db: AsyncSession, country_id: int) -> Country | None:
        return await db.get(Country, country_id)

    @staticmethod
    async def get_country_by_name(db: AsyncSession, country_name: str) -> Country | None:
        query = select(Country).filter(Country.country_name == country_name).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def update_country(db: AsyncSession, country_id: int, country_name: str) -> Country:
        query = update(Country)\
            .where(Country.country_id == country_id)\
            .values(country_name=country_name)

        await db.execute(query)
        await db.commit()

        return await CountryDatabaseHandler.get_country_by_id(db, country_id)

    @staticmethod
    async def get_paginated_countries(
            db: AsyncSession,
            country_name: str,
            limit: int,
            offset: int
    ) -> list[Country]:
        query = select(Country).order_by(Country.country_id)\
            .where(Country.country_name.contains(country_name)).offset(offset).limit(limit)
        db_countries = await db.execute(query)
        return db_countries.scalars().unique().all()

    @staticmethod
    async def count_countries(db: AsyncSession, country_name: str) -> int:
        query = select(func.count()).select_from(
            select(Country).where(Country.country_name.contains(country_name)).subquery()
        )
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def create_country(db: AsyncSession, country_name: str) -> None:
        db_country = Country(country_name=country_name)
        db.add(db_country)

    @staticmethod
    async def delete_country(db: AsyncSession, country_id: int) -> None:
        query = delete(Country).\
            where(Country.country_id == country_id)
        await db.execute(query)

    @staticmethod
    async def check_if_country_exists(
            db: AsyncSession,
            country_name: str,
            country_id: int = None
    ) -> bool:
        db_country = await CountryDatabaseHandler.get_country_by_name(db, country_name)
        if db_country:
            return True if db_country.country_id != country_id else False
        else:
            return False
