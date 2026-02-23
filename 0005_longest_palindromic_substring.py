from typing import List

class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        def expand(l: int, r: int):
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r - 1

        best_l, best_r = 0, 0
        for i in range(n):
            l1, r1 = expand(i, i)      # odd
            if r1 - l1 > best_r - best_l:
                best_l, best_r = l1, r1
            l2, r2 = expand(i, i + 1)  # even
            if r2 - l2 > best_r - best_l:
                best_l, best_r = l2, r2

        return s[best_l:best_r + 1]
