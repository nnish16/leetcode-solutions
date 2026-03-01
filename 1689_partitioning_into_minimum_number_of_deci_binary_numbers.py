"""LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers

Key observation:
- The minimum number of deci-binary numbers needed to sum to n equals the maximum digit in n.

Reason:
- Each deci-binary number contributes at most 1 to any digit position.
- Therefore, if a digit d appears in n, we need at least d numbers to supply that position.
- We can always construct d such numbers, so the bound is tight.

Time:  O(len(n))
Space: O(1)
"""


class Solution:
    def minPartitions(self, n: str) -> int:
        return max(int(ch) for ch in n)
