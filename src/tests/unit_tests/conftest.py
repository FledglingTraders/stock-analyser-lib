import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from src.models.base import Base as RealBase
from src.models.stock import Stock
from src.models.historical_data import HistoricalData

# Create a new Base for testing without schema
from sqlalchemy.orm import declarative_base

TestingBase = declarative_base(metadata=MetaData())  # No schema for SQLite

# Reflect models to use TestingBase instead of RealBase
Stock.__table__.metadata = TestingBase.metadata
HistoricalData.__table__.metadata = TestingBase.metadata

@pytest.fixture(scope="function")
def db_session():
    # Use an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables without schema
    TestingBase.metadata.create_all(bind=engine)

    # Provide a new Session for each test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
