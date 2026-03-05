class Solution:
    def minOperations(self, s: str) -> int:
        # Count mismatches vs patterns 0101... and 1010...
        mism0 = 0
        mism1 = 0
        for i, ch in enumerate(s):
            exp0 = '0' if i % 2 == 0 else '1'
            exp1 = '1' if i % 2 == 0 else '0'
            if ch != exp0:
                mism0 += 1
            if ch != exp1:
                mism1 += 1
        return mism0 if mism0 < mism1 else mism1
