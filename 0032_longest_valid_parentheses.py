class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # Stack of indices; start with a sentinel for the last unmatched ')'
        stack = [-1]
        best = 0

        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    # new base after an unmatched ')'
                    stack.append(i)
                else:
                    best = max(best, i - stack[-1])

        return best
