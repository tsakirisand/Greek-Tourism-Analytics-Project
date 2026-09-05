"""
Unit tests for PySpark data processing engine (pyspark_processor.py).
"""

from pyspark_processor import PySparkProcessor, process_with_pyspark


def test_pyspark_processor_transform():
    raw_data = [
        {
            "geo": "EL30",
            "geo_label": "Attica",
            "year": 2023,
            "hotels_total_arrivals": 1000,
            "hotels_total_overnights": 3000,
            "hotels_occupancy": 80.0,
            "receipts": 10.5,
            "turnover_total": 50.0,
        }
    ]

    processor = PySparkProcessor()
    try:
        transformed = processor.transform_records(raw_data)
        assert len(transformed) == 1
        row = transformed[0]
        assert "arrivals" in row or "hotels_total_arrivals" in row
        # Check financial metric scaling
        assert row["receipts"] == 10.5 * 1_000_000
        assert row["turnover"] == 50.0 * 1_000
    finally:
        processor.stop()


def test_process_with_pyspark_helper():
    raw_data = [
        {
            "geo": "EL42",
            "geo_label": "South Aegean",
            "year": 2022,
            "hotels_total_arrivals": 2000,
            "hotels_total_overnights": 6000,
            "hotels_occupancy": 85.0,
            "receipts": 20.0,
            "turnover_total": 100.0,
        }
    ]

    results = process_with_pyspark(raw_data)
    assert len(results) == 1
    assert results[0]["geo"] == "EL42"
