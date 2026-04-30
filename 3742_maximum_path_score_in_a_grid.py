from typing import List


class Solution:
    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        rows = len(grid)
        cols = len(grid[0])
        max_cost = min(k, rows + cols - 1)
        impossible = -10**9
        prev = [[impossible] * (max_cost + 1) for _ in range(cols)]

        for row in range(rows):
            curr = [[impossible] * (max_cost + 1) for _ in range(cols)]
            for col in range(cols):
                value = grid[row][col]
                extra_cost = 1 if value else 0

                if row == 0 and col == 0:
                    if extra_cost <= max_cost:
                        curr[col][extra_cost] = value
                    continue

                if row > 0:
                    source = prev[col]
                    for cost in range(extra_cost, max_cost + 1):
                        previous_score = source[cost - extra_cost]
                        if previous_score != impossible:
                            curr[col][cost] = previous_score + value

                if col > 0:
                    source = curr[col - 1]
                    for cost in range(extra_cost, max_cost + 1):
                        previous_score = source[cost - extra_cost]
                        if previous_score != impossible:
                            curr[col][cost] = max(curr[col][cost], previous_score + value)

            prev = curr

        best = max(prev[-1])
        return best if best != impossible else -1
