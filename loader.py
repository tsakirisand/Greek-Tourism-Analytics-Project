"""
ETL pipeline loader module to fetch, validate, transform, and load API data into PostgreSQL.
"""

from typing import Optional
import pandas as pd
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api_client import APIError, get_tourism_data
from database import get_session
from logger import logger
from models import TourismData
from schemas import TourismDataRecord


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Applies data transformations and unit scaling to raw pandas DataFrame.

    Args:
        df: Raw pandas DataFrame parsed from API records.

    Returns:
        pd.DataFrame: Transformed DataFrame with renamed columns and scaled metrics.
    """
    if df.empty:
        return df

    transformed = df.copy()

    rename_map = {
        "hotels_total_arrivals": "arrivals",
        "hotels_total_overnights": "overnights",
        "hotels_occupancy": "occupancy",
        "turnover_total": "turnover",
    }
    transformed = transformed.rename(columns=rename_map)

    # Scale financial metrics to full numeric values if available
    if "receipts" in transformed.columns:
        transformed["receipts"] = transformed["receipts"] * 1_000_000
    if "turnover" in transformed.columns:
        transformed["turnover"] = transformed["turnover"] * 1_000

    return transformed


def load(session_override: Optional[Session] = None) -> int:
    """Fetches data from the API, validates it using Pydantic, and loads it into the database.

    Args:
        session_override: Optional SQLAlchemy Session object for testing.

    Returns:
        int: Total number of valid records inserted into the database.
    """
    logger.info("Starting ETL data load process...")
    try:
        raw_data = get_tourism_data()
    except APIError as e:
        logger.error(f"ETL pipeline aborted due to API error: {e}")
        return 0

    if not raw_data:
        logger.warning("No data received from API. Aborting load.")
        return 0

    session = session_override if session_override is not None else get_session()
    if session is None:
        logger.error("Database session unavailable. Aborting load.")
        return 0

    close_session = session_override is None

    try:
        # Clear existing records to maintain idempotent state
        deleted_count = session.query(TourismData).delete()
        logger.info(f"Cleared {deleted_count} old records from tourism_data table.")

        inserted_count = 0
        for item in raw_data:
            try:
                valid_record = TourismDataRecord(**item)

                row = TourismData(
                    geo=valid_record.geo,
                    geo_label=valid_record.geo_label,
                    year=valid_record.year,
                    arrivals=valid_record.hotels_total_arrivals,
                    overnights=valid_record.hotels_total_overnights,
                    occupancy=valid_record.hotels_occupancy,
                    receipts=valid_record.receipts,
                    turnover=valid_record.turnover_total,
                )
                session.add(row)
                inserted_count += 1
            except ValidationError as ve:
                logger.error(
                    f"Data validation error for record {item.get('geo')}: {ve}"
                )

        session.commit()
        logger.info(
            f"ETL pipeline completed: successfully loaded {inserted_count} records."
        )
        return inserted_count
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error during ETL load: {e}")
        return 0
    finally:
        if close_session:
            session.close()


if __name__ == "__main__":
    load()
