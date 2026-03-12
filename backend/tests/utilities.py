def generate_csv_content(prices):
    lines = ["timestamp,amount"]

    for price in prices:
        lines.append(f"{price.timestamp.isoformat()},{price.amount}")

    return "\n".join(lines) + "\n"
