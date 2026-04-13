from math import factorial


class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        numbers = [str(value) for value in range(1, n + 1)]
        k -= 1
        permutation = []

        for remaining in range(n, 0, -1):
            block_size = factorial(remaining - 1)
            index, k = divmod(k, block_size)
            permutation.append(numbers.pop(index))

        return ''.join(permutation)
