from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empties = []

        def box_id(r: int, c: int) -> int:
            return (r // 3) * 3 + (c // 3)

        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == '.':
                    empties.append((r, c))
                else:
                    d = ord(ch) - ord('1')
                    bit = 1 << d
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[box_id(r, c)] |= bit

        FULL = (1 << 9) - 1

        def backtrack(start: int) -> bool:
            if start == len(empties):
                return True

            best_i = start
            best_cnt = 10

            for i in range(start, len(empties)):
                r, c = empties[i]
                b = box_id(r, c)
                used = rows[r] | cols[c] | boxes[b]
                mask = (~used) & FULL
                cnt = mask.bit_count()
                if cnt < best_cnt:
                    best_cnt = cnt
                    best_i = i
                    if cnt == 1:
                        break

            empties[start], empties[best_i] = empties[best_i], empties[start]
            r, c = empties[start]
            b = box_id(r, c)
            used = rows[r] | cols[c] | boxes[b]
            mask = (~used) & FULL

            while mask:
                bit = mask & -mask
                mask -= bit
                d = bit.bit_length() - 1

                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
                board[r][c] = chr(ord('1') + d)

                if backtrack(start + 1):
                    return True

                board[r][c] = '.'
                rows[r] ^= bit
                cols[c] ^= bit
                boxes[b] ^= bit

            empties[start], empties[best_i] = empties[best_i], empties[start]
            return False

        backtrack(0)
