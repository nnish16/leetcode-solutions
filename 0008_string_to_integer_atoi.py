class Solution:
    def myAtoi(self, s: str) -> int:
        i = 0
        n = len(s)

        # skip leading spaces
        while i < n and s[i] == ' ':
            i += 1

        sign = 1
        if i < n and s[i] in '+-':
            if s[i] == '-':
                sign = -1
            i += 1

        num = 0
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        while i < n and s[i].isdigit():
            digit = ord(s[i]) - ord('0')
            num = num * 10 + digit
            i += 1

        num *= sign
        if num < INT_MIN:
            return INT_MIN
        if num > INT_MAX:
            return INT_MAX
        return num
