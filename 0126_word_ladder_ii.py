from collections import defaultdict
from string import ascii_lowercase
from typing import DefaultDict, List, Set


class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        remaining: Set[str] = set(wordList)
        if endWord not in remaining:
            return []

        parents: DefaultDict[str, Set[str]] = defaultdict(set)
        current_level = {beginWord}

        while current_level and endWord not in parents:
            remaining -= current_level
            next_level: DefaultDict[str, Set[str]] = defaultdict(set)

            for word in current_level:
                for index, original in enumerate(word):
                    prefix = word[:index]
                    suffix = word[index + 1 :]
                    for letter in ascii_lowercase:
                        if letter == original:
                            continue
                        candidate = prefix + letter + suffix
                        if candidate in remaining:
                            next_level[candidate].add(word)

            current_level = set(next_level)
            for word, predecessors in next_level.items():
                parents[word].update(predecessors)

        if endWord not in parents:
            return []

        ladders: List[List[str]] = []
        path = [endWord]

        def build_paths(word: str) -> None:
            if word == beginWord:
                ladders.append(path[::-1])
                return

            for predecessor in parents[word]:
                path.append(predecessor)
                build_paths(predecessor)
                path.pop()

        build_paths(endWord)
        return ladders
