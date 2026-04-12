from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        results: List[List[str]] = []
        columns: set[int] = set()
        diag_down: set[int] = set()
        diag_up: set[int] = set()
        board = [["."] * n for _ in range(n)]

        def backtrack(row: int) -> None:
            if row == n:
                results.append(["".join(line) for line in board])
                return

            for col in range(n):
                if col in columns or (row - col) in diag_down or (row + col) in diag_up:
                    continue

                columns.add(col)
                diag_down.add(row - col)
                diag_up.add(row + col)
                board[row][col] = "Q"

                backtrack(row + 1)

                board[row][col] = "."
                diag_up.remove(row + col)
                diag_down.remove(row - col)
                columns.remove(col)

        backtrack(0)
        return results
