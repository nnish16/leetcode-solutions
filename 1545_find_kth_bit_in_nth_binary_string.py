class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        # S1 = "0"
        # Sn = S(n-1) + "1" + reverse(invert(S(n-1)))
        # len(Sn) = 2^n - 1, middle index (1-based) = 2^(n-1)

        def helper(n: int, k: int) -> str:
            if n == 1:
                return '0'
            mid = 1 << (n - 1)
            if k == mid:
                return '1'
            if k < mid:
                return helper(n - 1, k)
            # mirror into left half, then invert
            left_k = (1 << n) - k  # == (2^n) - k
            bit = helper(n - 1, left_k)
            return '1' if bit == '0' else '0'

        return helper(n, k)
