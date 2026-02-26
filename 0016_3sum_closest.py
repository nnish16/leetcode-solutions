"""LeetCode 16. 3Sum Closest

Difficulty: Medium

Approach: Sort + two pointers, track closest sum
Time: O(n^2)
Space: O(1)
"""

from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        best = nums[0] + nums[1] + nums[2]

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(best - target):
                    best = s

                if s == target:
                    return s
                if s < target:
                    l += 1
                else:
                    r -= 1

        return best
