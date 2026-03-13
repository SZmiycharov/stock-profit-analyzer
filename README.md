# Stock Profit Analyzer
![CI](https://github.com/SZmiycharov/stock-profit-analyzer/actions/workflows/ci.yml/badge.svg)

A production‑oriented full‑stack web application that calculates the
**most profitable buy and sell time for a stock** within a given time
range.

The user provides:

-   start timestamp
-   end timestamp
-   available funds

The system returns:

-   best buy time
-   best sell time
-   buy price
-   sell price
-   number of shares purchasable
-   profit per share
-   total profit
-   remaining funds

The backend uses an **O(n) single‑pass algorithm** over the price data.

------------------------------------------------------------------------

# Architecture

    stock-profit-analyzer
    ├── backend
    │   ├── common
    │   ├── models
    │   ├── services
    │   ├── prices_generator
    │   ├── data
    │   ├── tests
    │   └── main.py
    │   └── Dockerfile
    │
    ├── frontend
    │   ├── src
    │   │   ├── api
    │   │   ├── components
    │   │   ├── test
    │   │   ├── App.jsx
    │   │   └── main.jsx
    │   ├── nginx.conf
    │   └── Dockerfile
    │
    ├── .github
    │   └── workflows
    │       └── ci.yml
    │
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# Backend

## Stack

-   Python
-   FastAPI
-   Uvicorn
-   pytest

## Features

-   versioned REST API (`/api/v1`)
-   repository + service architecture
-   dependency injection
-   CSV‑based price dataset
-   health endpoint
-   unit tests for services and repository layer
-   validation and error handling

------------------------------------------------------------------------

# Frontend

## Stack

-   React
-   Vite
-   Vitest
-   React Testing Library

## Features

-   controlled form inputs
-   field validation
-   loading / error / empty states
-   request cancellation with AbortController
-   environment‑based API configuration
-   UI tests covering major interaction flows

------------------------------------------------------------------------

# Algorithm

The optimal trade is found using a **single‑pass O(n)** algorithm.

Logic:

1.  Track the **minimum price so far**
2.  Calculate potential profit for each new price
3.  Update the best trade if profit improves


    profit = current_price - min_price

Tie‑breaking requirement:

If multiple trades have equal profit, return the **earliest and
shortest** trade.

This is naturally satisfied because:

-   the minimum price is updated only when strictly lower
-   the best trade updates only when profit strictly increases

------------------------------------------------------------------------

# Running the Application

## Running with Docker (Recommended)

The entire system can be started using Docker Compose.

From the project root:

``` bash
docker compose up --build
```

This will start:

-   **FastAPI backend container**
-   **React frontend container served via nginx**
-   nginx proxy forwarding `/api` requests to the backend

Open the application:

Frontend:

    http://localhost:5173

Backend API docs:

    http://localhost:8000/docs

Stop containers:

``` bash
docker compose down
```

------------------------------------------------------------------------

## Running Locally (Development)

### Backend

``` bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```

Backend runs at:

    http://localhost:8000

Docs:

    http://localhost:8000/docs

Health endpoint:

    http://localhost:8000/health

### Frontend

``` bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

    http://localhost:5173

------------------------------------------------------------------------

# Environment Configuration

Frontend API URL is configured using:

    VITE_API_BASE_URL

Example development configuration:

    VITE_API_BASE_URL=http://localhost:8000/api/v1

Docker builds use:

    /api/v1

which nginx proxies to the backend container.

------------------------------------------------------------------------

# Running Tests

## Backend

    cd backend
    pytest

## Frontend

    cd frontend
    npm run test:run

Tests cover:

-   algorithm correctness
-   repository behaviour
-   API validation
-   UI validation
-   loading and error states
-   successful API interaction

------------------------------------------------------------------------

# Continuous Integration

CI is configured using **GitHub Actions**.

Workflow:

    .github/workflows/ci.yml

The pipeline runs on every push and pull request and performs:

-   dependency installation
-   FastAPI import smoke test
-   backend tests with pytest
-   frontend dependency installation
-   frontend tests with Vitest
-   frontend production build

This ensures the project remains buildable and tested automatically.

------------------------------------------------------------------------

# Example API Request

    GET /api/v1/optimal_trade

Example:

    http://localhost:8000/api/v1/optimal_trade?start_timestamp=2026-03-01T10:00:00&end_timestamp=2026-03-01T10:05:00&funds=1000

Example response:

    {
      "buy_timestamp": "2026-03-01T10:03:15",
      "sell_timestamp": "2026-03-01T10:04:28",
      "buy_price_amount": 99.29,
      "sell_price_amount": 99.84,
      "shares": 10,
      "profit_per_share": 0.55,
      "total_profit": 5.5,
      "remaining_funds": 7.1
    }

------------------------------------------------------------------------

# Production Considerations

The project is structured with production deployment in mind:

-   layered backend architecture
-   API versioning
-   environment‑based configuration
-   automated tests
-   CI pipeline
-   containerized deployment with Docker

Potential future improvements:

-   persistent database instead of CSV
-   metrics and observability
-   authentication / rate limiting
-   horizontal scaling
-   infrastructure deployment automation

------------------------------------------------------------------------

# Author

Stanislav Zmiycharov
