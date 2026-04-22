from typing import List


class Solution:
    def twoEditWords(self, queries: List[str], dictionary: List[str]) -> List[str]:
        def within_two_edits(a: str, b: str) -> bool:
            mismatches = 0
            for ca, cb in zip(a, b):
                if ca != cb:
                    mismatches += 1
                    if mismatches > 2:
                        return False
            return True

        answer: List[str] = []
        for query in queries:
            if any(within_two_edits(query, word) for word in dictionary):
                answer.append(query)
        return answer
