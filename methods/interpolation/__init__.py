"""
Lagrange Interpolation.

Given n data points (xi, yi), constructs the unique polynomial
of degree ≤ n-1 passing through them, and evaluates it at a query point x.
"""

from ..base import BaseNumericalMethod
from utils import parse_points


class Lagrange(BaseNumericalMethod):
    name = "Lagrange Interpolation"
    description = "Builds P(x) through all points; evaluates at a target x."
    category = "interpolation"
    input_spec = [
        ("points", "Data points as 'x1,y1 x2,y2 ...'", str),
        ("xq", "Value of x to interpolate at", float),
    ]

    def solve(self, params, tol, max_iter):
        xs, ys = parse_points(params["points"])
        xq = params["xq"]
        n = len(xs)

        headers = ["i", "xi", "yi", "Li(x)", "yi · Li(x)"]
        table = []
        total = 0.0

        for i in range(n):
            Li = 1.0
            for j in range(n):
                if i != j:
                    Li *= (xq - xs[j]) / (xs[i] - xs[j])
            term = ys[i] * Li
            total += term
            table.append([i, xs[i], ys[i], Li, term])

        extras = {"P(x) value": total, "Degree": n - 1}
        return total, table, headers, extras