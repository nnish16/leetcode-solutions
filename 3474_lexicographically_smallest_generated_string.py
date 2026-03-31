class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        length = n + m - 1
        word = ['?'] * length

        for i, flag in enumerate(str1):
            if flag == 'T':
                for j, ch in enumerate(str2):
                    pos = i + j
                    if word[pos] == '?' or word[pos] == ch:
                        word[pos] = ch
                    else:
                        return ''

        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        transitions = [[0] * 26 for _ in range(m + 1)]
        for state in range(m + 1):
            base = pi[m - 1] if state == m else state
            for c in range(26):
                ch = chr(ord('a') + c)
                k = base
                while k and str2[k] != ch:
                    k = pi[k - 1]
                if str2[k] == ch:
                    k += 1
                transitions[state][c] = k

        dp = [bytearray(m + 1) for _ in range(length + 1)]
        for state in range(m + 1):
            dp[length][state] = 1

        for idx in range(length - 1, -1, -1):
            choices = [word[idx]] if word[idx] != '?' else ['a', 'b']
            next_row = dp[idx + 1]
            cur_row = dp[idx]
            for state in range(m + 1):
                possible = 0
                for ch in choices:
                    next_state = transitions[state][ord(ch) - ord('a')]
                    if idx >= m - 1:
                        start = idx - m + 1
                        if str1[start] == 'T':
                            if next_state != m:
                                continue
                        elif next_state == m:
                            continue
                    if next_row[next_state]:
                        possible = 1
                        break
                cur_row[state] = possible

        if not dp[0][0]:
            return ''

        ans = []
        state = 0
        for idx in range(length):
            choices = [word[idx]] if word[idx] != '?' else ['a', 'b']
            for ch in choices:
                next_state = transitions[state][ord(ch) - ord('a')]
                if idx >= m - 1:
                    start = idx - m + 1
                    if str1[start] == 'T':
                        if next_state != m:
                            continue
                    elif next_state == m:
                        continue
                if dp[idx + 1][next_state]:
                    ans.append(ch)
                    state = next_state
                    break

        return ''.join(ans)
