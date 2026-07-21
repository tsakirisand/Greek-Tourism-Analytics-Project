"""
API Client for fetching Greek Tourism Data.
"""
import requests
import json
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

API_URL = "https://skillscapes.csd.auth.gr/api/data/greek-tourism"
logger = logging.getLogger(__name__)

def get_tourism_data() -> List[Dict[str, Any]]:
    """
    Fetches tourism data from the external API.

    Returns:
        A list of dictionaries containing the data records.
    """
    params = {
        "year_start": 2019,
        "year_end": 2024,
        "is_el_regional_unit": 0,
        "include": "hotels_total_arrivals,hotels_total_overnights,hotels_occupancy,receipts,turnover_total"
    }

    try:
        logger.info(f"Fetching data from {API_URL}...")
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info("Data fetched successfully from API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        sys.exit(1)


def save_raw_data(data: List[Dict[str, Any]], filename: str = "raw_data.json") -> None:
    """
    Saves the fetched raw data to a JSON file.
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / filename

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"Successfully saved {len(data)} records to {file_path}")
    except IOError as e:
        logger.error(f"Error saving data to file: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = get_tourism_data()
    save_raw_data(data)