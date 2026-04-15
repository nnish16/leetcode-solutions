from typing import List


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        result: List[str] = []
        index = 0

        while index < len(words):
            line_length = len(words[index])
            last = index + 1

            while last < len(words) and line_length + 1 + len(words[last]) <= maxWidth:
                line_length += 1 + len(words[last])
                last += 1

            line_words = words[index:last]
            gaps = last - index - 1
            letters = sum(len(word) for word in line_words)

            if last == len(words) or gaps == 0:
                line = ' '.join(line_words)
                line += ' ' * (maxWidth - len(line))
            else:
                total_spaces = maxWidth - letters
                even_spaces, extra_spaces = divmod(total_spaces, gaps)
                parts = []
                for gap_index, word in enumerate(line_words[:-1]):
                    parts.append(word)
                    spaces = even_spaces + (1 if gap_index < extra_spaces else 0)
                    parts.append(' ' * spaces)
                parts.append(line_words[-1])
                line = ''.join(parts)

            result.append(line)
            index = last

        return result
