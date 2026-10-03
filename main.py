"""
Entry point. Run with:  python main.py
Flow:  select category → select method → provide inputs → results + report
"""

import sys
from config import DEFAULT_TOLERANCE, DEFAULT_MAX_ITER
from equation import build_function
from methods import AVAILABLE_METHODS, methods_by_category
from ui import (
    CATEGORIES, print_category_menu, print_method_menu,
    collect_inputs, print_table, prompt_str, prompt_float, prompt_int,
)
from reporter import save_report


def _needs_equation(method):
    return method.category == "root_finding"


def run_method(method):
    print(f"\n--- {method.name} ---")

    # 1. Equation (root-finding only)
    eq_str = None
    f = None
    if _needs_equation(method):
        print("  Use 'x' as variable. Example: x**3 - x - 2  OR  cos(x) - x")
        eq_str = prompt_str("Enter f(x)")
        try:
            f = build_function(eq_str)
            f(1.0)
        except ValueError as e:
            print(f"  [!] {e}")
            return
    else:
        print("  Note: This method works on data points, no equation needed.")

    # 2. Method-specific inputs
    try:
        params = collect_inputs(method)
    except KeyboardInterrupt:
        print("\n  [!] Input cancelled.")
        return

    # 3. Global settings (root-finding only)
    tol, max_iter = 0.0, 0
    if _needs_equation(method):
        tol = prompt_float("Tolerance", default=DEFAULT_TOLERANCE)
        max_iter = prompt_int("Max iterations", default=DEFAULT_MAX_ITER)

    # 4. Solve
    try:
        answer, table, headers, extras = method.solve(params, tol, max_iter)
    except ValueError as e:
        print(f"\n  [!] {e}")
        return

    # 5. Display
    print(f"\n>>> {method.name} — Results <<<")
    print_table(headers, table)

    print("\n  FINAL RESULT:")
    print(f"    Answer : {answer}")
    if isinstance(extras, dict):
        for k, v in extras.items():
            if isinstance(v, list):
                print(f"    {k}:")
                for row in v:
                    print("       " + "  ".join(
                        f"{x:>10.6f}" if isinstance(x, float) else str(x) for x in row
                    ))
            elif isinstance(v, float):
                print(f"    {k}: {v:.10f}")
            else:
                print(f"    {k}: {v}")

    # 6. Save report
    inputs = {}
    if eq_str:
        inputs["f(x)"] = eq_str
    inputs.update(params)
    if _needs_equation(method):
        inputs["Tolerance"] = tol
        inputs["Max iterations"] = max_iter

    path = save_report(
        method_name=f"{method.category}/{method.name}",
        equation=eq_str or "(not applicable)",
        inputs=inputs,
        headers=headers,
        table=table,
        root=answer if isinstance(answer, (int, float)) else 0.0,
        iterations=len(table),
        extras=extras,
    )
    print(f"\n  [✓] Report saved → {path}")


def main():
    if not AVAILABLE_METHODS:
        print("No methods registered. Check the methods/ folder.")
        sys.exit(1)

    while True:
        print_category_menu()
        choice = input("  Select a category [0 to exit]: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            return

        try:
            cat_idx = int(choice) - 1
            if not (0 <= cat_idx < len(CATEGORIES)):
                raise ValueError
        except ValueError:
            print("  [!] Invalid selection.")
            continue

        category_key, category_label = CATEGORIES[cat_idx]
        methods = methods_by_category(category_key)

        if not methods:
            print(f"  [!] No methods registered under '{category_label}'.")
            continue

        while True:
            print_method_menu(category_label, methods)
            pick = input("  Select a method [0 to go back]: ").strip()

            if pick == "0":
                break

            try:
                m_idx = int(pick) - 1
                if not (0 <= m_idx < len(methods)):
                    raise ValueError
            except ValueError:
                print("  [!] Invalid selection.")
                continue

            try:
                run_method(methods[m_idx])
            except KeyboardInterrupt:
                print("\n  [!] Interrupted.")
            input("\n  Press Enter to return to methods list...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Exiting…")