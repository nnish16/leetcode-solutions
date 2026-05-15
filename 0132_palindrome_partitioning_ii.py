class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        is_palindrome = [[False] * n for _ in range(n)]
        for end in range(n):
            for start in range(end, -1, -1):
                if s[start] == s[end] and (end - start < 2 or is_palindrome[start + 1][end - 1]):
                    is_palindrome[start][end] = True

        cuts = [0] * n
        for end in range(n):
            if is_palindrome[0][end]:
                cuts[end] = 0
                continue

            best = end
            for start in range(1, end + 1):
                if is_palindrome[start][end]:
                    best = min(best, cuts[start - 1] + 1)
            cuts[end] = best

        return cuts[-1]
