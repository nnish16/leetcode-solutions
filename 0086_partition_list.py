from typing import Optional


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional['ListNode'], x: int) -> Optional['ListNode']:
        before_dummy = ListNode(0)
        after_dummy = ListNode(0)
        before = before_dummy
        after = after_dummy
        current = head

        while current:
            next_node = current.next
            current.next = None
            if current.val < x:
                before.next = current
                before = before.next
            else:
                after.next = current
                after = after.next
            current = next_node

        before.next = after_dummy.next
        return before_dummy.next
