import { useState } from "react";
import { fetchOptimalTrade } from "./api/optimalTradeApi";
import OptimalTradeForm from "./components/OptimalTradeForm";
import TradeResultCard from "./components/TradeResultCard";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  async function handleSubmit(formData) {
    setLoading(true);
    setError("");
    setHasSubmitted(true);

    try {
      const data = await fetchOptimalTrade(formData);
      setResult(data);
    } catch (err) {
      if (err.name === "AbortError") {
        return;
      }

      setError(err.message || "Unexpected error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="container">
        <header className="hero">
          <h1>Stock Profit Analyzer</h1>
          <p>
            Find the most profitable buy and sell time for a stock in a given
            period.
          </p>
        </header>

        <OptimalTradeForm onSubmit={handleSubmit} loading={loading} />

        {loading && (
          <div className="info-banner" aria-live="polite">
            Calculating optimal trade...
          </div>
        )}

        {error && (
          <div className="error-banner" role="alert">
            {error}
          </div>
        )}

        {!hasSubmitted && !result && !loading && !error && (
          <div className="empty-state">
            <h2>Ready to analyze</h2>
            <p>
              Enter a start timestamp, end timestamp, and available funds to
              calculate the best possible trade.
            </p>
          </div>
        )}

        {result && <TradeResultCard result={result} />}
      </div>
    </div>
  );
}