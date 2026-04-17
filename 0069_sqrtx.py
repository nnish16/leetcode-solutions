class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        left, right = 1, x // 2
        answer = 1

        while left <= right:
            mid = (left + right) // 2
            square = mid * mid

            if square == x:
                return mid
            if square < x:
                answer = mid
                left = mid + 1
            else:
                right = mid - 1

        return answer
