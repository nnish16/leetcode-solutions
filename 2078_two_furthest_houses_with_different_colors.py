from typing import List


class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        left = 0
        right = len(colors) - 1

        while colors[left] == colors[-1]:
            left += 1
        while colors[right] == colors[0]:
            right -= 1

        return max(len(colors) - 1 - left, right)
