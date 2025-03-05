from typing import Optional, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import joinedload

from stock_analyser_lib.models.stock import Stock
from stock_analyser_lib.models.base import BaseModel


class StockRepository:
    """Repository class for Stock model to handle database operations."""

    @staticmethod
    def bulk_upsert_historical_data(data_list: List[dict]):
        """Performs bulk Upsert (Insert or Update) on historical data."""
        with BaseModel.get_session() as session:
            try:
                stmt = insert(Stock).values(data_list)

                primary_keys = [key.name for key in inspect(Stock).primary_key]

                update_keys = {key: getattr(stmt.excluded, key) for key in data_list[0].keys() if key not in primary_keys}

                stmt = stmt.on_conflict_do_update(
                    index_elements=primary_keys,  # Conflict condition
                    set_=update_keys
                )
                session.execute(stmt)
                BaseModel.logger.info("Bulk insert successful.")
            except IntegrityError:
                BaseModel.logger.error("Bulk insert failed. Falling back to individual inserts.")
                session.rollback()
                # If bulk insert fails, fall back to inserting records one by one using merge()
                for data in data_list:
                    StockRepository.add_stock(**data)

    @staticmethod
    def add_stock(
            symbol: str,
            name: str,
            sector: Optional[str] = None,
            industry: Optional[str] = None,
            market_cap: Optional[float] = None):
        """Adds a new stock to the database."""
        with BaseModel.get_session() as session:
            stock = Stock(symbol=symbol, name=name, sector=sector, industry=industry, market_cap=market_cap)
            session.merge(stock)
            BaseModel.logger.info(f"Stock {symbol} added successfully.")

    @staticmethod
    def get_stock_by_symbol(symbol: str) -> Optional[Stock]:
        """Retrieves a stock by its symbol."""
        with BaseModel.get_session() as session:
            stock = session.query(Stock).filter_by(symbol=symbol).first()
            return stock

    @staticmethod
    def get_stock_by_sector(sector: str) -> Optional[Stock]:
        """Retrieves a stock by its symbol."""
        with BaseModel.get_session() as session:
            return session.query(Stock).filter_by(sector=sector).first()

    @staticmethod
    def get_stock_by_industry(industry: str) -> Optional[Stock]:
        """Retrieves a stock by its symbol."""
        with BaseModel.get_session() as session:
            stock = session.query(Stock).filter_by(industry=industry).first()
            return stock

    @staticmethod
    def get_all_stocks() -> List[Stock]:
        """Retrieves all stocks from the database."""
        with BaseModel.get_session() as session:
            stocks = session.query(Stock).all()
            return stocks

    @staticmethod
    def update_stock(symbol: str, **kwargs):
        """Updates an existing stock record."""
        with BaseModel.get_session() as session:
            stock = session.query(Stock).filter_by(symbol=symbol).first()
            if stock:
                for key, value in kwargs.items():
                    if hasattr(stock, key):
                        setattr(stock, key, value)

    @staticmethod
    def delete_stock(symbol: str):
        """Deletes a stock from the database."""
        with BaseModel.get_session() as session:
            stock = session.query(Stock).filter_by(symbol=symbol).first()
            if stock:
                session.delete(stock)
