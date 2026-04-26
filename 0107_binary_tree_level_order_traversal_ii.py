from collections import deque
from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrderBottom(self, root: Optional["TreeNode"]) -> List[List[int]]:
        if not root:
            return []

        levels: deque[List[int]] = deque()
        queue = deque([root])

        while queue:
            level: List[int] = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            levels.appendleft(level)

        return list(levels)
