class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows <= 1 or numRows >= len(s):
            return s

        rows = ["" for _ in range(numRows)]
        r = 0
        step = 1  # +1 going down, -1 going up

        for ch in s:
            rows[r] += ch
            if r == 0:
                step = 1
            elif r == numRows - 1:
                step = -1
            r += step

        return "".join(rows)
