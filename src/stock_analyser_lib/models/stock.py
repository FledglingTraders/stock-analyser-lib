from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from stock_analyser_lib.models.base import BaseModel
from stock_analyser_lib.enums.entity import Entity  # Importing Entity from entity.py


class Stock(BaseModel):
    """Represents a stock (company) in the market."""
    __tablename__ = Entity.STOCK.value

    symbol = Column(String(10), primary_key=True, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(255))
    market_cap = Column(DECIMAL(20, 2))

    historical_data = relationship("HistoricalData", back_populates="stock")

    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, name={self.name})>"
