from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups: dict[tuple[str, ...], List[str]] = defaultdict(list)

        for word in strs:
            groups[tuple(sorted(word))].append(word)

        return list(groups.values())
