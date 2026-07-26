"""
Unit tests for api_client module.
"""

import json
from unittest.mock import MagicMock, patch
import pytest
import requests
from api_client import (
    APIError,
    get_eurostat_boundaries,
    get_tourism_data,
    save_raw_data,
)


@pytest.fixture
def mock_valid_tourism_data():
    return [
        {
            "geo": "EL30",
            "geo_label": "Attiki",
            "year": 2023,
            "hotels_total_arrivals": 5000000.0,
            "hotels_total_overnights": 15000000.0,
            "hotels_occupancy": 65.5,
            "receipts": 2500.0,
            "turnover_total": 3000.0,
        },
        {
            "geo": "EL42",
            "geo_label": "Notio Aigaio",
            "year": 2023,
            "hotels_total_arrivals": 4000000.0,
            "hotels_total_overnights": 18000000.0,
            "hotels_occupancy": 72.0,
            "receipts": 3200.0,
            "turnover_total": 3800.0,
        },
    ]


def test_get_tourism_data_success(mock_valid_tourism_data):
    """Test fetching API data returns valid non-empty list of dicts."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_valid_tourism_data
        mock_get.return_value = mock_response

        data = get_tourism_data()

        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["geo"] == "EL30"
        assert data[0]["geo_label"] == "Attiki"
        assert data[0]["year"] == 2023
        assert isinstance(data[0]["hotels_total_arrivals"], float)


def test_get_tourism_data_validation_keys(mock_valid_tourism_data):
    """Test data validation for required keys and types."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_valid_tourism_data
        mock_get.return_value = mock_response

        data = get_tourism_data()
        required_keys = {
            "geo",
            "geo_label",
            "year",
            "hotels_total_arrivals",
            "receipts",
        }

        for record in data:
            assert required_keys.issubset(record.keys())
            assert isinstance(record["geo"], str)
            assert isinstance(record["year"], int)


def test_get_tourism_data_network_failure():
    """Test API error handling on network failure."""
    with patch(
        "requests.get", side_effect=requests.exceptions.ConnectionError("Network Down")
    ):
        with pytest.raises(APIError) as exc_info:
            get_tourism_data()
        assert "Failed to fetch data from API" in str(exc_info.value)


def test_get_tourism_data_http_500():
    """Test API error handling on HTTP 500 status code."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error"
        )
        mock_get.return_value = mock_response

        with pytest.raises(APIError):
            get_tourism_data()


def test_get_eurostat_boundaries_success():
    """Test fetching Eurostat NUTS 2 boundaries successfully."""
    fake_geojson = {"type": "FeatureCollection", "features": []}
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_geojson
        mock_get.return_value = mock_response

        boundaries = get_eurostat_boundaries()
        assert boundaries["type"] == "FeatureCollection"


def test_get_eurostat_boundaries_failure():
    """Test Eurostat boundary fetch failure fallback to empty dict."""
    with patch("requests.get", side_effect=requests.exceptions.Timeout("Timed out")):
        boundaries = get_eurostat_boundaries()
        assert boundaries == {}


def test_save_raw_data(tmp_path, mock_valid_tourism_data):
    """Test saving raw JSON data to file."""
    with patch("api_client.Path") as mock_path:
        mock_path.return_value = tmp_path
        target_file = tmp_path / "test_raw.json"

        save_raw_data(mock_valid_tourism_data, filename="test_raw.json")

        assert target_file.exists()
        with open(target_file, "r", encoding="utf-8") as f:
            content = json.load(f)
            assert len(content) == 2
