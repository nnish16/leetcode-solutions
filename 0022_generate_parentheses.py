from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res: List[str] = []

        def dfs(opened: int, closed: int, cur: list[str]) -> None:
            if opened == n and closed == n:
                res.append(''.join(cur))
                return

            if opened < n:
                cur.append('(')
                dfs(opened + 1, closed, cur)
                cur.pop()

            if closed < opened:
                cur.append(')')
                dfs(opened, closed + 1, cur)
                cur.pop()

        dfs(0, 0, [])
        return res
