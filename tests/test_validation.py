"""
Unit tests for data validation and pipeline assertions (data_validator.py).
"""

import pytest
from data_validator import (
    DataValidationError,
    assert_pipeline_quality,
    validate_records,
)


def test_validate_records():
    records = [
        {
            "geo": "EL30",
            "geo_label": "Attica",
            "year": 2023,
            "hotels_total_arrivals": 5000,
            "hotels_total_overnights": 15000,
            "hotels_occupancy": 75.5,
            "turnover_total": 1000.0,
            "receipts": 500.0,
        },
        {
            "geo": "INVALID",
            "geo_label": "Bad Year",
            "year": 1800,  # invalid year bounds
            "hotels_total_arrivals": 100,
            "hotels_total_overnights": 100,
            "hotels_occupancy": 10.0,
        },
    ]

    valid, invalid = validate_records(records)
    assert len(valid) == 1
    assert len(invalid) == 1
    assert valid[0].geo == "EL30"


def test_assert_pipeline_quality():
    records, _ = validate_records(
        [
            {
                "geo": "EL30",
                "geo_label": "Attica",
                "year": 2023,
                "hotels_total_arrivals": 5000,
                "hotels_total_overnights": 15000,
                "hotels_occupancy": 75.5,
            }
        ]
    )

    assert assert_pipeline_quality(records, min_records=1) is True

    with pytest.raises(DataValidationError):
        assert_pipeline_quality([], min_records=1)
