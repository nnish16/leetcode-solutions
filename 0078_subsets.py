from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = [[]]

        for num in nums:
            result += [subset + [num] for subset in result]

        return result
