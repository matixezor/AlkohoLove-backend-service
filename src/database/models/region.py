from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey

from src.database.database_metadata import Base


class Region(Base):
    __tablename__ = 'region'

    region_id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String)
    country_id = Column(Integer, ForeignKey('country.country_id'))

    country = relationship('Country', backref=backref('region', uselist=False), lazy='joined')
