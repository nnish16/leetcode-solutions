from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        stack: List[tuple[int, int]] = []

        for index, height in enumerate(heights):
            start = index
            while stack and stack[-1][1] > height:
                start_index, popped_height = stack.pop()
                max_area = max(max_area, popped_height * (index - start_index))
                start = start_index
            stack.append((start, height))

        total_bars = len(heights)
        for start_index, height in stack:
            max_area = max(max_area, height * (total_bars - start_index))

        return max_area
