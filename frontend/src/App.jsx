import { useState } from "react";
import { fetchOptimalTrade } from "./api/optimalTradeApi";
import OptimalTradeForm from "./components/OptimalTradeForm";
import TradeResultCard from "./components/TradeResultCard";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(formData) {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await fetchOptimalTrade(formData);
      setResult(data);
    } catch (err) {
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
          <p>Find the most profitable buy and sell time for a stock in a given period.</p>
        </header>

        <OptimalTradeForm onSubmit={handleSubmit} loading={loading} />

        {error && <div className="error-banner">{error}</div>}

        <TradeResultCard result={result} />
      </div>
    </div>
  );
}