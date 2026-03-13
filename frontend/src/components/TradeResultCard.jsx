function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function formatTimestamp(value) {
  return new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date(value));
}

function ResultItem({ label, value, emphasize = false }) {
  return (
    <div className={`result-item ${emphasize ? "result-item-emphasize" : ""}`}>
      <span className="label">{label}</span>
      <strong className="value">{value}</strong>
    </div>
  );
}

export default function TradeResultCard({ result }) {
  if (!result) {
    return null;
  }

  return (
    <section className="result-card" aria-labelledby="optimal-trade-title">
      <div className="result-card-header">
        <div>
          <p className="result-card-kicker">Analysis result</p>
          <h2 id="optimal-trade-title">Optimal Trade</h2>
        </div>

        <div className="profit-summary">
          <span className="profit-summary-label">Best total profit</span>
          <strong className="profit-summary-value">
            {formatCurrency(result.total_profit)}
          </strong>
        </div>
      </div>

      <div className="result-sections">
        <section className="result-section">
          <h3>Trade timing</h3>
          <div className="result-grid">
            <ResultItem
              label="Buy time"
              value={formatTimestamp(result.buy_timestamp)}
            />
            <ResultItem
              label="Sell time"
              value={formatTimestamp(result.sell_timestamp)}
            />
          </div>
        </section>

        <section className="result-section">
          <h3>Prices</h3>
          <div className="result-grid">
            <ResultItem
              label="Buy price"
              value={formatCurrency(result.buy_price_amount)}
            />
            <ResultItem
              label="Sell price"
              value={formatCurrency(result.sell_price_amount)}
            />
            <ResultItem
              label="Profit per share"
              value={formatCurrency(result.profit_per_share)}
            />
          </div>
        </section>

        <section className="result-section">
          <h3>Investment summary</h3>
          <div className="result-grid">
            <ResultItem label="Shares" value={result.shares} />
            <ResultItem
              label="Remaining funds"
              value={formatCurrency(result.remaining_funds)}
            />
            <ResultItem
              label="Total profit"
              value={formatCurrency(result.total_profit)}
              emphasize
            />
          </div>
        </section>
      </div>
    </section>
  );
}