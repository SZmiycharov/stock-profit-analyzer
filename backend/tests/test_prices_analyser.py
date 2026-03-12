from datetime import datetime, timedelta

import pytest

from backend.models.price import Price
from backend.services.prices_analyser import PricesAnalyser


class TestPricesAnalyser:
    def setup_method(self):
        self.analyzer = PricesAnalyser()
        self.start_time = datetime(2026, 3, 1, 10, 0, 0)

    def create_price(self, seconds_offset, amount):
        return Price(
            timestamp=self.start_time + timedelta(seconds=seconds_offset),
            amount=amount,
        )

    def test_find_best_trade_returns_most_profitable_trade(self):
        prices = [
            self.create_price(0, 10),
            self.create_price(1, 7),
            self.create_price(2, 12),
            self.create_price(3, 9),
        ]

        result = self.analyzer.find_best_trade(prices)

        assert result.buy.amount == 7
        assert result.sell.amount == 12
        assert result.profit_per_share == 5

    def test_find_best_trade_returns_earliest_when_profit_is_equal(self):
        prices = [
            self.create_price(0, 5),
            self.create_price(1, 10),
            self.create_price(2, 5),
            self.create_price(3, 10),
        ]

        result = self.analyzer.find_best_trade(prices)

        assert result.buy.timestamp == self.create_price(0, 5).timestamp
        assert result.sell.timestamp == self.create_price(1, 10).timestamp
        assert result.profit_per_share == 5

    def test_find_best_trade_returns_shortest_when_profit_and_buy_time_are_equal(self):
        prices = [
            self.create_price(0, 5),
            self.create_price(1, 10),
            self.create_price(2, 9),
            self.create_price(3, 10),
        ]

        result = self.analyzer.find_best_trade(prices)

        assert result.buy.timestamp == self.create_price(0, 5).timestamp
        assert result.sell.timestamp == self.create_price(1, 10).timestamp
        assert result.profit_per_share == 5

    def test_find_best_trade_works_when_prices_only_fall(self):
        prices = [
            self.create_price(0, 10),
            self.create_price(1, 9),
            self.create_price(2, 8),
            self.create_price(3, 7),
        ]

        result = self.analyzer.find_best_trade(prices)

        assert result.buy.amount == 10
        assert result.sell.amount == 9
        assert result.profit_per_share == -1

    def test_find_best_trade_raises_when_less_than_two_prices(self):
        prices = [self.create_price(0, 10)]

        with pytest.raises(ValueError):
            self.analyzer.find_best_trade(prices)
