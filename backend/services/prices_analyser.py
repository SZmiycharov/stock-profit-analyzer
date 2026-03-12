from backend.models.trade import Trade


class PricesAnalyser:
    @staticmethod
    def find_best_trade(prices):
        if len(prices) < 2:
            raise ValueError("At least two prices required")

        min_price = prices[0]
        best_buy_price = None
        best_sell_price = None
        best_profit = None

        for current_price in prices[1:]:
            profit_when_selling_at_current_price = current_price.amount - min_price.amount

            # we update best trade only when strictly better than previous best, as we want earliest and shortest
            if best_profit is None or profit_when_selling_at_current_price > best_profit:
                best_buy_price = min_price
                best_sell_price = current_price
                best_profit = profit_when_selling_at_current_price

            if current_price.amount < min_price.amount:
                min_price = current_price

        return Trade(buy_price=best_buy_price, sell_price=best_sell_price, profit_per_share=best_profit)
