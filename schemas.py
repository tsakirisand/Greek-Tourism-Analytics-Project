from pydantic import BaseModel, Field
from typing import Optional

class TourismDataRecord(BaseModel):
    """Schema for validating data returned from the Greek Tourism API."""
    geo: str = Field(..., description="The geographical code of the region.")
    geo_label: str = Field(..., description="The human-readable name of the region.")
    year: int = Field(..., ge=2000, le=2100, description="The year of the data record.")
    hotels_total_arrivals: Optional[float] = Field(None, description="Total arrivals.")
    hotels_total_overnights: Optional[float] = Field(None, description="Total overnights.")
    hotels_occupancy: Optional[float] = Field(None, description="Average occupancy.")
    receipts: Optional[float] = Field(None, description="Total receipts.")
    turnover_total: Optional[float] = Field(None, description="Total turnover.")
