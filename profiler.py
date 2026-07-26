"""
Performance profiling module using cProfile and pstats to benchmark queries and ETL functions.
"""

import cProfile
import pstats
from io import StringIO
from typing import Any, Callable
from sqlalchemy import create_engine

from loader import transform_data
from logger import logger
from models import Base, TourismData
from queries import (
    get_cumulative_arrivals_by_region,
    get_regional_rankings_by_year,
    get_top_regions_by_arrivals,
    get_yoy_growth_analysis,
)


def create_mock_benchmark_engine():
    """Creates an in-memory SQLite engine with sample data for benchmark execution."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        from sqlalchemy.orm import sessionmaker

        Session = sessionmaker(bind=engine)
        session = Session()
        sample_records = [
            TourismData(
                geo="EL30",
                geo_label="Attiki",
                year=2022,
                arrivals=1000.0,
                receipts=5000.0,
            ),
            TourismData(
                geo="EL30",
                geo_label="Attiki",
                year=2023,
                arrivals=1500.0,
                receipts=7500.0,
            ),
            TourismData(
                geo="EL42",
                geo_label="Notio Aigaio",
                year=2022,
                arrivals=2000.0,
                receipts=10000.0,
            ),
            TourismData(
                geo="EL42",
                geo_label="Notio Aigaio",
                year=2023,
                arrivals=2500.0,
                receipts=12500.0,
            ),
        ]
        session.add_all(sample_records)
        session.commit()
        session.close()
    return engine


def profile_function(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Profiles a function execution using cProfile and prints top bottleneck functions.

    Args:
        func: Target callable to profile.
        *args: Positional arguments for the callable.
        **kwargs: Keyword arguments for the callable.

    Returns:
        Any: Return value of the callable.
    """
    profiler = cProfile.Profile()
    logger.info(f"Starting cProfile performance benchmarking for '{func.__name__}'...")

    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(15)

    logger.info(
        f"--- Performance Profile Report for {func.__name__} ---\n{stream.getvalue()}"
    )
    return result


def run_benchmarks() -> None:
    """Executes performance profiling across key analytics queries and transformations."""
    print("==================================================")
    print("      GREEK TOURISM PERFORMANCE BENCHMARKS       ")
    print("==================================================")

    engine = create_mock_benchmark_engine()

    profile_function(get_top_regions_by_arrivals, limit=10, engine=engine)
    profile_function(get_cumulative_arrivals_by_region, engine=engine)
    profile_function(get_regional_rankings_by_year, engine=engine)
    profile_function(get_yoy_growth_analysis, engine=engine)


if __name__ == "__main__":
    run_benchmarks()
