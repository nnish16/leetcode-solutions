from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows = len(board)
        cols = len(board[0])

        def dfs(row: int, col: int, index: int) -> bool:
            if index == len(word):
                return True
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            if board[row][col] != word[index]:
                return False

            letter = board[row][col]
            board[row][col] = "#"
            found = (
                dfs(row + 1, col, index + 1)
                or dfs(row - 1, col, index + 1)
                or dfs(row, col + 1, index + 1)
                or dfs(row, col - 1, index + 1)
            )
            board[row][col] = letter
            return found

        for row in range(rows):
            for col in range(cols):
                if dfs(row, col, 0):
                    return True

        return False
