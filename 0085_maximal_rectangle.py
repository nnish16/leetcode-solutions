from typing import List


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        cols = len(matrix[0])
        heights = [0] * cols
        best = 0

        for row in matrix:
            for col in range(cols):
                if row[col] == "1":
                    heights[col] += 1
                else:
                    heights[col] = 0
            best = max(best, self._largest_rectangle_area(heights))

        return best

    def _largest_rectangle_area(self, heights: List[int]) -> int:
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
