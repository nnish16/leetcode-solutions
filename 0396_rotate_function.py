from typing import List


class Solution:
    def maxRotateFunction(self, nums: List[int]) -> int:
        total = sum(nums)
        n = len(nums)
        current = sum(index * value for index, value in enumerate(nums))
        best = current

        for offset in range(1, n):
            current += total - n * nums[-offset]
            if current > best:
                best = current

        return best
