from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        cols = len(obstacleGrid[0])
        dp = [0] * cols
        dp[0] = 1

        for row in obstacleGrid:
            for col, cell in enumerate(row):
                if cell == 1:
                    dp[col] = 0
                elif col > 0:
                    dp[col] += dp[col - 1]

        return dp[-1]
