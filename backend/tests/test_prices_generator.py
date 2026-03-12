from datetime import datetime
from unittest.mock import patch

from backend.prices_generator.prices_generator import PricesGenerator
from backend.prices_generator import prices_generator


class TestPricesGenerator:

    def setup_method(self):
        self.start_date = datetime(2026, 3, 1, 10, 0, 0)
        self.filename = "dummy.csv"
        self.base_price = 100.0

    def create_generator(self, seconds):
        return PricesGenerator(
            start_date=self.start_date,
            time_range_seconds=seconds,
            base_price=self.base_price,
            filename=self.filename,
        )

    def test_generate_prices_calls_writer_with_rows(self):
        generator = self.create_generator(3)

        with patch.object(prices_generator, "get_random_number_in_range", side_effect=[0.01, -0.02, 0.03]), \
                patch.object(prices_generator, "write_rows_to_csv") as write_mock:
            generator.generate_prices()

        write_mock.assert_called_once()

        filename, header, rows = write_mock.call_args[0]

        assert filename == self.filename
        assert header == ["timestamp", "price"]
        assert len(rows) == 3

    def test_generate_prices_generates_correct_timestamps(self):
        generator = self.create_generator(3)

        with patch.object(prices_generator, "get_random_number_in_range", return_value=0.0), \
                patch.object(prices_generator, "write_rows_to_csv") as write_mock:
            generator.generate_prices()

        rows = write_mock.call_args[0][2]

        assert rows[0][0] == "2026-03-01T10:00:00"
        assert rows[1][0] == "2026-03-01T10:00:01"
        assert rows[2][0] == "2026-03-01T10:00:02"

    def test_generate_prices_never_below_one(self):
        generator = self.create_generator(3)
        generator.base_price = 2.0

        with patch.object(prices_generator, "get_random_number_in_range", return_value=-1000.0), \
                patch.object(prices_generator, "write_rows_to_csv") as write_mock:
            generator.generate_prices()

        rows = write_mock.call_args[0][2]
        prices = [row[1] for row in rows]

        assert prices == [1, 1, 1]

    def test_generate_prices_zero_duration(self):
        generator = self.create_generator(0)

        with patch.object(prices_generator, "write_rows_to_csv") as write_mock:
            generator.generate_prices()

        write_mock.assert_called_once_with(self.filename, ["timestamp", "price"], [])

    def test_generate_prices_accumulates_changes(self):
        generator = self.create_generator(3)

        with patch.object(prices_generator, "get_random_number_in_range", side_effect=[1.0, 1.0, 1.0]), \
                patch.object(prices_generator, "write_rows_to_csv") as write_mock:
            generator.generate_prices()

        rows = write_mock.call_args[0][2]
        prices = [row[1] for row in rows]

        assert prices == [101.0, 102.0, 103.0]
