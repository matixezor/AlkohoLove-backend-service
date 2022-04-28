from sqlalchemy import Column, Integer, String

from src.database.database_metadata import Base


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String)
