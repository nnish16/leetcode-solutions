from collections import Counter, defaultdict
from typing import List


class Solution:
    def minimumHammingDistance(
        self,
        source: List[int],
        target: List[int],
        allowedSwaps: List[List[int]],
    ) -> int:
        parent = list(range(len(source)))
        rank = [0] * len(source)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            root_a = find(a)
            root_b = find(b)
            if root_a == root_b:
                return
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1

        for a, b in allowedSwaps:
            union(a, b)

        available = defaultdict(Counter)
        for index, value in enumerate(source):
            available[find(index)][value] += 1

        mismatches = 0
        for index, value in enumerate(target):
            counts = available[find(index)]
            if counts[value] > 0:
                counts[value] -= 1
            else:
                mismatches += 1

        return mismatches
