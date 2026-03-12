from datetime import datetime, timedelta

from backend.prices_generator.utilities import get_random_number_in_range, write_rows_to_csv


class PricesGenerator:
    def __init__(self, start_date, time_range_seconds, base_price, filename):
        self.start_date = start_date
        self.time_range_seconds = time_range_seconds
        self.base_price = base_price
        self.filename = filename

    def generate_prices(self):
        rows = []
        row_price = self.base_price

        for i in range(self.time_range_seconds):
            row_timestamp = self.start_date + timedelta(seconds=i)

            change = get_random_number_in_range(-0.05, 0.05)
            row_price = max(1, row_price + change)

            rows.append([row_timestamp.isoformat(), round(row_price, 2)])

        write_rows_to_csv(self.filename, ["timestamp", "price"], rows)


if '__main__' == __name__:
    PricesGenerator(
        start_date=datetime(2026, 3, 1, 10, 0, 0),
        time_range_seconds=7200,
        base_price=100.0,
        filename="../data/prices.csv"
    ).generate_prices()
