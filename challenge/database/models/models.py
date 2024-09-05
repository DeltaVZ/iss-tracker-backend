from sqlalchemy import Column, Integer, String, Float, DateTime, Enum

from challenge.database.database import Base
from challenge.database.models.visibility import Visibility


class IssPosition(Base):
    """
    It represents an ISS Position
    """
    __tablename__ = "iss_positions"

    name = Column(String)
    satellite_id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    velocity = Column(Float)
    visibility = Column(Enum(Visibility))
    footprint = Column(Float)
    timestamp = Column(DateTime, primary_key=True, index=True)
    daynum = Column(Float)
    solar_lat = Column(Float)
    solar_lon = Column(Float)
    units = Column(String)
