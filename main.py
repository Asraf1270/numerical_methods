"""
Entry point. Run with:  python main.py
"""

import sys
from config import DEFAULT_TOLERANCE, DEFAULT_MAX_ITER
from equation import build_function
from methods import AVAILABLE_METHODS
from ui import (
    print_menu, collect_inputs, print_table,
    prompt_str, prompt_float, prompt_int,
)
from reporter import save_report


def run_once(method):
    # ---- 1. Equation ----
    print(f"\n--- {method.name} ---")
    print("  Use 'x' as variable. Example: x**3 - x - 2  OR  cos(x) - x")
    eq_str = prompt_str("Enter f(x)")

    try:
        f = build_function(eq_str)
        # evaluation smoke test
        f(1.0)
    except ValueError as e:
        print(f"  [!] {e}")
        return

    # ---- 2. Method-specific inputs ----
    try:
        params = collect_inputs(method)
    except KeyboardInterrupt:
        print("\n  [!] Input cancelled.")
        return

    # ---- 3. Global params ----
    tol = prompt_float(f"Tolerance (default {DEFAULT_TOLERANCE})")
    max_iter = prompt_int(f"Max iterations (default {DEFAULT_MAX_ITER})")

    # ---- 4. Solve ----
    try:
        root, table, headers, iterations = method.solve(f, params, tol, max_iter)
    except ValueError as e:
        print(f"\n  [!] {e}")
        return

    # ---- 5. Display ----
    print(f"\n>>> {method.name} — Results <<<")
    print_table(headers, table)
    print(f"\n  Approximate Root : {root:.10f}")
    print(f"  Iterations Used  : {iterations}")
    print(f"  f(root)          : {f(root):.6e}")

    # ---- 6. Save ----
    inputs = {"f(x)": eq_str, **params,
              "Tolerance": tol, "Max iterations": max_iter}
    path = save_report(method.name, eq_str, inputs, headers, table, root, iterations)
    print(f"\n  [✓] Report saved → {path}")


def main():
    if not AVAILABLE_METHODS:
        print("No methods registered. Check the methods/ folder.")
        sys.exit(1)

    while True:
        print_menu(AVAILABLE_METHODS)
        choice = input("  Select a method [0 to exit]: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            return

        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(AVAILABLE_METHODS)):
                raise ValueError
        except ValueError:
            print("  [!] Invalid selection.")
            continue

        try:
            run_once(AVAILABLE_METHODS[idx])
        except KeyboardInterrupt:
            print("\n  [!] Interrupted.")
        input("\n  Press Enter to return to the menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Exiting…")