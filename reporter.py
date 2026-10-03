"""Saves a complete report to a unique .txt file."""

import os
from datetime import datetime

from config import RESULTS_DIR, FLOAT_PRECISION


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.{FLOAT_PRECISION}f}"
    return str(v)


def save_report(method_name, equation, inputs, headers, table, root, iterations, extras=None):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe = method_name.replace("/", "_").replace(" ", "_")
    filename = os.path.join(RESULTS_DIR, f"{safe}_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as fh:
        line = "=" * 72
        fh.write(line + "\n")
        fh.write("  NUMERICAL METHOD REPORT\n")
        fh.write(line + "\n")
        fh.write(f"Method       : {method_name}\n")
        fh.write(f"Date & Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"Equation     : {equation}\n")
        fh.write("-" * 72 + "\n")
        fh.write("INPUT DATA\n")
        for k, v in inputs.items():
            fh.write(f"  {k:<15}: {v}\n")
        fh.write("-" * 72 + "\n")
        fh.write("ITERATION / COMPUTATION TABLE\n")
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
        fh.write(f"  Answer          : {_fmt(root)}\n")
        fh.write(f"  Iterations used : {iterations}\n")

        if extras:
            fh.write("-" * 72 + "\n")
            fh.write("ADDITIONAL INFO\n")
            for k, v in extras.items():
                if isinstance(v, list):
                    fh.write(f"  {k}:\n")
                    for row in v:
                        fh.write("    " + "  ".join(_fmt(x) for x in row) + "\n")
                else:
                    fh.write(f"  {k:<22}: {_fmt(v) if isinstance(v,float) else v}\n")

        fh.write(line + "\n")

    return filename