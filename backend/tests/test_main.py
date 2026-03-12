from datetime import datetime, timedelta
from unittest.mock import Mock

from fastapi.testclient import TestClient

from backend.common.exceptions import InvalidTimeRangeError
from backend.main import app, get_prices_analyser, get_prices_repository
from backend.models.price import Price
from backend.models.trade import Trade


class TestMain:
    def setup_method(self):
        self.client = TestClient(app)
        self.optimal_trade_url = "/api/v1/optimal_trade"
        self.repository_mock = Mock()
        self.analyser_mock = Mock()

        app.dependency_overrides = {
            get_prices_repository: lambda: self.repository_mock,
            get_prices_analyser: lambda: self.analyser_mock,
        }

    def teardown_method(self):
        app.dependency_overrides = {}

    def test_health_returns_ok(self):
        response = self.client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_optimal_trade_returns_expected_response(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)
        another_timestamp = some_timestamp + timedelta(seconds=1)

        self.repository_mock.get_prices.return_value = [
            Price(timestamp=some_timestamp, amount=100.0),
            Price(timestamp=another_timestamp, amount=105.0),
        ]

        self.analyser_mock.find_best_trade.return_value = Trade(
            buy_price=Price(timestamp=some_timestamp, amount=100.0),
            sell_price=Price(timestamp=another_timestamp, amount=105.0),
            profit_per_share=5.0,
        )

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "buy_timestamp": "2026-03-01T10:00:00",
            "sell_timestamp": "2026-03-01T10:00:01",
            "buy_price_amount": 100.0,
            "sell_price_amount": 105.0,
            "shares": 10,
            "profit_per_share": 5.0,
            "total_profit": 50.0,
            "remaining_funds": 0.0,
        }

    def test_optimal_trade_returns_400_when_less_than_two_prices_exist(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        self.repository_mock.get_prices.return_value = [
            Price(timestamp=some_timestamp, amount=100.0),
        ]

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "At least two price points must exist in the selected range."
        }

    def test_optimal_trade_returns_400_when_repository_raises_invalid_time_range_error(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 10)
        earlier_timestamp = some_timestamp - timedelta(seconds=10)

        self.repository_mock.get_prices.side_effect = InvalidTimeRangeError(
            "Start timestamp must be before end timestamp."
        )

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": earlier_timestamp.isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Start timestamp must be before end timestamp."
        }

    def test_optimal_trade_returns_400_when_repository_raises_value_error(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)
        another_timestamp = some_timestamp + timedelta(seconds=10)

        self.repository_mock.get_prices.side_effect = ValueError(
            "Something went wrong while reading prices."
        )

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": another_timestamp.isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "Something went wrong while reading prices."
        }

    def test_optimal_trade_returns_422_when_start_timestamp_is_missing(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_end_timestamp_is_missing(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_funds_is_missing(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_start_timestamp_is_invalid(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": "not-a-date",
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": 1000,
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_end_timestamp_is_invalid(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": "not-a-date",
                "funds": 1000,
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_funds_is_not_a_number(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": "abc",
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_funds_is_zero(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": 0,
            },
        )

        assert response.status_code == 422

    def test_optimal_trade_returns_422_when_funds_is_negative(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        response = self.client.get(
            self.optimal_trade_url,
            params={
                "start_timestamp": some_timestamp.isoformat(),
                "end_timestamp": (some_timestamp + timedelta(seconds=10)).isoformat(),
                "funds": -100,
            },
        )

        assert response.status_code == 422
