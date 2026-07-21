"""
ETL script to load API data into the database with validation.
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from api_client import get_tourism_data
from database import get_session
from models import TourismData
from schemas import TourismDataRecord

logger = logging.getLogger(__name__)

def load():
    """Fetches data from the API, validates it, and loads it into the database."""
    logger.info("Starting data load process...")
    raw_data = get_tourism_data()

    if not raw_data:
        logger.warning("No data received from API. Aborting load.")
        return

    session = get_session()

    try:
        # Clear existing data to prevent duplicates on multiple runs
        deleted = session.query(TourismData).delete()
        logger.info(f"Cleared {deleted} old records from the database.")
        
        inserted_count = 0
        for item in raw_data:
            try:
                # Validate the incoming data using Pydantic
                valid_data = TourismDataRecord(**item)
                
                row = TourismData(
                    geo=valid_data.geo,
                    geo_label=valid_data.geo_label,
                    year=valid_data.year,
                    arrivals=valid_data.hotels_total_arrivals,
                    overnights=valid_data.hotels_total_overnights,
                    occupancy=valid_data.hotels_occupancy,
                    receipts=valid_data.receipts,
                    turnover=valid_data.turnover_total
                )
                session.add(row)
                inserted_count += 1
            except ValidationError as ve:
                logger.error(f"Data validation error for record {item.get('geo')}: {ve}")
        
        session.commit()
        logger.info(f"Successfully validated and inserted {inserted_count} rows into the database.")
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load()