"""
API Client module for fetching Greek Tourism and Eurostat boundary data.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from logger import logger

API_URL = "https://skillscapes.csd.auth.gr/api/data/greek-tourism"
EUROSTAT_GEOJSON_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_60M_2021_4326_LEVL_2.geojson"


class APIError(Exception):
    """Custom exception raised for API fetching or network failure errors."""

    pass


def get_tourism_data(
    url: str = API_URL,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 10,
) -> List[Dict[str, Any]]:
    """Fetches tourism data records from the external API.

    Args:
        url: The API endpoint URL to fetch data from.
        params: Optional dictionary of query parameters.
        timeout: Network request timeout in seconds.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing raw tourism data records.

    Raises:
        APIError: If a network error, timeout, or HTTP error occurs.
    """
    if params is None:
        params = {
            "year_start": 2019,
            "year_end": 2024,
            "is_el_regional_unit": 0,
            "include": "hotels_total_arrivals,hotels_total_overnights,hotels_occupancy,receipts,turnover_total",
        }

    try:
        logger.info(f"Fetching tourism data from API endpoint: {url}")
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise APIError(f"Unexpected data format received from API: {type(data)}")
        logger.info(f"Successfully fetched {len(data)} records from API.")
        return data
    except (requests.exceptions.RequestException, ValueError, APIError) as e:
        error_msg = f"Failed to fetch data from API: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e


def get_eurostat_boundaries(
    url: str = EUROSTAT_GEOJSON_URL, timeout: int = 10
) -> Dict[str, Any]:
    """Fetches official NUTS 2 geographic boundaries from the Eurostat Open Data API.

    Args:
        url: GeoJSON URL for Eurostat NUTS 2 boundaries.
        timeout: Request timeout in seconds.

    Returns:
        Dict[str, Any]: GeoJSON feature collection dictionary or empty dict on failure.
    """
    try:
        logger.info("Fetching Eurostat NUTS 2 geographic boundaries...")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        geojson_data = response.json()
        logger.info("Eurostat geographic boundaries fetched successfully.")
        return geojson_data
    except (requests.exceptions.RequestException, ValueError) as e:
        logger.warning(f"Could not fetch Eurostat boundaries: {e}")
        return {}


def save_raw_data(data: List[Dict[str, Any]], filename: str = "raw_data.json") -> None:
    """Saves raw API records to a JSON file in the data directory.

    Args:
        data: List of record dictionaries to save.
        filename: Target JSON filename.
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / filename

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"Successfully saved {len(data)} records to {file_path}")
    except IOError as e:
        logger.error(f"Error saving data to file {file_path}: {e}")
        raise


if __name__ == "__main__":
    try:
        records = get_tourism_data()
        save_raw_data(records)
    except APIError as err:
        logger.error(f"Script aborted due to API failure: {err}")
