"""
ETL pipeline loader module executing the multi-stage enterprise pipeline:
    API -> Raw JSON/CSV -> S3 -> Airflow -> Data Validation -> PySpark -> PostgreSQL/Warehouse -> SQL Analytics -> Dashboard
"""

import json
import os
from typing import Any, Dict, List, Optional
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api_client import APIError, get_tourism_data
from data_validator import assert_pipeline_quality, validate_records
from database import get_session
from logger import logger
from models import TourismData
from pyspark_processor import process_with_pyspark
from s3_client import upload_to_s3


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


def save_raw_files(raw_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """Persists raw API responses as JSON and CSV local staging files.

    Args:
        raw_data: List of raw dictionaries.

    Returns:
        Dict[str, str]: Map of local raw file paths.
    """
    os.makedirs("data/raw", exist_ok=True)
    json_path = "data/raw/tourism_data.json"
    csv_path = "data/raw/tourism_data.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    df_raw = pd.DataFrame(raw_data)
    df_raw.to_csv(csv_path, index=False, encoding="utf-8")

    logger.info(f"Persisted Raw JSON ({json_path}) and CSV ({csv_path}).")
    return {"json_path": json_path, "csv_path": csv_path}


def load(session_override: Optional[Session] = None) -> int:
    """Executes the full 9-stage ETL pipeline into the PostgreSQL database.

    Args:
        session_override: Optional SQLAlchemy Session object for testing.

    Returns:
        int: Total number of valid records inserted into the database.
    """
    logger.info("Starting Enterprise ETL data load process...")

    # Stage 1: API Fetch
    try:
        raw_data = get_tourism_data()
    except APIError as e:
        logger.error(f"ETL pipeline aborted due to API error: {e}")
        return 0

    if not raw_data:
        logger.warning("No data received from API. Aborting load.")
        return 0

    # Stage 2: Raw JSON / CSV Persist
    save_raw_files(raw_data)

    # Stage 3: S3 Bucket Upload
    try:
        upload_to_s3(raw_data, pd.DataFrame(raw_data))
    except Exception as e:
        logger.warning(f"S3 upload step encountered warning: {e}")

    # Stage 5: Data Validation Layer
    valid_records, invalid_records = validate_records(raw_data)
    try:
        assert_pipeline_quality(valid_records, min_records=1)
    except Exception as ve:
        logger.error(f"Data Validation quality assertion failed: {ve}")
        return 0

    # Stage 6: PySpark Transformation Engine
    raw_dicts_to_transform = [r.model_dump() for r in valid_records]
    spark_transformed_records = process_with_pyspark(raw_dicts_to_transform)

    # Stage 7: PostgreSQL Warehouse Loading
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
        for rec in spark_transformed_records:
            row = TourismData(
                geo=rec.get("geo"),
                geo_label=rec.get("geo_label"),
                year=rec.get("year"),
                arrivals=rec.get("arrivals", rec.get("hotels_total_arrivals")),
                overnights=rec.get("overnights", rec.get("hotels_total_overnights")),
                occupancy=rec.get("occupancy", rec.get("hotels_occupancy")),
                receipts=rec.get("receipts", 0.0),
                turnover=rec.get("turnover", 0.0),
            )
            session.add(row)
            inserted_count += 1

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
