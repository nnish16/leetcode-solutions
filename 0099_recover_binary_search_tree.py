from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def recoverTree(self, root: Optional["TreeNode"]) -> None:
        first: Optional["TreeNode"] = None
        second: Optional["TreeNode"] = None
        prev: Optional["TreeNode"] = None

        def inorder(node: Optional["TreeNode"]) -> None:
            nonlocal first, second, prev
            if not node:
                return
            inorder(node.left)
            if prev and prev.val > node.val:
                if first is None:
                    first = prev
                second = node
            prev = node
            inorder(node.right)

        inorder(root)
        if first and second:
            first.val, second.val = second.val, first.val
