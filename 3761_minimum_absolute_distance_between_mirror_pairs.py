from typing import List


class Solution:
    def minMirrorPairDistance(self, nums: List[int]) -> int:
        def reverse_number(value: int) -> int:
            reversed_value = 0
            while value > 0:
                reversed_value = reversed_value * 10 + value % 10
                value //= 10
            return reversed_value

        latest_index = {}
        best = len(nums) + 1

        for index, value in enumerate(nums):
            if value in latest_index:
                best = min(best, index - latest_index[value])

            latest_index[reverse_number(value)] = index

        return -1 if best == len(nums) + 1 else best
