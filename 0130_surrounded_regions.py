from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return

        rows = len(board)
        cols = len(board[0])
        stack = []

        def mark(row: int, col: int) -> None:
            if board[row][col] == "O":
                board[row][col] = "S"
                stack.append((row, col))

        for row in range(rows):
            mark(row, 0)
            if cols > 1:
                mark(row, cols - 1)

        for col in range(1, cols - 1):
            mark(0, col)
            if rows > 1:
                mark(rows - 1, col)

        while stack:
            row, col = stack.pop()
            if row > 0:
                mark(row - 1, col)
            if row + 1 < rows:
                mark(row + 1, col)
            if col > 0:
                mark(row, col - 1)
            if col + 1 < cols:
                mark(row, col + 1)

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == "O":
                    board[row][col] = "X"
                elif board[row][col] == "S":
                    board[row][col] = "O"
