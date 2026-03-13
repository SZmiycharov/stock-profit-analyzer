import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";
import { fetchOptimalTrade } from "./api/optimalTradeApi";

vi.mock("./api/optimalTradeApi", () => ({
  fetchOptimalTrade: vi.fn(),
}));

function fillValidForm() {
  fireEvent.change(screen.getByLabelText(/start timestamp/i), {
    target: { value: "2026-03-01T10:00" },
  });

  fireEvent.change(screen.getByLabelText(/end timestamp/i), {
    target: { value: "2026-03-01T10:05" },
  });

  fireEvent.change(screen.getByLabelText(/available funds/i), {
    target: { value: "1000" },
  });
}

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the initial empty state", () => {
    render(<App />);

    expect(screen.getByText(/stock profit analyzer/i)).toBeInTheDocument();
    expect(screen.getByText(/ready to analyze/i)).toBeInTheDocument();
    expect(
      screen.getByText(
        /enter a start timestamp, end timestamp, and available funds/i
      )
    ).toBeInTheDocument();
  });

  it("shows field validation errors on blur", async () => {
    const user = userEvent.setup();

    render(<App />);

    const startInput = screen.getByLabelText(/start timestamp/i);
    await user.click(startInput);
    await user.tab();

    expect(
      screen.getByText(/start timestamp is required/i)
    ).toBeInTheDocument();
  });

  it("shows invalid time range error when end is earlier than start", async () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/start timestamp/i), {
      target: { value: "2026-03-01T10:05" },
    });

    fireEvent.change(screen.getByLabelText(/end timestamp/i), {
      target: { value: "2026-03-01T10:00" },
    });

    fireEvent.blur(screen.getByLabelText(/end timestamp/i));

    expect(
      screen.getByText(/end timestamp must be later than start timestamp/i)
    ).toBeInTheDocument();
  });

  it("shows funds validation when funds are zero", async () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/funds/i), {
      target: { value: "0" },
    });

    fireEvent.blur(screen.getByLabelText(/funds/i));

    expect(
      screen.getByText(/available funds must be greater than 0/i)
    ).toBeInTheDocument();
  });

  it("keeps submit button disabled until form becomes valid", () => {
    render(<App />);

    const submitButton = screen.getByRole("button", {
      name: /find optimal trade/i,
    });

    expect(submitButton).toBeDisabled();

    fillValidForm();

    expect(submitButton).toBeEnabled();
  });

  it("submits the form and renders the trade result on success", async () => {
    fetchOptimalTrade.mockResolvedValue({
      buy_timestamp: "2026-03-01T10:00:00",
      sell_timestamp: "2026-03-01T10:05:00",
      buy_price_amount: 96.84,
      sell_price_amount: 99.39,
      shares: 10,
      profit_per_share: 2.55,
      total_profit: 25.5,
      remaining_funds: 31.6,
    });

    render(<App />);

    fillValidForm();

    const submitButton = screen.getByRole("button", {
      name: /find optimal trade/i,
    });

    expect(submitButton).toBeEnabled();

    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(fetchOptimalTrade).toHaveBeenCalledWith({
        startTimestamp: "2026-03-01T10:00:00",
        endTimestamp: "2026-03-01T10:05:00",
        funds: 1000,
      });
    });

    expect(
      await screen.findByRole("heading", { name: /^optimal trade$/i })
    ).toBeInTheDocument();

    expect(screen.getByText(/best total profit/i)).toBeInTheDocument();
    expect(screen.getAllByText("$25.50").length).toBeGreaterThan(0);
    expect(screen.getByText("10")).toBeInTheDocument();
  });

  it("shows an error banner when the API request fails", async () => {
    fetchOptimalTrade.mockRejectedValue(
      new Error("Cannot connect to backend server.")
    );

    render(<App />);

    fillValidForm();

    await userEvent.click(
      screen.getByRole("button", { name: /find optimal trade/i })
    );

    expect(
      await screen.findByRole("alert")
    ).toHaveTextContent(/cannot connect to backend server/i);
  });

  it("shows a loading banner while the request is in progress", async () => {
    let resolveRequest;

    fetchOptimalTrade.mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveRequest = resolve;
        })
    );

    render(<App />);

    fillValidForm();

    await userEvent.click(
      screen.getByRole("button", { name: /find optimal trade/i })
    );

    expect(
      screen.getByText(/calculating optimal trade/i)
    ).toBeInTheDocument();

    resolveRequest({
      buy_timestamp: "2026-03-01T10:00:00",
      sell_timestamp: "2026-03-01T10:05:00",
      buy_price_amount: 96.84,
      sell_price_amount: 99.39,
      shares: 10,
      profit_per_share: 2.55,
      total_profit: 25.5,
      remaining_funds: 31.6,
    });

    await waitFor(() => {
      expect(
        screen.queryByText(/calculating optimal trade/i)
      ).not.toBeInTheDocument();
    });
  });

  it("keeps the previous result visible when a later request fails", async () => {
    fetchOptimalTrade
      .mockResolvedValueOnce({
        buy_timestamp: "2026-03-01T10:00:00",
        sell_timestamp: "2026-03-01T10:05:00",
        buy_price_amount: 96.84,
        sell_price_amount: 99.39,
        shares: 10,
        profit_per_share: 2.55,
        total_profit: 25.5,
        remaining_funds: 31.6,
      })
      .mockRejectedValueOnce(new Error("Backend unavailable."));

    render(<App />);

    fillValidForm();

    await userEvent.click(
      screen.getByRole("button", { name: /find optimal trade/i })
    );

    expect(
      await screen.findByRole("heading", { name: /^optimal trade$/i })
    ).toBeInTheDocument();

    expect(screen.getAllByText("$25.50").length).toBeGreaterThan(0);

    fireEvent.change(screen.getByLabelText(/start timestamp/i), {
      target: { value: "2026-03-01T10:10" },
    });

    fireEvent.change(screen.getByLabelText(/end timestamp/i), {
      target: { value: "2026-03-01T10:20" },
    });

    await userEvent.click(
      screen.getByRole("button", { name: /find optimal trade/i })
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      /backend unavailable/i
    );

    expect(
      screen.getByRole("heading", { name: /^optimal trade$/i })
    ).toBeInTheDocument();

    expect(screen.getAllByText("$25.50").length).toBeGreaterThan(0);
  });
});