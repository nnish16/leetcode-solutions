from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result: List[List[int]] = []
        subset: List[int] = []

        def backtrack(index: int) -> None:
            result.append(subset.copy())
            for i in range(index, len(nums)):
                if i > index and nums[i] == nums[i - 1]:
                    continue
                subset.append(nums[i])
                backtrack(i + 1)
                subset.pop()

        backtrack(0)
        return result
