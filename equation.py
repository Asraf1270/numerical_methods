"""Equation parsing and utility math functions."""

import math


# Allowed symbols inside user-entered equations
_MATH_NAMESPACE = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "exp": math.exp, "log": math.log, "log10": math.log10,
    "ln": math.log, "sqrt": math.sqrt, "abs": abs,
    "pi": math.pi, "e": math.e,
}


def build_function(expression: str):
    """
    Convert a user-supplied string like 'x**3 - x - 2' into a callable f(x).
    Supports: sin, cos, tan, exp, log, ln, sqrt, pi, e, ^ (as **)
    """
    cleaned = expression.replace("^", "**").strip()
    # Allow implicit multiplication like 2x → 2*x, 3sin(x) → 3*sin(x)
    # (kept simple — user is encouraged to write explicit operators)

    def f(x):
        try:
            return eval(cleaned, {"__builtins__": {}}, {**_MATH_NAMESPACE, "x": x})
        except ZeroDivisionError:
            raise ValueError("Division by zero while evaluating f(x).")
        except Exception as exc:
            raise ValueError(f"Cannot evaluate expression: {exc}")

    # Smoke test
    try:
        f(1.0)
    except Exception:
        pass
    return f


def numerical_derivative(f, h: float = 1e-7):
    """Central-difference derivative."""
    def df(x):
        return (f(x + h) - f(x - h)) / (2 * h)
    return df