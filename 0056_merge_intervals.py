from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        intervals.sort(key=lambda interval: interval[0])
        merged = [intervals[0][:]]

        for start, end in intervals[1:]:
            last_interval = merged[-1]
            if start <= last_interval[1]:
                last_interval[1] = max(last_interval[1], end)
            else:
                merged.append([start, end])

        return merged
