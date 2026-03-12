from dataclasses import dataclass
from datetime import datetime


@dataclass
class Price:
    timestamp: datetime
    amount: float
