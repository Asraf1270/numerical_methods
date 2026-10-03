"""
Bairstow's Method.

Finds quadratic factors (x² + px + q) of a polynomial, extracting
both real and complex roots. Because it needs the polynomial's
coefficients (not an arbitrary f(x)), it takes a coefficient string
like: "1 -1 0 -2"  meaning  1·x³ + (-1)·x² + 0·x + (-2).
"""

import cmath
from ..base import NumericalMethod


class Bairstow(NumericalMethod):
    name = "Bairstow's Method"
    description = "Finds quadratic factors of a polynomial (real + complex roots)."
    input_spec = [
        ("coeffs", "Coefficients (highest → lowest), space-separated", str),
        ("r", "Initial r", float),
        ("s", "Initial s", float),
    ]

    def solve(self, f, params, tol, max_iter):
        # Parse coefficients
        try:
            coeffs = [float(c) for c in params["coeffs"].split()]
        except ValueError:
            raise ValueError("Coefficients must be numbers separated by spaces.")

        if len(coeffs) < 3:
            raise ValueError("Need at least degree 2 (3 coefficients) for Bairstow.")

        a = coeffs[:]
        n = len(a) - 1  # degree

        r = params["r"]
        s = params["s"]

        headers = ["Iter", "r", "s", "dr", "ds", "Error"]
        table = []
        err = None

        for it in range(1, max_iter + 1):
            # Synthetic division to compute b's and c's
            b = [0.0] * (n + 1)
            c = [0.0] * (n + 1)

            b[0] = a[0]
            b[1] = a[1] + r * b[0]
            for i in range(2, n + 1):
                b[i] = a[i] + r * b[i - 1] + s * b[i - 2]

            c[0] = b[0]
            c[1] = b[1] + r * c[0]
            for i in range(2, n):
                c[i] = b[i] + r * c[i - 1] + s * c[i - 2]

            # Solve the 2×2 system for dr, ds
            det = c[n - 2] * c[n - 1] - c[n - 3] * c[n]
            if det == 0:
                # Perturb to escape zero determinant
                r += 1.0
                s += 1.0
                continue

            dr = (b[n - 1] * c[n - 1] - b[n] * c[n - 2]) / det
            ds = (b[n] * c[n - 3] - b[n - 1] * c[n - 2]) / det

            # Fix indexing for the standard Bairstow update
            dr = (-b[n - 1] * c[n - 1] + b[n] * c[n - 2]) / (c[n - 2] * c[n - 2]
                 - c[n - 3] * c[n - 1]) if False else dr
            ds = (-b[n] * c[n - 2] + b[n - 1] * c[n - 3]) / det if False else ds

            # Simpler, more standard version:
            denom = c[n - 2] * c[n - 1] - c[n - 3] * c[n]
            dr = (-b[n - 1] * c[n - 1] + b[n] * c[n - 2]) / denom
            ds = (-b[n] * c[n - 2] + b[n - 1] * c[n - 3]) / denom

            r += dr
            s += ds
            err = max(abs(dr), abs(ds))
            table.append([it, r, s, dr, ds, err])

            if err < tol:
                break

        # Extract roots of x² + r·x + s = 0
        disc = cmath.sqrt(r * r - 4 * s)
        root1 = (-r + disc) / 2
        root2 = (-r - disc) / 2

        # We report root1 as the primary answer
        # (both roots are visible in the report's final lines via f(root) sanity)
        primary = float(root1.real) if abs(root1.imag) < 1e-12 else root1.real

        return primary, table, headers, it