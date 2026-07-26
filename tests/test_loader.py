"""
Unit tests for loader (ETL pipeline) module.
"""

from unittest.mock import patch
import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_client import APIError
from loader import load, transform_data
from models import Base, TourismData


@pytest.fixture
def test_db_session():
    """Fixture providing an in-memory SQLite database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mock_api_raw_records():
    return [
        {
            "geo": "EL30",
            "geo_label": "Attiki",
            "year": 2023,
            "hotels_total_arrivals": 1000.0,
            "hotels_total_overnights": 3000.0,
            "hotels_occupancy": 60.0,
            "receipts": 2500.0,
            "turnover_total": 3000.0,
        },
        {
            "geo": "EL42",
            "geo_label": "Notio Aigaio",
            "year": 2023,
            "hotels_total_arrivals": 2000.0,
            "hotels_total_overnights": 8000.0,
            "hotels_occupancy": 75.0,
            "receipts": 4500.0,
            "turnover_total": 5000.0,
        },
    ]


def test_transform_data_pandas_operations():
    """Test pandas data transformation and unit scaling."""
    raw_df = pd.DataFrame(
        [
            {
                "hotels_total_arrivals": 100,
                "hotels_total_overnights": 300,
                "hotels_occupancy": 50,
                "receipts": 2.5,
                "turnover_total": 3.0,
            }
        ]
    )

    transformed = transform_data(raw_df)

    assert "arrivals" in transformed.columns
    assert "overnights" in transformed.columns
    assert "turnover" in transformed.columns
    assert transformed.iloc[0]["receipts"] == 2_500_000.0
    assert transformed.iloc[0]["turnover"] == 3_000.0


def test_transform_data_empty():
    """Test transform_data with an empty DataFrame."""
    empty_df = pd.DataFrame()
    res = transform_data(empty_df)
    assert res.empty


def test_load_pipeline_success(test_db_session, mock_api_raw_records):
    """Test ETL pipeline end-to-end with mock API and in-memory SQLite session."""
    with patch("loader.get_tourism_data", return_value=mock_api_raw_records):
        count = load(session_override=test_db_session)

        assert count == 2
        records = test_db_session.query(TourismData).all()
        assert len(records) == 2
        assert records[0].geo_label == "Attiki"
        assert records[0].arrivals == 1000.0


def test_load_pipeline_api_error(test_db_session):
    """Test ETL pipeline when API raises APIError."""
    with patch("loader.get_tourism_data", side_effect=APIError("API down")):
        count = load(session_override=test_db_session)
        assert count == 0
        records = test_db_session.query(TourismData).all()
        assert len(records) == 0


def test_load_pipeline_invalid_record_skip(test_db_session):
    """Test ETL pipeline skips records failing Pydantic schema validation."""
    invalid_records = [
        {
            "geo": "EL30",
            "geo_label": "Attiki",
            "year": 1800,  # Invalid year < 2000
            "hotels_total_arrivals": 1000.0,
        },
        {
            "geo": "EL42",
            "geo_label": "Notio Aigaio",
            "year": 2023,
            "hotels_total_arrivals": 2000.0,
        },
    ]

    with patch("loader.get_tourism_data", return_value=invalid_records):
        count = load(session_override=test_db_session)
        assert count == 1
        records = test_db_session.query(TourismData).all()
        assert len(records) == 1
        assert records[0].geo_label == "Notio Aigaio"
