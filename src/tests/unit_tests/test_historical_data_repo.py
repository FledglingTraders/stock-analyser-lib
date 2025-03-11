import pytest
from datetime import datetime

from stock_analyser_lib.repositories.historical_data_repo import HistoricalDataRepository
from stock_analyser_lib.models.historical_data import HistoricalData

@pytest.fixture
def sample_historical_data():
    return {
        "symbol": "AAPL",
        "date": datetime.strptime("2021-01-01", "%Y-%m-%d").date(),
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 105,
        "volume": 1000000,
        "rsi": 70,
        "macd": 0.5,
        "sma_50": 100,
        "sma_200": 90,
        "bollinger_upper": 120,
        "bollinger_lower": 80
    }

def test_add_historical_data(db_session, sample_historical_data, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    HistoricalDataRepository.add_historical_data(**sample_historical_data)
    data = db_session.query(HistoricalData).filter_by(symbol="AAPL", date="2021-01-01").first()
    
    assert data is not None
    assert data.close == 105

def test_update_historical_data(db_session, sample_historical_data, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    HistoricalDataRepository.add_historical_data(**sample_historical_data)
    HistoricalDataRepository.update_historical_data("AAPL", "2021-01-01", close=110)
    
    data = db_session.query(HistoricalData).filter_by(symbol="AAPL", date="2021-01-01").first()
    assert data.close == 110

def test_delete_historical_data(db_session, sample_historical_data, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    HistoricalDataRepository.add_historical_data(**sample_historical_data)
    HistoricalDataRepository.delete_historical_data("AAPL", "2021-01-01")
    
    data = db_session.query(HistoricalData).filter_by(symbol="AAPL", date="2021-01-01").first()
    assert data is None
