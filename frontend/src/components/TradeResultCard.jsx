function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

function formatTimestamp(value) {
  return new Date(value).toLocaleString();
}

export default function TradeResultCard({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="result-card">
      <h2>Optimal Trade</h2>

      <div className="result-grid">
        <div>
          <span className="label">Buy time</span>
          <strong>{formatTimestamp(result.buy_timestamp)}</strong>
        </div>

        <div>
          <span className="label">Sell time</span>
          <strong>{formatTimestamp(result.sell_timestamp)}</strong>
        </div>

        <div>
          <span className="label">Buy price</span>
          <strong>{formatCurrency(result.buy_price_amount)}</strong>
        </div>

        <div>
          <span className="label">Sell price</span>
          <strong>{formatCurrency(result.sell_price_amount)}</strong>
        </div>

        <div>
          <span className="label">Shares</span>
          <strong>{result.shares}</strong>
        </div>

        <div>
          <span className="label">Profit per share</span>
          <strong>{formatCurrency(result.profit_per_share)}</strong>
        </div>

        <div>
          <span className="label">Total profit</span>
          <strong>{formatCurrency(result.total_profit)}</strong>
        </div>

        <div>
          <span className="label">Remaining funds</span>
          <strong>{formatCurrency(result.remaining_funds)}</strong>
        </div>
      </div>
    </div>
  );
}