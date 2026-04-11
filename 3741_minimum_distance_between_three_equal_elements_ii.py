from collections import defaultdict
from typing import List


class Solution:
    def minimumDistance(self, nums: List[int]) -> int:
        positions = defaultdict(list)
        best = float("inf")

        for index, value in enumerate(nums):
            positions[value].append(index)
            if len(positions[value]) >= 3:
                best = min(best, 2 * (index - positions[value][-3]))

        return -1 if best == float("inf") else best
