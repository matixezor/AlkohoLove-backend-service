from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, select
from fastapi import HTTPException, status

from src.database.database_metadata import Base
from src.domain.country import CountryCreate


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String)

class CountryDatabaseHandler:

    @staticmethod
    def raise_country_already_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Country already exists'
        )

    @staticmethod
    async def get_country_by_name(db: AsyncSession, country_name: str) -> Country | None:
        query = select(Country).filter(Country.country_name == country_name).limit(1)
        result = await db.execute(query)
        return result.scalars().first()


    @staticmethod
    async def get_all_countries(db: AsyncSession) -> list[Country]:
        query = select(Country)
        db_countries = await db.execute(query)
        return db_countries.scalars().all()

    @staticmethod
    async def create_country(db: AsyncSession, country_create_payload: CountryCreate) -> Country:
        db_country = Country(
            **country_create_payload.dict(),
        )

        db.add(db_country)
        await db.commit()
        await db.refresh(db_country)

        return db_country

    @staticmethod
    async def check_if_country_exists(db: AsyncSession, country_name: str, ) -> None:
        if await CountryDatabaseHandler.get_country_by_name(db, country_name):
            CountryDatabaseHandler.raise_country_already_exists()
