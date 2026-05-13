from typing import List


class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        delta = [0] * (2 * limit + 2)
        pairs = len(nums) // 2

        for index in range(pairs):
            left = nums[index]
            right = nums[-1 - index]
            low = min(left, right)
            high = max(left, right)
            pair_sum = left + right

            delta[2] += 2
            delta[low + 1] -= 1
            delta[pair_sum] -= 1
            delta[pair_sum + 1] += 1
            delta[high + limit + 1] += 1

        best = float("inf")
        current = 0
        for target_sum in range(2, 2 * limit + 1):
            current += delta[target_sum]
            best = min(best, current)

        return best
