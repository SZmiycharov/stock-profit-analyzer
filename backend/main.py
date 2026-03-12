from datetime import datetime
from functools import lru_cache

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query

from backend.common.exceptions import InvalidTimeRangeError
from backend.services.prices_analyser import PricesAnalyser
from backend.services.prices_repository import PricesRepository

app = FastAPI()

router = APIRouter(prefix="/api/v1")


@lru_cache
def get_prices_repository():
    return PricesRepository("backend/data/prices.csv")


def get_prices_analyser():
    return PricesAnalyser()


@app.get("/health")
def health():
    return {"status": "ok"}


@router.get("/optimal_trade")
def get_optimal_trade(
        start_timestamp: datetime = Query(..., description="Start of the time slice (ISO format)"),
        end_timestamp: datetime = Query(..., description="End of the time slice (ISO format)"),
        funds: float = Query(..., gt=0, description="Available funds for buying shares"),
        prices_repository: PricesRepository = Depends(get_prices_repository),
        prices_analyser: PricesAnalyser = Depends(get_prices_analyser),
):
    try:
        prices = prices_repository.get_prices(start_timestamp, end_timestamp)

        if len(prices) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least two price points must exist in the selected range.",
            )

        trade = prices_analyser.find_best_trade(prices)

        buy_price = trade.buy_price
        sell_price = trade.sell_price
        shares = int(funds // buy_price.amount)
        cost = round(shares * buy_price.amount, 2)
        total_profit = round(shares * trade.profit_per_share, 2)
        remaining_funds = round(funds - cost, 2)

        return {
            "buy_timestamp": buy_price.timestamp.isoformat(),
            "sell_timestamp": sell_price.timestamp.isoformat(),
            "buy_price_amount": buy_price.amount,
            "sell_price_amount": sell_price.amount,
            "shares": shares,
            "profit_per_share": round(trade.profit_per_share, 2),
            "total_profit": total_profit,
            "remaining_funds": remaining_funds,
        }
    except InvalidTimeRangeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


app.include_router(router)
