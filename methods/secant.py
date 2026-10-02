"""Secant Method."""

from .base import NumericalMethod


class Secant(NumericalMethod):
    name = "Secant Method"
    description = "Approximates derivative using two points (no derivative needed)."
    input_spec = [
        ("x0", "First initial guess x0", float),
        ("x1", "Second initial guess x1", float),
    ]

    def solve(self, f, params, tol, max_iter):
        x0, x1 = params["x0"], params["x1"]

        headers = ["Iter", "x0", "x1", "f(x0)", "f(x1)", "x2", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            f0, f1 = f(x0), f(x1)
            if (f1 - f0) == 0:
                raise ValueError("Division by zero in secant formula.")

            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            error = abs(x2 - x1)
            table.append([i, x0, x1, f0, f1, x2, error])

            if error < tol or abs(f(x2)) < tol:
                return x2, table, headers, i
            x0, x1 = x1, x2

        return x2, table, headers, max_iter