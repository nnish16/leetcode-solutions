class Solution:
    def isNumber(self, s: str) -> bool:
        s = s.strip()
        if not s:
            return False

        seen_digit = False
        seen_dot = False
        seen_exp = False
        digit_after_exp = True

        for i, ch in enumerate(s):
            if ch.isdigit():
                seen_digit = True
                if seen_exp:
                    digit_after_exp = True
            elif ch in '+-':
                if i > 0 and s[i - 1].lower() != 'e':
                    return False
            elif ch == '.':
                if seen_dot or seen_exp:
                    return False
                seen_dot = True
            elif ch.lower() == 'e':
                if seen_exp or not seen_digit:
                    return False
                seen_exp = True
                digit_after_exp = False
            else:
                return False

        return seen_digit and digit_after_exp
