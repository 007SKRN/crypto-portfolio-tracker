from typing import TypedDict, List
from dataclasses import dataclass

class CoinData(TypedDict):
    name: str
    current_price: float
    avg_price: float
    amount: float
    investment: float
    current_value: float
    profit: float
    profit_percentage: float
    portfolio_percentage: float
    targets: List[dict]
    changes: dict
    volume: dict

@dataclass
class ColumnConfig:
    label: str
    format: str = "{:.2f}"
    width: int = 0

class TableColumns:
    NAME = ColumnConfig("Coin", "{}", 75)
    CURRENT_PRICE = ColumnConfig("Current Price", "${:.8g}", 120)
    AVG_PRICE = ColumnConfig("Avg Price", "${:.8g}", 120)
    AMOUNT = ColumnConfig("Amount", "{:.8g}", 120)
    INVESTMENT = ColumnConfig("Investment", "${:.2f}", 120)
    CURRENT_VALUE = ColumnConfig("Current Value", "${:.2f}", 120)
    PROFIT = ColumnConfig("Profit/Loss", "{}", 100)
    PORTFOLIO_PERCENTAGE = ColumnConfig("Portfolio %", "{:.2f}%", 75)
    CHANGES = ColumnConfig("Changes", "{}", 150)
    VOLUME = ColumnConfig("24H Volume", "{}", 150)
    TARGETS = ColumnConfig("Targets", "{}", 100)