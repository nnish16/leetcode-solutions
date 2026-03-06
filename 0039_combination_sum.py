from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res: List[List[int]] = []

        def dfs(start: int, remain: int, path: List[int]) -> None:
            if remain == 0:
                res.append(path.copy())
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if c > remain:
                    break
                path.append(c)
                dfs(i, remain - c, path)  # can reuse same element
                path.pop()

        dfs(0, target, [])
        return res
