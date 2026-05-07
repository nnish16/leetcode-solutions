from typing import List


class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
        suffix_min = [0] * (n + 1)
        suffix_min[n] = float("inf")

        for i in range(n - 1, -1, -1):
            suffix_min[i] = min(nums[i], suffix_min[i + 1])

        ans = [0] * n
        prefix_max = float("-inf")
        block_start = 0
        block_max = float("-inf")

        for i, value in enumerate(nums):
            prefix_max = max(prefix_max, value)
            block_max = max(block_max, value)

            if i == n - 1 or prefix_max <= suffix_min[i + 1]:
                ans[block_start:i + 1] = [block_max] * (i - block_start + 1)
                block_start = i + 1
                block_max = float("-inf")

        return ans
