from typing import Optional


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedListToBST(self, head: Optional["ListNode"]) -> Optional["TreeNode"]:
        def find_middle(start: Optional["ListNode"]) -> tuple[Optional["ListNode"], Optional["ListNode"]]:
            prev = None
            slow = start
            fast = start

            while fast and fast.next:
                prev = slow
                slow = slow.next
                fast = fast.next.next

            return prev, slow

        if not head:
            return None
        if not head.next:
            return TreeNode(head.val)

        prev_mid, mid = find_middle(head)
        prev_mid.next = None

        root = TreeNode(mid.val)
        root.left = self.sortedListToBST(head)
        root.right = self.sortedListToBST(mid.next)
        return root
