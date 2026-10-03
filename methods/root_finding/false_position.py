"""False Position (Regula Falsi) Method."""

from ..base import NumericalMethod


class FalsePosition(NumericalMethod):
    name = "False Position Method"
    description = "Like bisection but uses linear interpolation for the new point."
    input_spec = [
        ("a", "Lower bound a", float),
        ("b", "Upper bound b", float),
    ]

    def solve(self, f, params, tol, max_iter):
        a, b = params["a"], params["b"]

        if f(a) * f(b) >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs.")

        headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
        table = []
        c_old = None

        for i in range(1, max_iter + 1):
            fa, fb = f(a), f(b)
            c = b - fb * (b - a) / (fb - fa)
            fc = f(c)
            error = abs(c - c_old) if c_old is not None else abs(b - a)
            table.append([i, a, b, c, fc, error])

            if abs(fc) < tol or error < tol:
                return c, table, headers, i

            if fa * fc < 0:
                b = c
            else:
                a = c
            c_old = c

        return c, table, headers, max_iter