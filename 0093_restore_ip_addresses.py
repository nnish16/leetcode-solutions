from typing import List


class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        result: List[str] = []
        parts: List[str] = []

        def backtrack(index: int) -> None:
            if len(parts) == 4:
                if index == len(s):
                    result.append(".".join(parts))
                return

            remaining_chars = len(s) - index
            remaining_parts = 4 - len(parts)
            if remaining_chars < remaining_parts or remaining_chars > remaining_parts * 3:
                return

            for end in range(index + 1, min(index + 4, len(s) + 1)):
                segment = s[index:end]
                if len(segment) > 1 and segment[0] == "0":
                    break
                if int(segment) > 255:
                    break
                parts.append(segment)
                backtrack(end)
                parts.pop()

        backtrack(0)
        return result
