const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

let currentController = null;

export async function fetchOptimalTrade({
  startTimestamp,
  endTimestamp,
  funds,
}) {
  if (currentController) {
    currentController.abort();
  }

  const controller = new AbortController();
  currentController = controller;

  const params = new URLSearchParams({
    start_timestamp: startTimestamp,
    end_timestamp: endTimestamp,
    funds: String(funds),
  });

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/optimal_trade?${params.toString()}`,
      {
        signal: controller.signal,
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const message =
        data?.detail ||
        data?.message ||
        "Something went wrong while fetching the optimal trade.";

      throw new Error(message);
    }

    return data;
  } finally {
    if (currentController === controller) {
      currentController = null;
    }
  }
}