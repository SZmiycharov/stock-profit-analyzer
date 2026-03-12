import csv
from datetime import datetime

from backend.models.price import Price


class PricesRepository:
    def __init__(self, filename):
        self.filename = filename
        self.prices = self._load_prices()

    def get_prices(self, start, end):
        if start >= end:
            raise ValueError("Start time must be before end time.")

        return [price for price in self.prices if start <= price.timestamp <= end]

    def _load_prices(self):
        prices = []

        with open(self.filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                prices.append(
                    Price(timestamp=datetime.fromisoformat(row["timestamp"]), amount=float(row["amount"]))
                )

        return prices
