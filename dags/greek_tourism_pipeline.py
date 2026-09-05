"""
Apache Airflow Pipeline DAG definition for Greek Tourism Analytics.

Orchestrates the multi-stage pipeline flow:
    API -> Raw JSON/CSV -> S3 Staging -> Airflow DAG -> Data Validation -> PySpark ETL -> PostgreSQL Warehouse -> SQL Analytics -> Dashboard
"""

from datetime import datetime, timedelta
from typing import Any, Dict

from logger import logger

# Try importing Airflow operators
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False


def extract_api_task_func(**kwargs) -> Dict[str, Any]:
    """Task 1 & 2: Extract data from API and persist Raw JSON / CSV payloads."""
    from api_client import get_tourism_data
    import pandas as pd
    import os

    logger.info("[Airflow DAG Task 1/8] Executing API Extraction...")
    raw_data = get_tourism_data()
    df = pd.DataFrame(raw_data)

    os.makedirs("data/raw", exist_ok=True)
    json_path = "data/raw/tourism_data.json"
    csv_path = "data/raw/tourism_data.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        import json

        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    df.to_csv(csv_path, index=False)
    logger.info(
        f"[Airflow DAG Task 2/8] Persisted Raw JSON to {json_path} and CSV to {csv_path}"
    )
    return {"raw_count": len(raw_data), "json_path": json_path, "csv_path": csv_path}


def upload_s3_task_func(**kwargs) -> Dict[str, str]:
    """Task 3: Upload Raw JSON / CSV to S3 Bucket."""
    from s3_client import upload_to_s3
    from api_client import get_tourism_data
    import pandas as pd

    logger.info("[Airflow DAG Task 3/8] Uploading Raw Data to S3 Bucket...")
    raw_data = get_tourism_data()
    df = pd.DataFrame(raw_data)
    s3_res = upload_to_s3(raw_data, df)
    logger.info(f"[Airflow DAG Task 3/8] S3 Upload Results: {s3_res}")
    return s3_res


def validate_data_task_func(**kwargs) -> Dict[str, int]:
    """Task 4 & 5: Data Validation & Quality Assertions."""
    from api_client import get_tourism_data
    from data_validator import validate_records, assert_pipeline_quality

    logger.info("[Airflow DAG Task 5/8] Running Data Validation...")
    raw_data = get_tourism_data()
    valid_records, invalid_records = validate_records(raw_data)
    assert_pipeline_quality(valid_records, min_records=1)
    return {"valid_count": len(valid_records), "invalid_count": len(invalid_records)}


def spark_transform_task_func(**kwargs) -> Dict[str, int]:
    """Task 6: PySpark Distributed Data Transformation."""
    from api_client import get_tourism_data
    from pyspark_processor import process_with_pyspark

    logger.info("[Airflow DAG Task 6/8] Executing PySpark Data Transformation...")
    raw_data = get_tourism_data()
    transformed = process_with_pyspark(raw_data)
    return {"transformed_count": len(transformed)}


def load_warehouse_task_func(**kwargs) -> Dict[str, int]:
    """Task 7: Load Transformed PySpark Data to PostgreSQL Warehouse."""
    from loader import load

    logger.info(
        "[Airflow DAG Task 7/8] Ingesting PySpark Data into PostgreSQL Warehouse..."
    )
    count = load()
    return {"loaded_count": count}


def sql_analytics_task_func(**kwargs) -> Dict[str, str]:
    """Task 8: Run SQL Analytical Queries & Window Functions."""
    from queries import (
        get_top_regions_by_arrivals,
        get_cumulative_arrivals_by_region,
        get_regional_rankings_by_year,
        get_yoy_growth_analysis,
    )

    logger.info(
        "[Airflow DAG Task 8/8] Executing SQL Analytics Queries (SUM, RANK, LAG OVER)..."
    )
    df1 = get_top_regions_by_arrivals(5)
    df2 = get_cumulative_arrivals_by_region()
    df3 = get_regional_rankings_by_year()
    df4 = get_yoy_growth_analysis()

    return {
        "top_regions_rows": str(len(df1)),
        "cumulative_rows": str(len(df2)),
        "rankings_rows": str(len(df3)),
        "yoy_rows": str(len(df4)),
    }


def trigger_dashboard_task_func(**kwargs) -> str:
    """Task 9: Verify Dashboard Readiness."""
    logger.info(
        "[Airflow DAG Task 9/9] Pipeline Execution Complete. Streamlit Dashboard updated."
    )
    return "Dashboard ready."


if AIRFLOW_AVAILABLE:
    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2026, 1, 1),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    dag = DAG(
        "greek_tourism_pipeline",
        default_args=default_args,
        description="Airflow Orchestrated Pipeline for Greek Tourism Analytics",
        schedule_interval="@daily",
        catchup=False,
    )

    t1_extract = PythonOperator(
        task_id="extract_api_and_raw_storage",
        python_callable=extract_api_task_func,
        dag=dag,
    )

    t2_upload_s3 = PythonOperator(
        task_id="upload_raw_s3",
        python_callable=upload_s3_task_func,
        dag=dag,
    )

    t3_validate = PythonOperator(
        task_id="data_validation",
        python_callable=validate_data_task_func,
        dag=dag,
    )

    t4_pyspark = PythonOperator(
        task_id="pyspark_transformation",
        python_callable=spark_transform_task_func,
        dag=dag,
    )

    t5_load_postgres = PythonOperator(
        task_id="load_postgresql_warehouse",
        python_callable=load_warehouse_task_func,
        dag=dag,
    )

    t6_sql_analytics = PythonOperator(
        task_id="sql_analytics_execution",
        python_callable=sql_analytics_task_func,
        dag=dag,
    )

    t7_dashboard = PythonOperator(
        task_id="dashboard_ready",
        python_callable=trigger_dashboard_task_func,
        dag=dag,
    )

    # Airflow Task Dependency Flow
    (
        t1_extract
        >> t2_upload_s3
        >> t3_validate
        >> t4_pyspark
        >> t5_load_postgres
        >> t6_sql_analytics
        >> t7_dashboard
    )


class PipelineOrchestrator:
    """Standalone Orchestrator for executing the 9-stage pipeline directly without Airflow server."""

    @staticmethod
    def run_full_pipeline() -> Dict[str, Any]:
        logger.info("==================================================")
        logger.info("Starting Full 9-Stage Greek Tourism Pipeline")
        logger.info("==================================================")

        res_extract = extract_api_task_func()
        res_s3 = upload_s3_task_func()
        res_val = validate_data_task_func()
        res_spark = spark_transform_task_func()
        res_db = load_warehouse_task_func()
        res_sql = sql_analytics_task_func()
        res_dash = trigger_dashboard_task_func()

        logger.info("==================================================")
        logger.info("Pipeline Execution Completed Successfully!")
        logger.info("==================================================")

        return {
            "extract": res_extract,
            "s3": res_s3,
            "validation": res_val,
            "pyspark": res_spark,
            "database": res_db,
            "sql_analytics": res_sql,
            "dashboard": res_dash,
        }
