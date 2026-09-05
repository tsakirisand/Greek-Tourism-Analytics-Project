"""
Main CLI entry point for the Greek Tourism Project.

Provides options for database initialization, enterprise multi-stage ETL data loading,
S3 staging, Data Validation, PySpark execution, SQL query analytics, and Streamlit dashboard.
"""

import argparse
import subprocess  # nosec B404
import sys

from api_client import get_tourism_data
from create_tables import init_db
from dags.greek_tourism_pipeline import PipelineOrchestrator
from data_validator import assert_pipeline_quality, validate_records
from loader import load, save_raw_files
from logger import logger
from pyspark_processor import process_with_pyspark
from queries import (
    get_cumulative_arrivals_by_region,
    get_regional_rankings_by_year,
    get_top_regions_by_arrivals,
    get_yoy_growth_analysis,
)
from s3_client import upload_to_s3


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
        description="Greek Tourism Analytics Enterprise CLI Data Management Tool"
    )

    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database schema and indexes.",
    )

    parser.add_argument(
        "--load-data",
        action="store_true",
        help="Fetch data from API, stage to S3, validate, transform via PySpark, and load into PostgreSQL.",
    )

    parser.add_argument(
        "--s3-upload",
        action="store_true",
        help="Fetch API raw JSON/CSV data and stage to S3 bucket / local fallback.",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run Pydantic schema validation and quality assertions on raw dataset.",
    )

    parser.add_argument(
        "--spark-transform",
        action="store_true",
        help="Run PySpark SQL DataFrame transformation engine on input data.",
    )

    parser.add_argument(
        "--pipeline-all",
        action="store_true",
        help="Execute complete 9-stage pipeline (API -> S3 -> Validation -> PySpark -> Postgres -> SQL Analytics -> Dashboard).",
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

    if args.s3_upload:
        raw = get_tourism_data()
        save_raw_files(raw)
        res = upload_to_s3(raw)
        print(f"\n--- S3 Staging Upload Results ---\n{res}")

    if args.validate:
        raw = get_tourism_data()
        valid, invalid = validate_records(raw)
        assert_pipeline_quality(valid)
        print(
            f"\n--- Data Validation Results ---\nValid: {len(valid)}, Invalid: {len(invalid)}"
        )

    if args.spark_transform:
        raw = get_tourism_data()
        transformed = process_with_pyspark(raw)
        print(f"\n--- PySpark Transformed Records count: {len(transformed)} ---")

    if args.load_data:
        load()

    if args.pipeline_all:
        res = PipelineOrchestrator.run_full_pipeline()
        print(f"\n--- Enterprise 9-Stage Pipeline Completed ---\n{res}")

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
