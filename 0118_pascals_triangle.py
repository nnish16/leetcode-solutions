from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        triangle: List[List[int]] = []

        for row_index in range(numRows):
            row = [1] * (row_index + 1)
            for col in range(1, row_index):
                row[col] = triangle[row_index - 1][col - 1] + triangle[row_index - 1][col]
            triangle.append(row)

        return triangle
