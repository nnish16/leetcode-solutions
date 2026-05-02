from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def flatten(self, root: Optional["TreeNode"]) -> None:
        if not root:
            return

        stack = [root]
        previous = None

        while stack:
            node = stack.pop()

            if previous is not None:
                previous.left = None
                previous.right = node

            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

            previous = node
