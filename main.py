from stock_analyser_lib.repositories.historical_data_repo import HistoricalDataRepository
from stock_analyser_lib.repositories.stock_repo import StockRepository
from stock_analyser_lib.models.stock import Stock
from stock_analyser_lib.models.historical_data import HistoricalData


# Test add_stock() method
StockRepository.add_stock(symbol="AMZN", name="Amazon.com Inc.", sector="Technology", industry="E-commerce", market_cap=2000000000000)
StockRepository.add_stock(symbol="AAPL", name="Apple Inc.", sector="Technology", industry="Consumer Electronics", market_cap=2000000000000)
StockRepository.add_stock(symbol="MSFT", name="Microsoft Corporation", sector="Technology", industry="Software", market_cap=2000000000000)
StockRepository.add_stock(symbol="GOOGL", name="Alphabet Inc.", sector="Technology", industry="Internet Services", market_cap=2000000000000)
StockRepository.add_stock(symbol="TSLA", name="Tesla Inc.", sector="Automotive", industry="Electric Vehicles", market_cap=2000000000000)

# Test bulk_upsert_historical_data() method
StockRepository.bulk_upsert_historical_data([
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "market_cap": 2000000000000},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software", "market_cap": 2000000000000},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Services", "market_cap": 2000000000000},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Automotive", "industry": "Electric Vehicles", "market_cap": 2000000000000},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Technology", "industry": "E-commerce", "market_cap": 2000000000000}
])

# Test get_stock_by_symbol() method
stock = StockRepository.get_stock_by_symbol("AAPL")
print(stock)    # Output: <Stock(symbol=AAPL, name=Apple Inc.)> (or similar)

# Test get_stock_by_sector() method
stock = StockRepository.get_stock_by_sector("Technology")
print(stock)    # Output: <Stock(symbol=AAPL, name=Apple Inc.)> (or similar)

# Test get_stock_by_industry() method
stock = StockRepository.get_stock_by_industry("Consumer Electronics")
print(stock)    # Output: <Stock(symbol=AAPL, name=Apple Inc.)> (or similar)

# Test get_all_stocks() method
stocks = StockRepository.get_all_stocks()
print(stocks)    # Output: [<Stock(symbol=AAPL, name=Apple Inc.)>, <Stock(symbol=MSFT, name=Microsoft Corporation)>] (or similar)   # noqa: E501

# Test update_stock() method

stock = StockRepository.get_stock_by_symbol("AAPL")
stock.market_cap = 3000000000000
StockRepository.update_stock("AAPL", open=777)
stock = StockRepository.get_stock_by_symbol("AAPL")
print(stock)    # Output: <Stock(symbol=AAPL, name=Apple Inc.)> (or similar)




# Test add_historical_data() method 
HistoricalDataRepository.add_historical_data(
    symbol="AAPL", date="2021-01-01", open=100, high=110, low=90, close=105, volume=1000000, rsi=70, macd=0.5,
    sma_50=100, sma_200=90, bollinger_upper=120, bollinger_lower=80
)
  
# Test bulk_upsert_historical_data() method
HistoricalDataRepository.bulk_upsert_historical_data([
    {"symbol": "AAPL", "date": "2021-01-01", "open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000000, "rsi": 70, "macd": 0.5, "sma_50": 100, "sma_200": 90, "bollinger_upper": 120, "bollinger_lower": 80},
    {"symbol": "AAPL", "date": "2021-01-02", "open": 105, "high": 115, "low": 95, "close": 110, "volume": 1200000, "rsi": 75, "macd": 0.6, "sma_50": 105, "sma_200": 95, "bollinger_upper": 125, "bollinger_lower": 85},
    {"symbol": "AAPL", "date": "2021-01-03", "open": 110, "high": 120, "low": 100, "close": 115, "volume": 1400000, "rsi": 80, "macd": 0.7, "sma_50": 110, "sma_200": 100, "bollinger_upper": 130, "bollinger_lower": 90},
    {"symbol": "AAPL", "date": "2021-01-04", "open": 115, "high": 125, "low": 105, "close": 120, "volume": 1600000, "rsi": 85, "macd": 0.8, "sma_50": 115, "sma_200": 105, "bollinger_upper": 135, "bollinger_lower": 95},
    {"symbol": "AAPL", "date": "2021-01-05", "open": 120, "high": 130, "low": 110, "close": 125, "volume": 1800000, "rsi": 90, "macd": 0.9, "sma_50": 120,"sma_200": 110, "bollinger_upper": 140, "bollinger_lower": 100}
])

# Test get_historical_data() method
historical_data = HistoricalDataRepository.get_historical_data("AAPL")
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)>, <HistoricalData(symbol=AAPL, date=2021-01-02, close=110.00)>] (or similar)   # noqa: E501

# Test get_historical_data_by_symbol() method
historical_data = HistoricalDataRepository.get_historical_data_by_symbol("AAPL")
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)>, <HistoricalData(symbol=AAPL, date=2021-01-02, close=110.00)>] (or similar)   # noqa: E501

# Test get_historical_data_by_date() method
historical_data = HistoricalDataRepository.get_historical_data_by_date("2021-01-01")
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)>] (or similar)

# Test get_historical_data_by_date_range() method
historical_data = HistoricalDataRepository.get_historical_data_by_date_range("2021-01-01", "2021-01-03")    # noqa: E501
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)>, <HistoricalData(symbol=AAPL, date=2021-01-02, close=110.00)>] (or similar)   # noqa: E501

# test get_historical_data_by_symbol_and_date() method
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date("AAPL", "2021-01-01")
print(historical_data)    # Output: <HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)> (or similar)

# Test get_historical_data_by_symbol_and_date_range() method
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date_range("AAPL", "2021-01-01", "2021-01-03")    # noqa: E501
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=105.00)>, <HistoricalData(symbol=AAPL, date=2021-01-02, close=110.00)>] (or similar)   # noqa: E501

# Test update_historical_data() method
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date("AAPL", "2021-01-01")
historical_data.close = 110
HistoricalDataRepository.update_historical_data("AAPL", "2021-01-01", close=190)
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date("AAPL", "2021-01-01")
print(historical_data)    # Output: <HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)> (or similar)

# Test delete_historical_data() method
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date("AAPL", "2021-01-01")
HistoricalDataRepository.delete_historical_data("AAPL", "2021-01-01")
historical_data = HistoricalDataRepository.get_historical_data_by_symbol_and_date("AAPL", "2021-01-01")
print(historical_data)    # Output: None

# Test get_historical_data_by_rsi() method
historical_data = HistoricalDataRepository.get_historical_data_by_rsi(70)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_macd() method
historical_data = HistoricalDataRepository.get_historical_data_by_macd( 0.5)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_sma_50() method
historical_data = HistoricalDataRepository.get_historical_data_by_sma_50(100)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_sma_200() method
historical_data = HistoricalDataRepository.get_historical_data_by_sma_200(90)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_bollinger_upper() method
historical_data = HistoricalDataRepository.get_historical_data_by_bollinger_upper(120)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_bollinger_lower() method
historical_data = HistoricalDataRepository.get_historical_data_by_bollinger_lower(80)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_volume() method
historical_data = HistoricalDataRepository.get_historical_data_by_volume(4000000)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_price() method
historical_data = HistoricalDataRepository.get_historical_data_by_price(110)
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# Test get_historical_data_by_price_range() method
historical_data = HistoricalDataRepository.get_historical_data_by_price_range(100, 110)   # noqa: E501
print(historical_data)    # Output: [<HistoricalData(symbol=AAPL, date=2021-01-01, close=110.00)>] (or similar)

# test delete_stock() method
StockRepository.delete_stock("AAPL")
stock = StockRepository.get_stock_by_symbol("AAPL")
print(stock)    # Output: None

# Delete all stocks and historical data
StockRepository.delete_stock("AMZN")
StockRepository.delete_stock("MSFT")
StockRepository.delete_stock("GOOGL")
StockRepository.delete_stock("TSLA")    # noqa: E501
historical_data = HistoricalDataRepository.get_historical_data_by_symbol("AAPL")
for data in historical_data:
    HistoricalDataRepository.delete_historical_data(data)
historical_data = HistoricalDataRepository.get_historical_data_by_symbol("AAPL")
print(historical_data)    # Output: [] (or similar)

