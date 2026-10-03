"""Shared helpers for interpolation methods."""


def parse_points(text: str):
    """
    Parse 'x1,y1 x2,y2 ...' or 'x1,y1; x2,y2; ...' or newline-separated
    into two lists xs, ys. Raises ValueError with a helpful message.
    """
    raw = text.replace(";", " ").replace("\n", " ").strip()
    tokens = [t for t in raw.split() if t]

    xs, ys = [], []
    for tok in tokens:
        if "," not in tok:
            raise ValueError(f"Invalid point '{tok}'. Use format x,y.")
        x_str, y_str = tok.split(",", 1)
        try:
            xs.append(float(x_str))
            ys.append(float(y_str))
        except ValueError:
            raise ValueError(f"Cannot parse numbers from '{tok}'.")

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