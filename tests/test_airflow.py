"""
Unit tests for Airflow DAG structure and standalone pipeline orchestrator.
"""

from dags.greek_tourism_pipeline import (
    PipelineOrchestrator,
    extract_api_task_func,
    upload_s3_task_func,
    validate_data_task_func,
    spark_transform_task_func,
    sql_analytics_task_func,
)


def test_airflow_tasks():
    res_extract = extract_api_task_func()
    assert "raw_count" in res_extract

    res_s3 = upload_s3_task_func()
    assert "json_path" in res_s3

    res_val = validate_data_task_func()
    assert "valid_count" in res_val

    res_spark = spark_transform_task_func()
    assert "transformed_count" in res_spark

    res_sql = sql_analytics_task_func()
    assert "top_regions_rows" in res_sql


def test_standalone_orchestrator():
    res = PipelineOrchestrator.run_full_pipeline()
    assert "extract" in res
    assert "s3" in res
    assert "validation" in res
    assert "pyspark" in res
    assert "database" in res
    assert "sql_analytics" in res
    assert "dashboard" in res
