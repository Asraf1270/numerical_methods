"""
Brent's Method.

Combines:
  - Inverse quadratic interpolation
  - Secant method
  - Bisection (fallback for robustness)
It is the default algorithm in most production root finders (e.g., scipy).
"""

import math
from ..base import NumericalMethod


class Brent(NumericalMethod):
    name = "Brent's Method"
    description = "Hybrid: inverse quadratic + secant + bisection. Very robust."
    input_spec = [
        ("a", "Lower bound a", float),
        ("b", "Upper bound b", float),
    ]

    def solve(self, f, params, tol, max_iter):
        a, b = params["a"], params["b"]
        fa, fb = f(a), f(b)

        if fa * fb >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs.")

        # Ensure |fa| < |fb|
        if abs(fa) > abs(fb):
            a, b = b, a
            fa, fb = fb, fa

        c, fc = a, fa
        d = b - a
        e = d

        headers = ["Iter", "a", "b", "c", "f(b)", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            if fb * fc > 0:
                c, fc = a, fa
                d = e = b - a

            if abs(fc) < abs(fb):
                a, b, c = b, c, b
                fa, fb, fc = fb, fc, fb

            # Convergence check
            tol1 = 2 * 1e-15 * abs(b) + 0.5 * tol
            xm = 0.5 * (c - b)
            error = abs(xm)

            table.append([i, a, b, c, fb, error])

            if abs(xm) <= tol1 or fb == 0:
                return b, table, headers, i

            # Attempt inverse quadratic interpolation or secant
            if abs(e) >= tol1 and abs(fa) > abs(fb):
                s = fb / fa
                if a == c:
                    # Secant
                    p = 2 * xm * s
                    q = 1 - s
                else:
                    # Inverse quadratic interpolation
                    q = fa / fc
                    r = fb / fc
                    p = s * (2 * xm * q * (q - r) - (b - a) * (r - 1))
                    q = (q - 1) * (r - 1) * (s - 1)

                if p > 0:
                    q = -q
                p = abs(p)

                # Accept interpolation only if it stays well inside the interval
                if 2 * p < min(3 * xm * q - abs(tol1 * q), abs(e * q)):
                    e = d
                    d = p / q
                else:
                    d = xm
                    e = d
            else:
                d = xm
                e = d

            a, fa = b, fb
            if abs(d) > tol1:
                b += d
            else:
                b += tol1 if xm > 0 else -tol1

            fb = f(b)

        return b, table, headers, max_iter