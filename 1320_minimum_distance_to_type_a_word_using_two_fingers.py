class Solution:
    def minimumDistance(self, word: str) -> int:
        unused = 26

        def distance(a: int, b: int) -> int:
            if a == unused or b == unused:
                return 0
            ax, ay = divmod(a, 6)
            bx, by = divmod(b, 6)
            return abs(ax - bx) + abs(ay - by)

        if len(word) < 2:
            return 0

        dp = {unused: 0}

        for index in range(1, len(word)):
            prev_char = ord(word[index - 1]) - ord("A")
            curr_char = ord(word[index]) - ord("A")
            next_dp: dict[int, int] = {}

            for other_finger, cost in dp.items():
                move_active = cost + distance(prev_char, curr_char)
                best_move_active = next_dp.get(other_finger)
                if best_move_active is None or move_active < best_move_active:
                    next_dp[other_finger] = move_active

                move_other = cost + distance(other_finger, curr_char)
                best_move_other = next_dp.get(prev_char)
                if best_move_other is None or move_other < best_move_other:
                    next_dp[prev_char] = move_other

            dp = next_dp

        return min(dp.values())
