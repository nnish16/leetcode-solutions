from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional["TreeNode"], targetSum: int) -> List[List[int]]:
        paths: List[List[int]] = []
        current: List[int] = []

        def dfs(node: Optional["TreeNode"], remaining: int) -> None:
            if not node:
                return

            current.append(node.val)
            remaining -= node.val

            if not node.left and not node.right:
                if remaining == 0:
                    paths.append(current.copy())
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)

            current.pop()

        dfs(root, targetSum)
        return paths
