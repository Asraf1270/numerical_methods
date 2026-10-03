"""
Steffensen's Method.

Accelerates fixed-point iteration x = g(x) using Aitken's Δ² extrapolation.
Achieves quadratic convergence without needing a derivative.
"""

from ..base import NumericalMethod
from equation import build_function


class Steffensen(NumericalMethod):
    name = "Steffensen's Method"
    description = "Quadratic convergence for x = g(x), no derivative required."
    input_spec = [
        ("g_expr", "Enter g(x) such that x = g(x)", str),
        ("x0", "Initial guess x0", float),
    ]

    def solve(self, f, params, tol, max_iter):
        g = build_function(params["g_expr"])
        x = params["x0"]

        headers = ["Iter", "x", "g(x)", "g(g(x))", "x_new", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            gx = g(x)
            ggx = g(gx)

            denom = ggx - 2 * gx + x
            if denom == 0:
                raise ValueError("Steffensen denominator is zero; try another x0.")

            x_new = x - (gx - x) ** 2 / denom
            error = abs(x_new - x)
            table.append([i, x, gx, ggx, x_new, error])

            if error < tol or abs(f(x_new)) < tol:
                return x_new, table, headers, i
            x = x_new

        return x_new, table, headers, max_iter