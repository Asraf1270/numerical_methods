"""Shared helpers for interpolation methods."""

import re


def parse_points(text: str):
    """
    Parse data points in styles like '(x1, y1), (x2, y2), ...',
    'x1,y1 x2,y2 ...', or 'x1, y1; x2, y2; ...' into two lists xs, ys.
    Raises ValueError with a helpful message.
    """
    if text is None:
        raise ValueError("Data points input is required.")

    numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", str(text))
    if len(numbers) < 2 or len(numbers) % 2 != 0:
        raise ValueError(
            "Invalid point format. Use '(x1, y1), (x2, y2), ...' or 'x1,y1 x2,y2 ...'."
        )

    xs, ys = [], []
    for i in range(0, len(numbers), 2):
        try:
            xs.append(float(numbers[i]))
            ys.append(float(numbers[i + 1]))
        except ValueError as exc:
            raise ValueError(f"Cannot parse numbers from '{text}'.") from exc

    if len(xs) < 2:
        raise ValueError("Need at least 2 data points.")

    # Sort by x (safe for Lagrange & divided difference;
    # for forward/backward, we keep order but users should input sorted)
    pairs = sorted(zip(xs, ys))
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    return xs, ys


def is_equally_spaced(xs, tol=1e-9):
    if len(xs) < 2:
        return False
    h = xs[1] - xs[0]
    for i in range(2, len(xs)):
        if abs((xs[i] - xs[i - 1]) - h) > tol:
            return False
    return True


def forward_diff_table(ys):
    """Return upper-triangular forward difference table."""
    n = len(ys)
    table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        table[i][0] = ys[i]
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
    return table


def backward_diff_table(ys):
    """Return upper-triangular backward difference table (∇)."""
    n = len(ys)
    table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        table[i][0] = ys[i]
    for j in range(1, n):
        for i in range(j, n):
            table[i][j] = table[i][j - 1] - table[i - 1][j - 1]
    return table


def divided_diff_table(xs, ys):
    """Return divided difference table (first row = coefficients)."""
    n = len(xs)
    table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        table[i][0] = ys[i]

    for j in range(1, n):
        for i in range(n - j):
            if xs[i + j] - xs[i] == 0:
                raise ValueError("Duplicate x-values not allowed.")
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (xs[i + j] - xs[i])

    return table