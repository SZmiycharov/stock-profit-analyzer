from dataclasses import dataclass
from backend.models.price import Price


@dataclass
class TradeResult:
    buy: Price
    sell: Price
    profit_per_share: float
