"""
Newton Forward Difference Interpolation.

Best used when the query point is near the START of an equally-spaced table.
Formula: P(x) = y0 + u·Δy0 + u(u-1)/2!·Δ²y0 + ...
   with u = (x - x0) / h
"""

from ..base import BaseNumericalMethod
from utils import parse_points, is_equally_spaced, forward_diff_table


class NewtonForward(BaseNumericalMethod):
    name = "Newton Forward Difference"
    description = "Forward-difference formula for equally-spaced points (query near start)."
    category = "interpolation"
    input_spec = [
        ("points", "Data points as '(x1, y1), (x2, y2), ...'", str),
        ("xq", "Value of x to interpolate at", float),
    ]

    def solve(self, params, tol, max_iter):
        xs, ys = parse_points(params["points"])
        xq = params["xq"]

        if not is_equally_spaced(xs):
            raise ValueError("Newton Forward requires equally-spaced x values.")

        h = xs[1] - xs[0]
        u = (xq - xs[0]) / h
        n = len(xs)

        diff_table = forward_diff_table(ys)

        # Iteration table
        headers = ["i", "xi", "yi", "u-term", "Contribution"]
        table = []
        total = ys[0]

        for i in range(1, n):
            coef = 1.0
            for k in range(i):
                coef *= (u - k)
            coef /= __import__("math").factorial(i)
            term = coef * diff_table[0][i]
            total += term
            table.append([i, xs[i], ys[i], coef, term])

        extras = {
            "h": h,
            "u": u,
            "Forward difference table": diff_table,
            "P(x) value": total,
        }
        return total, table, headers, extras