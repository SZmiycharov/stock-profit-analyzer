import { useMemo, useState } from "react";

function toBackendTimestamp(value) {
  return `${value}:00`;
}

function validateForm(form) {
  const errors = {};

  if (!form.startTimestamp) {
    errors.startTimestamp = "Start timestamp is required.";
  }

  if (!form.endTimestamp) {
    errors.endTimestamp = "End timestamp is required.";
  }

  if (!form.funds) {
    errors.funds = "Available funds is required.";
  } else if (Number.isNaN(Number(form.funds))) {
    errors.funds = "Available funds must be a valid number.";
  } else if (Number(form.funds) <= 0) {
    errors.funds = "Available funds must be greater than 0.";
  }

  if (
    form.startTimestamp &&
    form.endTimestamp &&
    new Date(form.startTimestamp) >= new Date(form.endTimestamp)
  ) {
    errors.endTimestamp = "End timestamp must be later than start timestamp.";
  }

  return errors;
}

function FieldError({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="field-error" role="alert">
      {message}
    </div>
  );
}

export default function OptimalTradeForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    startTimestamp: "",
    endTimestamp: "",
    funds: "",
  });

  const [touched, setTouched] = useState({
    startTimestamp: false,
    endTimestamp: false,
    funds: false,
  });

  const errors = useMemo(() => validateForm(form), [form]);

  const isFormValid = Object.keys(errors).length === 0;

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function handleBlur(event) {
    const { name } = event.target;

    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    setTouched({
      startTimestamp: true,
      endTimestamp: true,
      funds: true,
    });

    if (!isFormValid) {
      return;
    }

    onSubmit({
      startTimestamp: toBackendTimestamp(form.startTimestamp),
      endTimestamp: toBackendTimestamp(form.endTimestamp),
      funds: Number(form.funds),
    });
  }

  function getInputClassName(fieldName) {
    const hasError = touched[fieldName] && errors[fieldName];
    return hasError ? "input-error" : "";
  }

  return (
    <form onSubmit={handleSubmit} className="trade-form" noValidate>
      <div className="form-group">
        <label htmlFor="startTimestamp">Start timestamp</label>
        <input
          id="startTimestamp"
          name="startTimestamp"
          type="datetime-local"
          value={form.startTimestamp}
          onChange={handleChange}
          onBlur={handleBlur}
          disabled={loading}
          className={getInputClassName("startTimestamp")}
          aria-invalid={Boolean(touched.startTimestamp && errors.startTimestamp)}
          aria-describedby={
            touched.startTimestamp && errors.startTimestamp
              ? "startTimestamp-error"
              : undefined
          }
        />
        <div className="field-hint">Select the beginning of the analysis period.</div>
        {touched.startTimestamp && errors.startTimestamp && (
          <div id="startTimestamp-error">
            <FieldError message={errors.startTimestamp} />
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="endTimestamp">End timestamp</label>
        <input
          id="endTimestamp"
          name="endTimestamp"
          type="datetime-local"
          value={form.endTimestamp}
          onChange={handleChange}
          onBlur={handleBlur}
          disabled={loading}
          className={getInputClassName("endTimestamp")}
          aria-invalid={Boolean(touched.endTimestamp && errors.endTimestamp)}
          aria-describedby={
            touched.endTimestamp && errors.endTimestamp
              ? "endTimestamp-error"
              : undefined
          }
        />
        <div className="field-hint">Select the end of the analysis period.</div>
        {touched.endTimestamp && errors.endTimestamp && (
          <div id="endTimestamp-error">
            <FieldError message={errors.endTimestamp} />
          </div>
        )}
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
          onBlur={handleBlur}
          disabled={loading}
          className={getInputClassName("funds")}
          aria-invalid={Boolean(touched.funds && errors.funds)}
          aria-describedby={touched.funds && errors.funds ? "funds-error" : undefined}
        />
        <div className="field-hint">
          Enter the amount available for purchasing shares.
        </div>
        {touched.funds && errors.funds && (
          <div id="funds-error">
            <FieldError message={errors.funds} />
          </div>
        )}
      </div>

      <button type="submit" disabled={loading || !isFormValid}>
        {loading ? "Calculating..." : "Find Optimal Trade"}
      </button>
    </form>
  );
}