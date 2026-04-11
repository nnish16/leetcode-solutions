class Solution:
    def myPow(self, x: float, n: int) -> float:
        exponent = n
        base = x

        if exponent < 0:
            base = 1 / base
            exponent = -exponent

        result = 1.0
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2

        return result
