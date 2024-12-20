from config.settings import API_BASE_URL, API_KEY
from src.utils import logger

from typing import Dict, List
import requests

class CoinMarketCapAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = API_BASE_URL

    def get_current_prices(self, coin_ids: List[str]) -> Dict:
        url = f"{self.base_url}/cryptocurrency/quotes/latest"
        params = {
            "id": ",".join(coin_ids),
            "aux": "total_supply"
        }
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching prices: {e}")
            return {} 