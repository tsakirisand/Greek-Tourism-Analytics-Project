"""
PySpark ETL Data Processing Engine.

Performs scalable distributed data transformations, unit scaling, metric calculations,
and schema standardization using PySpark SQL DataFrames (with fallback for non-JVM environments).
"""

from typing import Any, Dict, List, Optional
import pandas as pd

from logger import logger

# Try importing PySpark
try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, lit

    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False



class PySparkProcessor:
    """ETL Processor utilizing PySpark SQL DataFrame engine with fallback support."""

    def __init__(self, app_name: str = "GreekTourismPySparkProcessor"):
        self.app_name = app_name
        self.spark: Optional[Any] = None

        if PYSPARK_AVAILABLE:
            try:
                self.spark = (
                    SparkSession.builder.appName(app_name)
                    .master("local[*]")
                    .config("spark.driver.bindAddress", "127.0.0.1")
                    .getOrCreate()
                )
                # Lower log level for clean CLI output
                self.spark.sparkContext.setLogLevel("WARN")
                logger.info("Initialized PySpark SparkSession successfully.")
            except Exception as e:
                logger.warning(
                    f"PySpark SparkSession initialization bypassed ({e}). Using pandas fallback engine."
                )
                self.spark = None

    def transform_records(
        self, raw_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Processes raw dictionary records through PySpark transformation pipeline.

        Args:
            raw_records: Input dictionary records.

        Returns:
            List[Dict[str, Any]]: Transformed records ready for PostgreSQL data warehouse loading.
        """
        if not raw_records:
            logger.warning("Empty records passed to PySpark processor.")
            return []

        logger.info(
            f"Running PySpark transformation pipeline on {len(raw_records)} records..."
        )

        if self.spark is not None:
            try:
                return self._transform_pyspark(raw_records)
            except Exception as e:
                logger.warning(
                    f"PySpark transformation failed ({e}). Falling back to Pandas engine."
                )

        return self._transform_pandas_fallback(raw_records)

    def _transform_pyspark(
        self, raw_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Executes transformations using PySpark DataFrame operations."""
        df_spark = self.spark.createDataFrame(raw_records)

        # Standardize column naming
        columns = df_spark.columns
        if "hotels_total_arrivals" in columns:
            df_spark = df_spark.withColumnRenamed("hotels_total_arrivals", "arrivals")
        if "hotels_total_overnights" in columns:
            df_spark = df_spark.withColumnRenamed(
                "hotels_total_overnights", "overnights"
            )
        if "hotels_occupancy" in columns:
            df_spark = df_spark.withColumnRenamed("hotels_occupancy", "occupancy")
        if "turnover_total" in columns:
            df_spark = df_spark.withColumnRenamed("turnover_total", "turnover")

        # Scale receipts and turnover to actual monetary values
        if "receipts" in df_spark.columns:
            df_spark = df_spark.withColumn("receipts", col("receipts") * 1_000_000)
        else:
            df_spark = df_spark.withColumn("receipts", lit(0.0))

        if "turnover" in df_spark.columns:
            df_spark = df_spark.withColumn("turnover", col("turnover") * 1_000)
        else:
            df_spark = df_spark.withColumn("turnover", lit(0.0))

        # Convert back to python dicts
        transformed_dicts = [row.asDict() for row in df_spark.collect()]
        logger.info(
            f"PySpark DataFrame transformation completed successfully: {len(transformed_dicts)} rows."
        )
        return transformed_dicts

    def _transform_pandas_fallback(
        self, raw_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fallback transformation using Pandas DataFrame."""
        df = pd.DataFrame(raw_records)

        rename_map = {
            "hotels_total_arrivals": "arrivals",
            "hotels_total_overnights": "overnights",
            "hotels_occupancy": "occupancy",
            "turnover_total": "turnover",
        }
        df = df.rename(columns=rename_map)

        if "receipts" in df.columns:
            df["receipts"] = df["receipts"] * 1_000_000
        else:
            df["receipts"] = 0.0

        if "turnover" in df.columns:
            df["turnover"] = df["turnover"] * 1_000
        else:
            df["turnover"] = 0.0

        records = df.to_dict(orient="records")
        logger.info(f"Pandas fallback transformation completed: {len(records)} rows.")
        return records

    def stop(self) -> None:
        """Stops active PySpark SparkSession."""
        if self.spark is not None:
            try:
                self.spark.stop()
                logger.info("PySpark SparkSession stopped.")
            except Exception as e:
                logger.warning(f"Error stopping SparkSession: {e}")


def process_with_pyspark(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convenience helper to process records through PySpark processor.

    Args:
        raw_records: Input raw API records.

    Returns:
        List[Dict[str, Any]]: Transformed records.
    """
    processor = PySparkProcessor()
    try:
        return processor.transform_records(raw_records)
    finally:
        processor.stop()
