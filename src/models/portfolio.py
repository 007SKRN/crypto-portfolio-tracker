from src.utils import CoinMarketCapAPI, CoinNotFoundError, InvalidInputError, logger
from src.models.database import Session, CoinModel
from src.models import CoinData

from typing import Dict, List, Optional

class Portfolio:
    def __init__(self):
        self.api_client = CoinMarketCapAPI()
        self.session = Session()
        self._load_coins_from_db()

    def _load_coins_from_db(self):
        self.coins = {
            coin.id: {
                "name": coin.name,
                "id": coin.coin_id,
                "avg_price": coin.avg_price,
                "amount": coin.amount,
                "targets": coin.targets or []
            }
            for coin in self.session.query(CoinModel).all()
        }

    def add_coin(
        self,
        name: str,
        coin_id: str,
        avg_price: float,
        amount: float,
        targets: Optional[List[float]] = None
    ) -> int:
        if avg_price <= 0:
            raise InvalidInputError("Average price must be greater than 0")
        if amount <= 0:
            raise InvalidInputError("Amount must be greater than 0")

        name = name
        targets = targets or []
        
        coin = CoinModel(
            name=name,
            coin_id=coin_id,
            avg_price=avg_price,
            amount=amount,
            targets=targets
        )
        
        self.session.add(coin)
        self.session.commit()
        
        self.coins[coin.id] = {
            "name": name,
            "id": coin_id,
            "avg_price": avg_price,
            "amount": amount,
            "targets": targets
        }

        logger.info(f"Coin added: {name} with ID {coin_id}, average price {avg_price}, amount {amount}, targets {targets}")
        return coin.id

    def remove_coin(self, db_id: int) -> None:
        coin = self.session.query(CoinModel).get(db_id)
        if coin:
            self.session.delete(coin)
            self.session.commit()
        self.coins.pop(db_id, None)

        logger.info(f"Coin removed: {coin.name if coin else db_id}")

    def get_coin(self, db_id: int) -> Dict:
        if db_id not in self.coins:
            raise CoinNotFoundError(f"Coin with ID {db_id} not found in portfolio")
        return self.coins[db_id]

    def get_portfolio_data(self) -> List[CoinData]:
        if not self.coins:
            return []

        try:
            current_prices = self.api_client.get_current_prices(
                [coin["id"] for coin in self.coins.values()]
            )
            coins = []
            for name, data in self.coins.items():
                if data["id"] in current_prices:
                    current_price = current_prices.get(data["id"], {}).get("quote", {}).get("USD", {}).get("price", 0)
                    change_24h = current_prices.get(data["id"], {}).get("quote", {}).get("USD", {}).get("percent_change_24h", 0)
                    volume_change_24h = current_prices.get(data["id"], {}).get("quote", {}).get("USD", {}).get("volume_change_24h", 0)
                    coins.append(self._analyze_coin(name, data, current_price, change_24h, volume_change_24h))
            return coins
        except Exception as e:
            logger.error(f"Error fetching portfolio data: {e}")
            return []

    def _analyze_coin(self, db_id: int, coin_data: Dict, current_price: float, change_24h: float, volume_change_24h: float) -> Dict:
        avg_price = coin_data["avg_price"]
        amount = coin_data["amount"]
        targets = coin_data["targets"]
        name = coin_data["name"]

        investment = avg_price * amount
        current_value = current_price * amount
        profit = current_value - investment
        profit_percentage = (profit / investment) * 100

        total_investment = sum(
            self.coins[coin_id]["avg_price"] * self.coins[coin_id]["amount"]
            for coin_id in self.coins
        )
        
        portfolio_percentage = (investment / total_investment * 100) if total_investment > 0 else 0

        target_analysis = [
            {
                "price": target,
                "profit": (target - avg_price) * amount,
                "percentage": ((target - avg_price) / avg_price) * 100
            }
            for target in targets
        ]

        return {
            "db_id": db_id,
            "name": name.upper(),
            "current_price": current_price,
            "avg_price": avg_price,
            "amount": amount,
            "investment": investment,
            "current_value": current_value,
            "profit": profit,
            "profit_percentage": profit_percentage,
            "portfolio_percentage": portfolio_percentage,
            "targets": target_analysis,
            "percent_change_24h": change_24h,
            "volume_change_24h": volume_change_24h
        }