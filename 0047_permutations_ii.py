from typing import List


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        permutations: List[List[int]] = []
        current: List[int] = []
        used = [False] * len(nums)

        def backtrack() -> None:
            if len(current) == len(nums):
                permutations.append(current.copy())
                return

            for index, value in enumerate(nums):
                if used[index]:
                    continue
                if index > 0 and nums[index - 1] == value and not used[index - 1]:
                    continue
                used[index] = True
                current.append(value)
                backtrack()
                current.pop()
                used[index] = False

        backtrack()
        return permutations
