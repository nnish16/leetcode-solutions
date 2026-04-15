from typing import List


class Solution:
    def closestTarget(self, words: List[str], target: str, startIndex: int) -> int:
        n = len(words)
        best = n + 1

        for i, word in enumerate(words):
            if word != target:
                continue
            distance = abs(i - startIndex)
            best = min(best, distance, n - distance)

        return -1 if best == n + 1 else best
