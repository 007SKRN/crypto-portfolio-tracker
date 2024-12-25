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
    NAME = ColumnConfig("Coin", "{}", 50)
    CURRENT_PRICE = ColumnConfig("Current Price", "${:.8g}", 75)
    AVG_PRICE = ColumnConfig("Avg Price", "${:.8g}", 75)
    AMOUNT = ColumnConfig("Amount", "{:.8g}", 75)
    INVESTMENT = ColumnConfig("Investment", "${:.2f}", 75)
    CURRENT_VALUE = ColumnConfig("Current Value", "${:.2f}", 75)
    PROFIT = ColumnConfig("Profit/Loss", "{}", 75)
    PORTFOLIO_PERCENTAGE = ColumnConfig("Portfolio %", "{:.2f}%", 50)
    CHANGES = ColumnConfig("Changes", "{}", 100)
    VOLUME = ColumnConfig("24H Volume", "{}", 100)
    TARGETS = ColumnConfig("Targets", "{}", 100)
    ACTIONS = ColumnConfig("Actions", "{}", 100)