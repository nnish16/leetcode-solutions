from typing import List


class Solution:
    def isGood(self, nums: List[int]) -> bool:
        target = max(nums)
        if len(nums) != target + 1:
            return False

        nums.sort()
        for value in range(1, target):
            if nums[value - 1] != value:
                return False

        return nums[-1] == target and nums[-2] == target
