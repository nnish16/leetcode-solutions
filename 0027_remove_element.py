from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # In-place overwrite using two pointers.
        k = 0
        for x in nums:
            if x != val:
                nums[k] = x
                k += 1
        return k
