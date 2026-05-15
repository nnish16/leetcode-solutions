from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        is_palindrome = [[False] * n for _ in range(n)]
        for end in range(n):
            for start in range(end, -1, -1):
                if s[start] == s[end] and (end - start < 2 or is_palindrome[start + 1][end - 1]):
                    is_palindrome[start][end] = True

        result: List[List[str]] = []
        path: List[str] = []

        def backtrack(index: int) -> None:
            if index == n:
                result.append(path.copy())
                return

            for end in range(index, n):
                if not is_palindrome[index][end]:
                    continue
                path.append(s[index:end + 1])
                backtrack(end + 1)
                path.pop()

        backtrack(0)
        return result
