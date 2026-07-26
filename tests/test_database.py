"""
Unit tests for database module and queries.
"""

import os
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_database_url, get_engine
from models import Base, TourismData
from queries import (
    explain_query,
    get_cumulative_arrivals_by_region,
    get_regional_rankings_by_year,
    get_top_regions_by_arrivals,
    get_yoy_growth_analysis,
)


@pytest.fixture
def in_memory_db_engine():
    """Fixture providing an in-memory SQLite database engine initialized with schema."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(in_memory_db_engine):
    """Fixture providing an active database session for in-memory SQLite."""
    Session = sessionmaker(bind=in_memory_db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def populate_test_data(db_session):
    """Populates test data across multiple regions and years into the database."""
    records = [
        TourismData(
            geo="EL30",
            geo_label="Attiki",
            year=2022,
            arrivals=100.0,
            receipts=500.0,
        ),
        TourismData(
            geo="EL30",
            geo_label="Attiki",
            year=2023,
            arrivals=150.0,
            receipts=750.0,
        ),
        TourismData(
            geo="EL42",
            geo_label="Notio Aigaio",
            year=2022,
            arrivals=200.0,
            receipts=1000.0,
        ),
        TourismData(
            geo="EL42",
            geo_label="Notio Aigaio",
            year=2023,
            arrivals=250.0,
            receipts=1250.0,
        ),
    ]
    db_session.add_all(records)
    db_session.commit()


def test_get_database_url_default():
    """Test constructing default database URL from environment variables."""
    with patch.dict(os.environ, {}, clear=True):
        url = get_database_url()
        assert "postgresql://postgres:password@localhost:5432/greek_tourism" in url


def test_get_database_url_custom_postgres():
    """Test parsing postgres:// connection strings from cloud environment."""
    env = {"DATABASE_URL": "postgres://user:pass@host.render.com:5432/dbname"}
    with patch.dict(os.environ, env):
        url = get_database_url()
        assert url.startswith("postgresql://")


def test_get_engine():
    """Test creating SQLAlchemy engine safely."""
    engine = get_engine()
    assert engine is not None


def test_data_insertion(db_session):
    """Test data insertion into database and retrieval via session."""
    record = TourismData(
        geo="EL30",
        geo_label="Attiki",
        year=2023,
        arrivals=5000.0,
        overnights=15000.0,
        receipts=2500.0,
    )
    db_session.add(record)
    db_session.commit()

    queried = db_session.query(TourismData).filter_by(geo="EL30").first()
    assert queried is not None
    assert queried.geo_label == "Attiki"
    assert queried.arrivals == 5000.0


def test_query_top_regions(in_memory_db_engine, populate_test_data):
    """Test data retrieval with get_top_regions_by_arrivals query."""
    df = get_top_regions_by_arrivals(limit=2, engine=in_memory_db_engine)
    assert not df.empty
    assert len(df) == 2
    assert "geo_label" in df.columns
    assert df.iloc[0]["geo_label"] == "Notio Aigaio"
    assert df.iloc[0]["arrivals"] == 450.0  # 200 + 250


def test_query_cumulative_arrivals(in_memory_db_engine, populate_test_data):
    """Test data retrieval with window function cumulative arrivals query."""
    df = get_cumulative_arrivals_by_region(engine=in_memory_db_engine)
    assert not df.empty
    assert "cumulative_arrivals" in df.columns
    attiki_df = df[df["geo_label"] == "Attiki"].sort_values("year")
    assert list(attiki_df["cumulative_arrivals"]) == [100.0, 250.0]


def test_query_regional_rankings(in_memory_db_engine, populate_test_data):
    """Test data retrieval with window function regional rankings query."""
    df = get_regional_rankings_by_year(engine=in_memory_db_engine)
    assert not df.empty
    assert "arrival_rank" in df.columns
    df_2023 = df[df["year"] == 2023].sort_values("arrival_rank")
    assert df_2023.iloc[0]["geo_label"] == "Notio Aigaio"
    assert df_2023.iloc[0]["arrival_rank"] == 1


def test_query_yoy_growth(in_memory_db_engine, populate_test_data):
    """Test data retrieval with window function YoY growth query."""
    df = get_yoy_growth_analysis(engine=in_memory_db_engine)
    assert not df.empty
    attiki_2023 = df[(df["geo_label"] == "Attiki") & (df["year"] == 2023)].iloc[0]
    assert attiki_2023["prev_year_arrivals"] == 100.0
    assert attiki_2023["yoy_growth_pct"] == 50.0  # (150 - 100) / 100 * 100


def test_explain_query(in_memory_db_engine, populate_test_data):
    """Test EXPLAIN ANALYZE execution monitor on SQL queries."""
    sql = "SELECT * FROM tourism_data WHERE year = :year"
    plan = explain_query(sql, params={"year": 2023}, engine=in_memory_db_engine)
    assert isinstance(plan, list)
    assert len(plan) > 0
