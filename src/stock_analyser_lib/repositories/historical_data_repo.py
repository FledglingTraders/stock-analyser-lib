from typing import Optional, List
from datetime import date

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import joinedload

from stock_analyser_lib.models.historical_data import HistoricalData
from stock_analyser_lib.models.base import BaseModel


class HistoricalDataRepository:
    """Repository class for HistoricalData model to handle database operations."""

    @staticmethod
    def bulk_upsert_historical_data(data_list: List[dict]):
        """Performs bulk Upsert (Insert or Update) on historical data."""
        with BaseModel.get_session() as session:
            try:
                stmt = insert(HistoricalData).values(data_list)

                primary_keys = [key.name for key in inspect(HistoricalData).primary_key]

                update_keys = {key: getattr(stmt.excluded, key) for key in data_list[0].keys() if key not in primary_keys}

                stmt = stmt.on_conflict_do_update(
                    index_elements=primary_keys,  # Conflict condition
                    set_=update_keys
                )

                session.execute(stmt)
                BaseModel.logger.info("Bulk historical_data insert successful.")
            except IntegrityError:
                BaseModel.logger.error("Bulk historical_data insert failed. Falling back to individual inserts.")
                session.rollback()
                # If bulk insert fails, fall back to inserting records one by one using merge()
                for data in data_list:
                    HistoricalDataRepository.add_historical_data(**data)

    @staticmethod
    def add_historical_data(
            symbol: str, date: date, open: float,
            high: float, low: float, close: float,
            volume: int, rsi: Optional[float] = None,
            macd: Optional[float] = None, sma_50: Optional[float] = None,
            sma_200: Optional[float] = None, bollinger_upper: Optional[float] = None,
            bollinger_lower: Optional[float] = None):

        """Adds a new historical data entry."""
        with BaseModel.get_session() as session:
            historical_data = HistoricalData(
                symbol=symbol, date=date, open=open, high=high, low=low, close=close, volume=volume,
                rsi=rsi, macd=macd, sma_50=sma_50, sma_200=sma_200,
                bollinger_upper=bollinger_upper, bollinger_lower=bollinger_lower
            )
            session.merge(historical_data)
            BaseModel.logger.info(f"Historical data for {symbol} on {date} added successfully.")

    @staticmethod
    def update_historical_data(symbol: str, date: str, **kwargs):
        """Updates an existing historical data record.

        Args:
            symbol (str): The stock symbol.
            date (str): The date of the historical data to update.
            **kwargs: Key-value pairs of fields to update (e.g., close=110.0).
        """
        with BaseModel.get_session() as session:
            try:
                # Find the record to update
                historical_data = session.query(HistoricalData).filter_by(symbol=symbol, date=date).first()

                if historical_data:
                    # Update the fields dynamically
                    for key, value in kwargs.items():
                        if hasattr(historical_data, key):
                            setattr(historical_data, key, value)
                    BaseModel.logger.info(f"Historical data for {symbol} on {date} updated successfully.")
                else:
                    BaseModel.logger.warning(f"No historical data found for {symbol} on {date}.")
            except IntegrityError as e:
                session.rollback()
                BaseModel.logger.error(f"Failed to update historical data for {symbol} on {date}: {e}")

    @staticmethod
    def get_historical_data(symbol: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[HistoricalData]:
        """Retrieves historical data for a stock within an optional date range."""
        with BaseModel.get_session() as session:
            query = session.query(HistoricalData).filter_by(symbol=symbol)
            if start_date:
                query = query.filter(HistoricalData.date >= start_date)
            if end_date:
                query = query.filter(HistoricalData.date <= end_date)
            return query.all()

    @staticmethod
    def get_historical_data_by_symbol(symbol: str) -> List[HistoricalData]:
        """Fetch historical data by stock symbol."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(symbol=symbol).all()
            return data

    @staticmethod
    def get_historical_data_by_date(date: date) -> List[HistoricalData]:
        """Fetch historical data by specific date."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(date=date).all()
            return data

    @staticmethod
    def get_historical_data_by_date_range(start_date: date, end_date: date) -> List[HistoricalData]:
        """Fetch historical data within a date range."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter(HistoricalData.date.between(start_date, end_date)).all()
            return data

    @staticmethod
    def get_historical_data_by_symbol_and_date(symbol: str, date: date) -> Optional[HistoricalData]:
        """Fetch historical data by stock symbol and date."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(symbol=symbol, date=date).first()
            return data

    @staticmethod
    def get_historical_data_by_symbol_and_date_range(symbol: str, start_date: date, end_date: date) -> List[HistoricalData]:
        """Fetch historical data by stock symbol within a date range."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter(HistoricalData.symbol == symbol, HistoricalData.date.between(start_date, end_date)).all()
            return data

    @staticmethod
    def delete_historical_data(symbol: str, date: date):
        """Deletes historical data for a specific stock and date."""
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(symbol=symbol, date=date).first()
            if data:
                session.delete(data)

    # RSI-related methods
    @staticmethod
    def get_historical_data_by_rsi(rsi: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(rsi=rsi).all()
            return data

    # MACD-related methods
    @staticmethod
    def get_historical_data_by_macd(macd: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(macd=macd).all()
            return data

    # SMA-related methods
    @staticmethod
    def get_historical_data_by_sma_50(sma_50: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(sma_50=sma_50).all()
            return data

    @staticmethod
    def get_historical_data_by_sma_200(sma_200: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(sma_200=sma_200).all()
            return data

    # Bollinger Bands-related methods
    @staticmethod
    def get_historical_data_by_bollinger_upper(bollinger_upper: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(bollinger_upper=bollinger_upper).all()
            return data

    @staticmethod
    def get_historical_data_by_bollinger_lower(bollinger_lower: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(bollinger_lower=bollinger_lower).all()
            return data

    # Volume-related methods
    @staticmethod
    def get_historical_data_by_volume(volume: int) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(volume=volume).all()
            return data

    # Price-related methods
    @staticmethod
    def get_historical_data_by_price(price: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter_by(close=price).all()
            return data

    @staticmethod
    def get_historical_data_by_price_range(min_price: float, max_price: float) -> List[HistoricalData]:
        with BaseModel.get_session() as session:
            data = session.query(HistoricalData).filter(HistoricalData.close.between(min_price, max_price)).all()
            return data
