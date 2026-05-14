from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: Optional["TreeNode"]) -> int:
        def dfs(node: Optional["TreeNode"], value: int) -> int:
            if node is None:
                return 0

            value = value * 10 + node.val
            if node.left is None and node.right is None:
                return value

            return dfs(node.left, value) + dfs(node.right, value)

        return dfs(root, 0)
