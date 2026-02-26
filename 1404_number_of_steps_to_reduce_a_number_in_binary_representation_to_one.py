class Solution:
    def numSteps(self, s: str) -> int:
        # Work from least-significant bit to the second-most-significant.
        # Track a carry that represents prior +1 operations.
        if s == "1":
            return 0

        carry = 0
        steps = 0

        for i in range(len(s) - 1, 0, -1):
            bit = ord(s[i]) - 48  # int(s[i]) but faster
            if bit + carry == 1:
                # odd -> +1 (makes it even, introduces carry) then /2
                steps += 2
                carry = 1
            else:
                # even -> /2
                steps += 1

        return steps + carry
