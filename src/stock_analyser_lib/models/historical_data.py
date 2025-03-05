from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from stock_analyser_lib.models.base import BaseModel  # Importing Base from base.py
from stock_analyser_lib.enums.entity import Entity  # Importing Entity from entity.py


class HistoricalData(BaseModel):
    """Represents historical stock data (OHLCV + technical indicators)."""
    __tablename__ = Entity.HISTORICAL_DATA.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), ForeignKey('stocks.symbol'))
    date = Column(Date, nullable=False)
    open = Column(DECIMAL(10, 2))
    high = Column(DECIMAL(10, 2))
    low = Column(DECIMAL(10, 2))
    close = Column(DECIMAL(10, 2))
    volume = Column(Integer)
    rsi = Column(DECIMAL(5, 2))
    macd = Column(DECIMAL(5, 3))
    sma_50 = Column(DECIMAL(10, 2))
    sma_200 = Column(DECIMAL(10, 2))
    bollinger_upper = Column(DECIMAL(10, 2))
    bollinger_lower = Column(DECIMAL(10, 2))

    stock = relationship("Stock", back_populates="historical_data")

    __table_args__ = (ForeignKeyConstraint([symbol],
                                           ['stocks.symbol']), {})

    def __repr__(self):
        return f"<HistoricalData(symbol={self.symbol}, date={self.date}, close={self.close})>"
