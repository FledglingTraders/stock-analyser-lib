import pytest
from stock_analyser_lib.repositories.stock_repo import StockRepository
from stock_analyser_lib.models.stock import Stock

@pytest.fixture
def sample_stock():
    return {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": 2000000000000
    }

def test_add_stock(db_session, sample_stock, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    StockRepository.add_stock(**sample_stock)
    stock = db_session.query(Stock).filter_by(symbol="AAPL").first()
    
    assert stock is not None
    assert stock.name == "Apple Inc."

def test_get_stock_by_symbol(db_session, sample_stock, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    # Add stock
    StockRepository.add_stock(**sample_stock)
    
    # Fetch stock
    stock = StockRepository.get_stock_by_symbol("AAPL")
    assert stock is not None
    assert stock.name == "Apple Inc."

def test_update_stock(db_session, sample_stock, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    StockRepository.add_stock(**sample_stock)
    StockRepository.update_stock("AAPL", name="Apple Corporation")
    
    stock = StockRepository.get_stock_by_symbol("AAPL")
    assert stock.name == "Apple Corporation"

def test_delete_stock(db_session, sample_stock, mocker):
    mocker.patch("stock_analyser_lib.models.base.SessionLocal", return_value=db_session)
    
    StockRepository.add_stock(**sample_stock)
    StockRepository.delete_stock("AAPL")
    
    stock = StockRepository.get_stock_by_symbol("AAPL")
    assert stock is None
