class Solution:
    def minOperations(self, s: str, k: int) -> int:
        n = len(s)
        z = s.count('0')
        if z == 0:
            return 0
        if k == 0:
            return -1
        if k > n:
            return -1

        # Special case: each operation flips all indices
        if k == n:
            # After t operations, every bit is flipped t times.
            # Need t even for initial '1' positions, t odd for initial '0' positions.
            if z == n:
                return 1  # t must be odd; smallest is 1
            return -1

        # Parity feasibility: total flips = t*k must have same parity as number of zeros (odd flips needed per zero)
        if (k % 2 == 0) and (z % 2 == 1):
            return -1

        def ceil_div(a: int, b: int) -> int:
            return (a + b - 1) // b

        nk = n - k

        def feasible(t: int) -> bool:
            if t <= 0:
                return False
            total = t * k
            if total < z:
                return False
            if (total - z) & 1:
                return False
            # Upper bound constraints based on max achievable total flips with fixed per-index parity
            if t & 1:
                # t odd: need t*(n-k) >= n-z
                if t * nk < (n - z):
                    return False
            else:
                # t even: need t*(n-k) >= z
                if t * nk < z:
                    return False
            return True

        ans = None

        # If k is odd, t parity is forced by z parity (since t*k parity = t parity)
        if k % 2 == 1:
            t = max(1, ceil_div(z, k))
            if (t % 2) != (z % 2):
                t += 1
            # Also respect the upper-bound-derived constraint
            need = (n - z) if (t & 1) else z
            t = max(t, ceil_div(need, nk))
            if (t % 2) != (z % 2):
                t += 1
            while not feasible(t):
                t += 2
            ans = t
        else:
            # k even (and z even here): try both t parities and take min
            for parity in (0, 1):
                t = max(1, ceil_div(z, k))
                if (t & 1) != parity:
                    t += 1
                need = (n - z) if parity == 1 else z
                t = max(t, ceil_div(need, nk))
                if (t & 1) != parity:
                    t += 1
                while not feasible(t):
                    t += 2
                ans = t if ans is None else min(ans, t)

        return -1 if ans is None else ans
