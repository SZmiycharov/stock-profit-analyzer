import { useState } from "react";

export default function OptimalTradeForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    startTimestamp: "",
    endTimestamp: "",
    funds: "",
  });

  const [validationError, setValidationError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    setValidationError("");

    if (!form.startTimestamp || !form.endTimestamp || !form.funds) {
      setValidationError("All fields are required.");
      return;
    }

    if (Number(form.funds) <= 0) {
      setValidationError("Funds must be greater than 0.");
      return;
    }

    if (new Date(form.startTimestamp) >= new Date(form.endTimestamp)) {
      setValidationError("Start timestamp must be earlier than end timestamp.");
      return;
    }

    onSubmit({
      startTimestamp: form.startTimestamp,
      endTimestamp: form.endTimestamp,
      funds: Number(form.funds),
    });
  }

  return (
    <form onSubmit={handleSubmit} className="trade-form">
      <div className="form-group">
        <label htmlFor="startTimestamp">Start timestamp</label>
        <input
          id="startTimestamp"
          name="startTimestamp"
          type="datetime-local"
          value={form.startTimestamp}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="endTimestamp">End timestamp</label>
        <input
          id="endTimestamp"
          name="endTimestamp"
          type="datetime-local"
          value={form.endTimestamp}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="funds">Available funds</label>
        <input
          id="funds"
          name="funds"
          type="number"
          min="0"
          step="0.01"
          placeholder="1000"
          value={form.funds}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      {validationError && <div className="error-message">{validationError}</div>}

      <button type="submit" disabled={loading}>
        {loading ? "Calculating..." : "Find Optimal Trade"}
      </button>
    </form>
  );
}