from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy_one = float("-inf")
        sell_one = 0
        buy_two = float("-inf")
        sell_two = 0

        for price in prices:
            buy_one = max(buy_one, -price)
            sell_one = max(sell_one, buy_one + price)
            buy_two = max(buy_two, sell_one - price)
            sell_two = max(sell_two, buy_two + price)

        return sell_two
