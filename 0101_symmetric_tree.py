from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional["TreeNode"]) -> bool:
        def mirror(left: Optional["TreeNode"], right: Optional["TreeNode"]) -> bool:
            if not left or not right:
                return left is right
            if left.val != right.val:
                return False
            return mirror(left.left, right.right) and mirror(left.right, right.left)

        return mirror(root.left, root.right) if root else True
