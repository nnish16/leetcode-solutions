class Solution:
    def rotatedDigits(self, n: int) -> int:
        valid_digits = {"0", "1", "2", "5", "6", "8", "9"}
        changing_digits = {"2", "5", "6", "9"}
        good_count = 0

        for value in range(1, n + 1):
            digits = str(value)
            if all(digit in valid_digits for digit in digits) and any(
                digit in changing_digits for digit in digits
            ):
                good_count += 1

        return good_count
