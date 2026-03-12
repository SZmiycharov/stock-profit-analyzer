import csv
import os
import random


def get_random_number_in_range(start, end):
    return random.uniform(start, end)


def write_rows_to_csv(filename, header, rows):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
