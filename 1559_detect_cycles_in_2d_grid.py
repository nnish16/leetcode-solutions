from typing import List


class Solution:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        rows = len(grid)
        cols = len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def dfs(row: int, col: int, parent_row: int, parent_col: int, char: str) -> bool:
            if visited[row][col]:
                return True

            visited[row][col] = True

            for d_row, d_col in directions:
                next_row = row + d_row
                next_col = col + d_col
                if not (0 <= next_row < rows and 0 <= next_col < cols):
                    continue
                if grid[next_row][next_col] != char:
                    continue
                if next_row == parent_row and next_col == parent_col:
                    continue
                if visited[next_row][next_col] or dfs(next_row, next_col, row, col, char):
                    return True

            return False

        for row in range(rows):
            for col in range(cols):
                if not visited[row][col] and dfs(row, col, -1, -1, grid[row][col]):
                    return True

        return False
