from typing import Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional["TreeNode"]) -> bool:
        def validate(node: Optional["TreeNode"], low: int | None, high: int | None) -> bool:
            if not node:
                return True
            if low is not None and node.val <= low:
                return False
            if high is not None and node.val >= high:
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)

        return validate(root, None, None)
