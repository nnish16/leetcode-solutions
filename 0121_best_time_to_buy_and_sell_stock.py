from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")
        best_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            best_profit = max(best_profit, price - min_price)

        return best_profit
