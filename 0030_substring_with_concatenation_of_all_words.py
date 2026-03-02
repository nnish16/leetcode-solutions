from typing import List
from collections import Counter, defaultdict

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        word_count = len(words)
        total_len = word_len * word_count
        if len(s) < total_len:
            return []

        need = Counter(words)
        res: List[int] = []

        # We slide in word-sized steps for each possible offset
        for offset in range(word_len):
            left = offset
            window = defaultdict(int)
            used = 0  # number of words matched in window (counting multiplicities)

            for right in range(offset, len(s) - word_len + 1, word_len):
                w = s[right:right + word_len]

                if w in need:
                    window[w] += 1
                    used += 1

                    # shrink if word frequency exceeded
                    while window[w] > need[w]:
                        w_left = s[left:left + word_len]
                        window[w_left] -= 1
                        used -= 1
                        left += word_len

                    # if we have all words, record and move left by one word
                    if used == word_count:
                        res.append(left)
                        w_left = s[left:left + word_len]
                        window[w_left] -= 1
                        used -= 1
                        left += word_len
                else:
                    # reset window
                    window.clear()
                    used = 0
                    left = right + word_len

        return res
