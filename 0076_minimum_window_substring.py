from collections import Counter, defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(t) > len(s):
            return ""

        need = Counter(t)
        window = defaultdict(int)
        required = len(need)
        formed = 0
        best_start = 0
        best_length = float("inf")
        left = 0

        for right, char in enumerate(s):
            if char in need:
                window[char] += 1
                if window[char] == need[char]:
                    formed += 1

            while formed == required:
                current_length = right - left + 1
                if current_length < best_length:
                    best_length = current_length
                    best_start = left

                left_char = s[left]
                if left_char in need:
                    window[left_char] -= 1
                    if window[left_char] < need[left_char]:
                        formed -= 1
                left += 1

        if best_length == float("inf"):
            return ""
        return s[best_start:best_start + best_length]
