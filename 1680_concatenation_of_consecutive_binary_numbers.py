class Solution:
    def concatenatedBinary(self, n: int) -> int:
        MOD = 10**9 + 7
        ans = 0
        bitlen = 0

        for x in range(1, n + 1):
            if x & (x - 1) == 0:
                bitlen += 1
            ans = ((ans << bitlen) + x) % MOD

        return ans
