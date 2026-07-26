"""
Database models for Greek Tourism data analytics dashboard.
"""

from sqlalchemy import Column, Float, Index, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TourismData(Base):
    """Model representing tourism data records with database indexes."""

    __tablename__ = "tourism_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    geo = Column(String, nullable=False, index=True)
    geo_label = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    arrivals = Column(Float, default=0.0)
    overnights = Column(Float, default=0.0)
    occupancy = Column(Float, default=0.0)
    receipts = Column(Float, default=0.0)
    turnover = Column(Float, default=0.0)

    __table_args__ = (
        Index("idx_geo_year", "geo_label", "year"),
        Index("idx_geo_code_year", "geo", "year"),
    )

    def __repr__(self) -> str:
        return (
            f"<TourismData(geo_label='{self.geo_label}', year={self.year}, "
            f"arrivals={self.arrivals})>"
        )
