from backend.models.trade_result import TradeResult


class PricesAnalyser:
    @staticmethod
    def find_best_trade(prices):
        if len(prices) < 2:
            raise ValueError("At least two prices required")

        min_price = prices[0]
        best_buy = None
        best_sell = None
        best_profit = None

        for current_price in prices[1:]:
            profit_when_selling_at_current_price = current_price.amount - min_price.amount

            # we update best trade only when strictly better than previous best, as we want earliest and shortest
            if best_profit is None or profit_when_selling_at_current_price > best_profit:
                best_buy = min_price
                best_sell = current_price
                best_profit = profit_when_selling_at_current_price

            if current_price.amount < min_price.amount:
                min_price = current_price

        return TradeResult(buy=best_buy, sell=best_sell, profit_per_share=best_profit)
