"""
Newton's Divided Difference Interpolation.

Works for ANY (possibly non-uniform) set of x values.
Formula: P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
"""

from ..base import BaseNumericalMethod
from utils import parse_points, divided_diff_table


class NewtonDivided(BaseNumericalMethod):
    name = "Newton Divided Difference"
    description = "Handles non-uniform x values via divided differences."
    category = "interpolation"
    input_spec = [
        ("points", "Data points as 'x1,y1 x2,y2 ...'", str),
        ("xq", "Value of x to interpolate at", float),
    ]

    def solve(self, params, tol, max_iter):
        xs, ys = parse_points(params["points"])
        xq = params["xq"]
        n = len(xs)

        table_coefs = divided_diff_table(xs, ys)

        headers = ["i", "xi", "f[xi]", "Term coef", "Product (x-xk)", "Contribution"]
        table = []
        total = table_coefs[0][0]     # f[x0]

        for i in range(1, n):
            prod = 1.0
            for k in range(i):
                prod *= (xq - xs[k])
            term = table_coefs[0][i] * prod
            total += term
            table.append([i, xs[i], table_coefs[0][i],
                          table_coefs[0][i], prod, term])

        extras = {
            "Divided difference table": table_coefs,
            "P(x) value": total,
            "Degree": n - 1,
        }
        return total, table, headers, extras