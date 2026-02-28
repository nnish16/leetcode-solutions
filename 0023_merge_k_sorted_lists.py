# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

from typing import List, Optional
import heapq


class Solution:
    def mergeKLists(self, lists: List[Optional['ListNode']]) -> Optional['ListNode']:
        heap = []
        uid = 0

        for node in lists:
            if node is not None:
                heapq.heappush(heap, (node.val, uid, node))
                uid += 1

        dummy = ListNode(0)
        tail = dummy

        while heap:
            _, _, node = heapq.heappop(heap)
            tail.next = node
            tail = tail.next
            if node.next is not None:
                heapq.heappush(heap, (node.next.val, uid, node.next))
                uid += 1

        tail.next = None
        return dummy.next
