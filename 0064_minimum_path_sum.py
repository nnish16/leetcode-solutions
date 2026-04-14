from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        cols = len(grid[0])
        dp = [0] * cols

        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if r == 0 and c == 0:
                    dp[c] = value
                elif r == 0:
                    dp[c] = dp[c - 1] + value
                elif c == 0:
                    dp[c] += value
                else:
                    dp[c] = min(dp[c], dp[c - 1]) + value

        return dp[-1]
