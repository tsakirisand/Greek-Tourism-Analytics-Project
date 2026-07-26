"""
SQL Query module containing window functions, rankings, YoY growth, and performance execution profiling.
"""

import functools
import time
from typing import Any, Callable, Dict, List, Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from database import get_engine
from logger import logger


def time_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to log execution time of query functions."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(f"Execution time for {func.__name__}: {duration_ms:.2f} ms")
        return result

    return wrapper


@time_execution
def get_top_regions_by_arrivals(
    limit: int = 10, engine: Optional[Engine] = None
) -> pd.DataFrame:
    """Fetches the top regions based on aggregate total arrivals.

    Args:
        limit: Number of top regions to fetch.
        engine: Optional SQLAlchemy engine override.

    Returns:
        pd.DataFrame: Dataframe with region names and aggregate arrivals.
    """
    if engine is None:
        engine = get_engine()
    if engine is None:
        return pd.DataFrame()

    query = text("""
        SELECT geo_label, SUM(arrivals) AS arrivals, SUM(receipts) AS receipts
        FROM tourism_data
        GROUP BY geo_label
        ORDER BY arrivals DESC
        LIMIT :limit
    """)

    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"limit": limit})
        return df
    except Exception as e:
        logger.error(f"Error fetching top regions by arrivals: {e}")
        return pd.DataFrame()


@time_execution
def get_cumulative_arrivals_by_region(
    engine: Optional[Engine] = None,
) -> pd.DataFrame:
    """Calculates cumulative arrivals per region over time using SQL window functions (SUM OVER).

    Args:
        engine: Optional SQLAlchemy engine override.

    Returns:
        pd.DataFrame: Dataframe with geo_label, year, arrivals, and cumulative_arrivals.
    """
    if engine is None:
        engine = get_engine()
    if engine is None:
        return pd.DataFrame()

    query = text("""
        SELECT
            geo_label,
            year,
            arrivals,
            SUM(arrivals) OVER (
                PARTITION BY geo_label
                ORDER BY year
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_arrivals
        FROM tourism_data
        ORDER BY geo_label, year
    """)

    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        logger.error(f"Error executing cumulative arrivals query: {e}")
        return pd.DataFrame()


@time_execution
def get_regional_rankings_by_year(
    engine: Optional[Engine] = None,
) -> pd.DataFrame:
    """Ranks regions per year using window functions (RANK OVER PARTITION BY).

    Args:
        engine: Optional SQLAlchemy engine override.

    Returns:
        pd.DataFrame: Dataframe containing region rankings by year.
    """
    if engine is None:
        engine = get_engine()
    if engine is None:
        return pd.DataFrame()

    query = text("""
        SELECT
            year,
            geo_label,
            arrivals,
            receipts,
            RANK() OVER (
                PARTITION BY year
                ORDER BY arrivals DESC
            ) AS arrival_rank
        FROM tourism_data
        ORDER BY year DESC, arrival_rank ASC
    """)

    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        logger.error(f"Error executing regional rankings query: {e}")
        return pd.DataFrame()


@time_execution
def get_yoy_growth_analysis(engine: Optional[Engine] = None) -> pd.DataFrame:
    """Computes Year-over-Year (YoY) arrival growth using SQL window functions (LAG OVER).

    Args:
        engine: Optional SQLAlchemy engine override.

    Returns:
        pd.DataFrame: Dataframe containing current year, previous year, and YoY growth rate.
    """
    if engine is None:
        engine = get_engine()
    if engine is None:
        return pd.DataFrame()

    query = text("""
        SELECT
            geo_label,
            year,
            arrivals,
            LAG(arrivals) OVER (
                PARTITION BY geo_label
                ORDER BY year
            ) AS prev_year_arrivals,
            ROUND(
                CAST(
                    (arrivals - LAG(arrivals) OVER (PARTITION BY geo_label ORDER BY year))
                    / NULLIF(LAG(arrivals) OVER (PARTITION BY geo_label ORDER BY year), 0) * 100
                AS NUMERIC),
            2) AS yoy_growth_pct
        FROM tourism_data
        ORDER BY geo_label, year
    """)

    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        logger.error(f"Error executing YoY growth query: {e}")
        return pd.DataFrame()


def explain_query(
    sql_query: str,
    params: Optional[Dict[str, Any]] = None,
    engine: Optional[Engine] = None,
) -> List[str]:
    """Executes EXPLAIN ANALYZE for query performance monitoring.

    Args:
        sql_query: Raw SQL query string to profile.
        params: Query execution parameters.
        engine: Optional SQLAlchemy engine override.

    Returns:
        List[str]: Query execution plan output lines.
    """
    if engine is None:
        engine = get_engine()
    if engine is None:
        return ["Database engine not available."]

    db_driver = engine.dialect.name
    explain_prefix = (
        "EXPLAIN QUERY PLAN " if db_driver == "sqlite" else "EXPLAIN ANALYZE "
    )
    full_query = text(f"{explain_prefix}{sql_query}")

    try:
        with engine.connect() as conn:
            result = conn.execute(full_query, params or {})
            lines = [str(row[0]) for row in result.fetchall()]
            logger.info(f"EXPLAIN execution plan fetched ({len(lines)} plan lines).")
            return lines
    except Exception as e:
        logger.error(f"Failed to execute EXPLAIN on query: {e}")
        return [f"Error: {e}"]


if __name__ == "__main__":
    df_top = get_top_regions_by_arrivals(5)
    print("--- Top 5 Regions ---")
    print(df_top)

    df_cum = get_cumulative_arrivals_by_region()
    print("\n--- Cumulative Arrivals Head ---")
    print(df_cum.head())

    df_rank = get_regional_rankings_by_year()
    print("\n--- Regional Rankings Head ---")
    print(df_rank.head())

    df_yoy = get_yoy_growth_analysis()
    print("\n--- YoY Growth Analysis Head ---")
    print(df_yoy.head())
