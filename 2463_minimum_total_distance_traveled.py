from functools import lru_cache
from math import inf
from typing import List


class Solution:
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        robot.sort()
        factory.sort()
        positions = [position for position, _ in factory]
        limits = [limit for _, limit in factory]
        robot_count = len(robot)
        factory_count = len(factory)

        @lru_cache(None)
        def dp(robot_index: int, factory_index: int) -> int:
            if robot_index == robot_count:
                return 0
            if factory_index == factory_count:
                return inf

            best = dp(robot_index, factory_index + 1)
            distance = 0
            position = positions[factory_index]
            max_take = min(limits[factory_index], robot_count - robot_index)

            for used in range(1, max_take + 1):
                distance += abs(robot[robot_index + used - 1] - position)
                best = min(best, distance + dp(robot_index + used, factory_index + 1))

            return best

        return dp(0, 0)
