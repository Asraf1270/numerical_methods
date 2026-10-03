"""
Muller's Method.

Uses quadratic interpolation through three points to find a root.
Often converges faster than the secant method and can find
complex roots (not covered here — we keep it real-valued).
"""

import math
from ..base import NumericalMethod


class Mullers(NumericalMethod):
    name = "Mullers Method"
    description = (
        "Quadratic interpolation through 3 points; converges faster than Secant."
    )
    input_spec = [
        ("x0", "First guess x0", float),
        ("x1", "Second guess x1", float),
        ("x2", "Third guess x2", float),
    ]

    def solve(self, f, params, tol, max_iter):
        x0, x1, x2 = params["x0"], params["x1"], params["x2"]

        if len({x0, x1, x2}) < 3:
            raise ValueError("x0, x1 and x2 must be three distinct points.")

        headers = ["Iter", "x0", "x1", "x2", "x3", "f(x3)", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            f0, f1, f2 = f(x0), f(x1), f(x2)

            h1 = x1 - x0
            h2 = x2 - x1
            if h1 == 0 or h2 == 0 or (h1 + h2) == 0:
                raise ValueError("Division by zero due to repeated points.")

            # Divided differences
            delta1 = (f1 - f0) / h1
            delta2 = (f2 - f1) / h2
            a = (delta2 - delta1) / (h2 + h1)
            b = a * h2 + delta2
            c = f2

            # Discriminant — choose the larger-magnitude denominator for stability
            disc = math.sqrt(b * b - 4 * a * c) if (b * b - 4 * a * c) >= 0 \
                else complex(0, math.sqrt(abs(b * b - 4 * a * c)))

            denom_plus = b + disc
            denom_minus = b - disc
            denom = denom_plus if abs(denom_plus) >= abs(denom_minus) else denom_minus

            if denom == 0:
                raise ValueError("Denominator in Muller's update is zero.")

            dx = -2 * c / denom
            x3 = x2 + dx
            error = abs(x3 - x2)

            # Guard against complex arithmetic slipping in
            if hasattr(x3, "imag") and abs(x3.imag) > 1e-12:
                raise ValueError(
                    "Iteration wandered into the complex plane. "
                    "Try different initial guesses."
                )
            x3 = float(x3.real) if hasattr(x3, "real") else float(x3)

            table.append([i, x0, x1, x2, x3, f(x3), error])

            if error < tol or abs(f(x3)) < tol:
                return x3, table, headers, i

            # Shift points forward for the next iteration
            x0, x1, x2 = x1, x2, x3

        return x3, table, headers, max_iter