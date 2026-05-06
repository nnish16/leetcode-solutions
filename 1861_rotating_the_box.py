from typing import List


class Solution:
    def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
        rows = len(box)
        cols = len(box[0])

        for r in range(rows):
            write = cols - 1
            for c in range(cols - 1, -1, -1):
                if box[r][c] == '*':
                    write = c - 1
                elif box[r][c] == '#':
                    box[r][c] = '.'
                    box[r][write] = '#'
                    write -= 1

        rotated = [[''] * rows for _ in range(cols)]
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = box[r][c]

        return rotated
