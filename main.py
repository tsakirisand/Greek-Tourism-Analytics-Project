"""
Main CLI entry point for the Greek Tourism Project.

Provides options for database initialization, ETL data loading, SQL query execution,
and launching the Streamlit dashboard.
"""

import argparse
import subprocess  # nosec B404
import sys

from create_tables import init_db
from loader import load
from logger import logger
from queries import (
    get_cumulative_arrivals_by_region,
    get_regional_rankings_by_year,
    get_top_regions_by_arrivals,
    get_yoy_growth_analysis,
)


def run_dashboard() -> None:
    """Launches the interactive Streamlit dashboard application."""
    logger.info("Starting Streamlit Dashboard application...")
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", "app/🏛️_Dashboard.py"]
        subprocess.run(cmd, check=True)  # nosec B603 B607
    except KeyboardInterrupt:
        logger.info("Dashboard process stopped by user.")
    except Exception as e:
        logger.error(f"Failed to start Streamlit Dashboard: {e}")


def main() -> None:
    """Parses CLI arguments and dispatches commands."""
    parser = argparse.ArgumentParser(
        description="Greek Tourism Analytics CLI Management Tool"
    )

    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database schema and indexes.",
    )

    parser.add_argument(
        "--load-data",
        action="store_true",
        help="Fetch data from API, validate, transform, and load into PostgreSQL.",
    )

    parser.add_argument(
        "--query-top",
        type=int,
        metavar="N",
        help="Query and display top N regions by arrivals.",
    )

    parser.add_argument(
        "--query-window",
        action="store_true",
        help="Run SQL window functions (Cumulative sums, rankings, YoY growth).",
    )

    parser.add_argument(
        "--dashboard", action="store_true", help="Launch Streamlit Dashboard."
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    logger.info("Starting Greek Tourism Analytics CLI")

    if args.init_db:
        init_db()

    if args.load_data:
        load()

    if args.query_top:
        df = get_top_regions_by_arrivals(limit=args.query_top)
        print(f"\n--- Top {args.query_top} Regions by Arrivals ---")
        print(df.to_string(index=False))

    if args.query_window:
        print("\n--- Cumulative Arrivals (SUM OVER) ---")
        print(get_cumulative_arrivals_by_region().head())
        print("\n--- Regional Rankings (RANK OVER) ---")
        print(get_regional_rankings_by_year().head())
        print("\n--- YoY Growth Analysis (LAG OVER) ---")
        print(get_yoy_growth_analysis().head())

    if args.dashboard:
        run_dashboard()


if __name__ == "__main__":
    main()
