from dataclasses import dataclass
from backend.models.price import Price


@dataclass
class Trade:
    buy_price: Price
    sell_price: Price
    profit_per_share: float
