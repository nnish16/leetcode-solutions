from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def generateTrees(self, n: int) -> List[Optional["TreeNode"]]:
        if n == 0:
            return []

        def build(left: int, right: int) -> List[Optional["TreeNode"]]:
            if left > right:
                return [None]

            trees: List[Optional["TreeNode"]] = []
            for root_value in range(left, right + 1):
                left_trees = build(left, root_value - 1)
                right_trees = build(root_value + 1, right)
                for left_tree in left_trees:
                    for right_tree in right_trees:
                        root = TreeNode(root_value)
                        root.left = left_tree
                        root.right = right_tree
                        trees.append(root)
            return trees

        return build(1, n)
