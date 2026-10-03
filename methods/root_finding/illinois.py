"""
Illinois Modified False Position Method.

Classic Regula Falsi can stagnate when one endpoint stops moving.
The Illinois modification halves the stagnant endpoint's function value,
restoring fast convergence while keeping bracketing guarantees.
"""

from ..base import NumericalMethod


class Illinois(NumericalMethod):
    name = "Illinois False Position"
    description = "Accelerated Regula Falsi that avoids endpoint stagnation."
    input_spec = [
        ("a", "Lower bound a", float),
        ("b", "Upper bound b", float),
    ]

    def solve(self, f, params, tol, max_iter):
        a, b = params["a"], params["b"]

        fa, fb = f(a), f(b)
        if fa * fb >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs.")

        headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
        table = []
        c_old = None
        side = None  # remember which side was updated last

        for i in range(1, max_iter + 1):
            c = (a * fb - b * fa) / (fb - fa)
            fc = f(c)
            error = abs(c - c_old) if c_old is not None else abs(b - a)
            table.append([i, a, b, c, fc, error])

            if abs(fc) < tol or error < tol:
                return c, table, headers, i

            if fa * fc < 0:
                # root is in [a, c] → b moves
                b, fb = c, fc
                if side == "b":
                    fa *= 0.5      # Illinois step: dampen the stagnant endpoint
                side = "b"
            else:
                # root is in [c, b] → a moves
                a, fa = c, fc
                if side == "a":
                    fb *= 0.5
                side = "a"

            c_old = c

        return c, table, headers, max_iter