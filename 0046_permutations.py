from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
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
                used[index] = True
                current.append(value)
                backtrack()
                current.pop()
                used[index] = False

        backtrack()
        return permutations
