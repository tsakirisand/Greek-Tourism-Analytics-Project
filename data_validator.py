"""
Data validation module implementing enterprise quality assertions and schema validation.
"""

from typing import Any, Dict, List, Tuple
from pydantic import ValidationError

from logger import logger
from schemas import TourismDataRecord


class DataValidationError(Exception):
    """Custom exception raised when critical data validation assertions fail."""

    pass


def validate_records(
    records: List[Dict[str, Any]],
) -> Tuple[List[TourismDataRecord], List[Dict[str, Any]]]:
    """Validates raw dictionaries against Pydantic schema and returns valid/invalid items.

    Args:
        records: List of dictionary raw records.

    Returns:
        Tuple[List[TourismDataRecord], List[Dict[str, Any]]]: Valid Pydantic records and invalid dicts.
    """
    logger.info(f"Starting Data Validation stage for {len(records)} records...")
    valid_records: List[TourismDataRecord] = []
    invalid_records: List[Dict[str, Any]] = []

    for item in records:
        try:
            record = TourismDataRecord(**item)
            # Custom domain validation checks
            if record.year < 2000 or record.year > 2100:
                logger.warning(
                    f"Invalid year encountered: {record.year} for geo {record.geo}"
                )
                invalid_records.append(item)
                continue

            if (
                record.hotels_total_arrivals is not None
                and record.hotels_total_arrivals < 0
            ) or (
                record.hotels_total_overnights is not None
                and record.hotels_total_overnights < 0
            ):
                logger.warning(f"Negative metric value for geo {record.geo}")
                invalid_records.append(item)
                continue

            valid_records.append(record)
        except ValidationError as ve:
            logger.warning(f"Record validation failed for geo {item.get('geo')}: {ve}")
            invalid_records.append(item)

    logger.info(
        f"Data Validation completed: {len(valid_records)} valid records, "
        f"{len(invalid_records)} invalid records."
    )
    return valid_records, invalid_records


def assert_pipeline_quality(
    records: List[TourismDataRecord], min_records: int = 1
) -> bool:
    """Quality assertion to ensure the dataset meets baseline standard before processing.

    Args:
        records: Validated list of records.
        min_records: Minimum required record count.

    Returns:
        bool: True if validation assertions pass.

    Raises:
        DataValidationError: If dataset quality checks fail.
    """
    if len(records) < min_records:
        raise DataValidationError(
            f"Quality Assertion Failed: Received {len(records)} records, expected at least {min_records}."
        )

    geos = {r.geo for r in records}
    if not geos:
        raise DataValidationError(
            "Quality Assertion Failed: Dataset contains no geographic region identifiers."
        )

    logger.info(
        f"Pipeline Quality Assertion passed for {len(records)} valid records across {len(geos)} regions."
    )
    return True
