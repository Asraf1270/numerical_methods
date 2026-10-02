"""Saves complete run data to a unique .txt report."""

import os
from datetime import datetime

from config import RESULTS_DIR, FLOAT_PRECISION


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.{FLOAT_PRECISION}f}"
    return str(v)


def save_report(method_name, equation, inputs, headers, table, root, iterations):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = method_name.replace(" ", "_")
    filename = os.path.join(RESULTS_DIR, f"{safe_name}_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as fh:
        line = "=" * 72
        fh.write(line + "\n")
        fh.write("  NUMERICAL METHOD REPORT\n")
        fh.write(line + "\n")
        fh.write(f"Method       : {method_name}\n")
        fh.write(f"Date & Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"Equation     : f(x) = {equation}\n")
        fh.write("-" * 72 + "\n")
        fh.write("INPUT DATA\n")
        for k, v in inputs.items():
            fh.write(f"  {k:<15}: {v}\n")
        fh.write("-" * 72 + "\n")
        fh.write("ITERATION TABLE\n")
        fh.write("-" * 72 + "\n")

        widths = []
        for col in range(len(headers)):
            col_width = max(len(str(headers[col])),
                            max((len(_fmt(r[col])) for r in table), default=0))
            widths.append(min(col_width, 16))

        fh.write(" | ".join(f"{h:^{w}}" for h, w in zip(headers, widths)) + "\n")
        fh.write("-" * 72 + "\n")
        for row in table:
            fh.write(" | ".join(f"{_fmt(v):^{w}}" for v, w in zip(row, widths)) + "\n")

        fh.write("-" * 72 + "\n")
        fh.write("FINAL RESULT\n")
        fh.write(f"  Root approximation : {root:.{FLOAT_PRECISION}f}\n")
        fh.write(f"  Iterations used    : {iterations}\n")
        fh.write(line + "\n")

    return filename