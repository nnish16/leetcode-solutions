class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m = len(num1)
        n = len(num2)
        digits = [0] * (m + n)

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                product = (ord(num1[i]) - ord("0")) * (ord(num2[j]) - ord("0"))
                total = product + digits[i + j + 1]
                digits[i + j + 1] = total % 10
                digits[i + j] += total // 10

        index = 0
        while index < len(digits) and digits[index] == 0:
            index += 1

        return "".join(str(digit) for digit in digits[index:])
