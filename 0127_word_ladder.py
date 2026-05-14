from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0

        front = {beginWord}
        back = {endWord}
        visited = {beginWord, endWord}
        steps = 1
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        while front and back:
            if len(front) > len(back):
                front, back = back, front

            nxt = set()
            for word in front:
                chars = list(word)
                for i, original in enumerate(chars):
                    for letter in alphabet:
                        if letter == original:
                            continue
                        chars[i] = letter
                        candidate = ''.join(chars)
                        if candidate in back:
                            return steps + 1
                        if candidate in words and candidate not in visited:
                            visited.add(candidate)
                            nxt.add(candidate)
                    chars[i] = original

            front = nxt
            steps += 1

        return 0
