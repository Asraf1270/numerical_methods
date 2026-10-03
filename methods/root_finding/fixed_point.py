"""Fixed Point Iteration Method."""

from ..base import NumericalMethod
from equation import build_function


class FixedPoint(NumericalMethod):
    name = "Fixed Point Iteration"
    description = "Iterates x = g(x) starting from x0 until convergence."
    input_spec = [
        ("g_expr", "Enter g(x) such that x = g(x)", str),
        ("x0", "Initial guess x0", float),
    ]

    def solve(self, f, params, tol, max_iter):
        g = build_function(params["g_expr"])
        x = params["x0"]

        headers = ["Iter", "x", "g(x)", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            x_new = g(x)
            error = abs(x_new - x)
            table.append([i, x, x_new, error])

            if error < tol or abs(g(x_new) - x_new) < tol:
                return x_new, table, headers, i
            x = x_new

        return x_new, table, headers, max_iter