"""
Database models.
"""
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TourismData(Base):
    """
    Model representing tourism data records.
    """
    __tablename__ = "tourism_data"

    id = Column(Integer, primary_key=True)
    geo = Column(String)
    geo_label = Column(String)
    year = Column(Integer)
    arrivals = Column(Float)
    overnights = Column(Float)
    occupancy = Column(Float)
    receipts = Column(Float)
    turnover = Column(Float)

    def __repr__(self):
        return f"<TourismData(geo_label='{self.geo_label}', year={self.year}, arrivals={self.arrivals})>"