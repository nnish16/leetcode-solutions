class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        INT_MIN = -2**31
        INT_MAX = 2**31 - 1

        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        negative = (dividend < 0) ^ (divisor < 0)
        a = -dividend if dividend < 0 else dividend
        b = -divisor if divisor < 0 else divisor

        res = 0
        for shift in range(31, -1, -1):
            if (a >> shift) >= b:
                a -= b << shift
                res += 1 << shift

        return -res if negative else res
