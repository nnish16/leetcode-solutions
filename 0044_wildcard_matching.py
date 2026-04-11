class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        s_index = 0
        p_index = 0
        star_index = -1
        match_index = 0

        while s_index < len(s):
            if p_index < len(p) and (p[p_index] == s[s_index] or p[p_index] == "?"):
                s_index += 1
                p_index += 1
            elif p_index < len(p) and p[p_index] == "*":
                star_index = p_index
                match_index = s_index
                p_index += 1
            elif star_index != -1:
                p_index = star_index + 1
                match_index += 1
                s_index = match_index
            else:
                return False

        while p_index < len(p) and p[p_index] == "*":
            p_index += 1

        return p_index == len(p)
