"""
Newton Backward Difference Interpolation.

Best used when the query point is near the END of an equally-spaced table.
Formula: P(x) = yn + v·∇yn + v(v+1)/2!·∇²yn + ...
   with v = (x - xn) / h
"""

from ..base import BaseNumericalMethod
from utils import parse_points, is_equally_spaced, backward_diff_table
import math


class NewtonBackward(BaseNumericalMethod):
    name = "Newton Backward Difference"
    description = "Backward-difference formula for equally-spaced points (query near end)."
    category = "interpolation"
    input_spec = [
        ("points", "Data points as '(x1, y1), (x2, y2), ...'", str),
        ("xq", "Value of x to interpolate at", float),
    ]

    def solve(self, params, tol, max_iter):
        xs, ys = parse_points(params["points"])
        xq = params["xq"]

        if not is_equally_spaced(xs):
            raise ValueError("Newton Backward requires equally-spaced x values.")

        h = xs[1] - xs[0]
        n = len(xs)
        v = (xq - xs[-1]) / h

        diff_table = backward_diff_table(ys)

        headers = ["i", "xi", "yi", "v-term", "Contribution"]
        table = []
        total = ys[-1]   # start from yn

        for i in range(1, n):
            coef = 1.0
            for k in range(i):
                coef *= (v + k)
            coef /= math.factorial(i)
            term = coef * diff_table[-1][i]
            total += term
            table.append([i, xs[n - 1 - i], ys[n - 1 - i], coef, term])

        extras = {
            "h": h,
            "v": v,
            "Backward difference table": diff_table,
            "P(x) value": total,
        }
        return total, table, headers, extras