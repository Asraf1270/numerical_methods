"""Newton-Raphson Method."""

from .base import NumericalMethod
from equation import numerical_derivative


class NewtonRaphson(NumericalMethod):
    name = "Newton-Raphson Method"
    description = "Uses tangent line: x_new = x - f(x)/f'(x)."
    input_spec = [
        ("x0", "Initial guess x0", float),
    ]

    def solve(self, f, params, tol, max_iter):
        x = params["x0"]
        df = numerical_derivative(f)

        headers = ["Iter", "x", "f(x)", "f'(x)", "x_new", "Error"]
        table = []

        for i in range(1, max_iter + 1):
            fx = f(x)
            dfx = df(x)

            if dfx == 0:
                raise ValueError("Derivative is zero; method fails.")

            x_new = x - fx / dfx
            error = abs(x_new - x)
            table.append([i, x, fx, dfx, x_new, error])

            if error < tol or abs(f(x_new)) < tol:
                return x_new, table, headers, i
            x = x_new

        return x_new, table, headers, max_iter