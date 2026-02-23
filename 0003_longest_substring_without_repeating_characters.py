"""LeetCode 3. Longest Substring Without Repeating Characters

Difficulty: Medium

Approach: Sliding window with last seen index for each character.
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = 0
        best = 0

        for right, ch in enumerate(s):
            if ch in last and last[ch] >= left:
                left = last[ch] + 1
            last[ch] = right
            best = max(best, right - left + 1)

        return best
