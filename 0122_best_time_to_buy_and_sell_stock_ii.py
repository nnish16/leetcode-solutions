from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0

        for previous, current in zip(prices, prices[1:]):
            if current > previous:
                profit += current - previous

        return profit
