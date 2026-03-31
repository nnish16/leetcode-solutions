from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        ans: List[List[int]] = []
        path: List[int] = []
        n = len(candidates)

        def dfs(start: int, remain: int) -> None:
            if remain == 0:
                ans.append(path[:])
                return

            prev = None
            for i in range(start, n):
                x = candidates[i]
                if x == prev:
                    continue
                if x > remain:
                    break
                path.append(x)
                dfs(i + 1, remain - x)
                path.pop()
                prev = x

        dfs(0, target)
        return ans
