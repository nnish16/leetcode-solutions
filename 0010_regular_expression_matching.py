from functools import lru_cache

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        # DP over indices (i in s, j in p)
        @lru_cache(None)
        def dp(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)

            first = i < len(s) and (p[j] == s[i] or p[j] == '.')

            # handle '*' as "zero or more of previous token"
            if j + 1 < len(p) and p[j + 1] == '*':
                # skip token+*  OR  consume one char if it matches
                return dp(i, j + 2) or (first and dp(i + 1, j))

            return first and dp(i + 1, j + 1)

        return dp(0, 0)
