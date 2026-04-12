class Solution:
    def totalNQueens(self, n: int) -> int:
        columns: set[int] = set()
        diag_down: set[int] = set()
        diag_up: set[int] = set()
        count = 0

        def backtrack(row: int) -> None:
            nonlocal count
            if row == n:
                count += 1
                return

            for col in range(n):
                if col in columns or (row - col) in diag_down or (row + col) in diag_up:
                    continue

                columns.add(col)
                diag_down.add(row - col)
                diag_up.add(row + col)

                backtrack(row + 1)

                diag_up.remove(row + col)
                diag_down.remove(row - col)
                columns.remove(col)

        backtrack(0)
        return count
