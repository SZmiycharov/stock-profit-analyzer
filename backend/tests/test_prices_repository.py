from datetime import datetime, timedelta
from unittest.mock import mock_open, patch

import pytest

from backend.models.price import Price
from backend.services.prices_repository import PricesRepository
from backend.tests.utilities import generate_csv_content


class TestPricesRepository:
    def test_load_prices_parses_csv_rows(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)

        prices = [
            Price(some_timestamp, 100.50),
            Price(some_timestamp + timedelta(seconds=1), 101.25)
        ]
        csv_content = generate_csv_content(prices)

        with patch("builtins.open", mock_open(read_data=csv_content)):
            repository = PricesRepository("dummy.csv")

        assert len(repository.prices) == 2
        assert repository.prices[0].timestamp == some_timestamp
        assert repository.prices[0].amount == 100.50
        assert repository.prices[1].timestamp == some_timestamp + timedelta(seconds=1)
        assert repository.prices[1].amount == 101.25

    def test_get_prices_returns_only_requested_range(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)
        prices = [
            Price(some_timestamp, 100.50),
            Price(some_timestamp + timedelta(seconds=5), 101.25),
            Price(some_timestamp + timedelta(seconds=10), 102.00),
        ]
        csv_content = generate_csv_content(prices)

        with patch("builtins.open", mock_open(read_data=csv_content)):
            repository = PricesRepository("dummy.csv")

        result = repository.get_prices(
            some_timestamp + timedelta(seconds=2),
            some_timestamp + timedelta(seconds=6)
        )

        assert len(result) == 1
        assert result[0].timestamp == some_timestamp + timedelta(seconds=5)
        assert result[0].amount == 101.25

    def test_get_prices_returns_empty_list_when_no_prices_match(self):
        some_timestamp = datetime(2026, 3, 1, 10, 0, 0)
        prices = [
            Price(some_timestamp, 100.50),
            Price(some_timestamp + timedelta(seconds=1), 101.25),
        ]
        csv_content = generate_csv_content(prices)

        with patch("builtins.open", mock_open(read_data=csv_content)):
            repository = PricesRepository("dummy.csv")

        result = repository.get_prices(
            some_timestamp + timedelta(seconds=3),
            some_timestamp + timedelta(seconds=4),
        )

        assert result == []

    def test_get_prices_raises_when_start_is_not_before_end(self):
        prices = [
            Price(datetime(2026, 3, 1, 10, 0, 0), 100.50),
        ]
        csv_content = generate_csv_content(prices)

        with patch("builtins.open", mock_open(read_data=csv_content)):
            repository = PricesRepository("dummy.csv")

        some_timestamp = datetime(2026, 3, 1, 10, 0, 2)
        with pytest.raises(ValueError):
            repository.get_prices(
                some_timestamp,
                some_timestamp - timedelta(seconds=3),
            )

    def test_load_prices_returns_empty_list_when_csv_has_only_header(self):
        csv_content = generate_csv_content([])

        with patch("builtins.open", mock_open(read_data=csv_content)):
            repository = PricesRepository("dummy.csv")

        assert repository.prices == []
