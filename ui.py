"""Terminal UI for the two-category application."""

from config import APP_NAME, APP_VERSION


CATEGORIES = [
    ("root_finding", "Root Finding"),
    ("interpolation", "Interpolation & Polynomial"),
]


def print_banner():
    print("\n" + "=" * 72)
    print(f"  {APP_NAME}  v{APP_VERSION}".center(72))
    print("=" * 72)


def print_category_menu():
    print_banner()
    print("  Select Category:\n")
    for idx, (_, label) in enumerate(CATEGORIES, start=1):
        print(f"   [{idx}] {label}")
    print(f"\n   [0] Exit")
    print("=" * 72)


def print_method_menu(category_label, methods):
    print(f"\n===== {category_label} =====")
    print("-" * 72)
    for idx, m in enumerate(methods, start=1):
        print(f"   [{idx}] {m.name}")
    print(f"\n   [0] Back to categories")
    print("-" * 72)


def prompt_float(text, default=None):
    suffix = f" (default {default})" if default is not None else ""
    while True:
        raw = input(f"  {text}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  [!] Please enter a valid number.")


def prompt_int(text, default=None):
    suffix = f" (default {default})" if default is not None else ""
    while True:
        raw = input(f"  {text}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  [!] Please enter a valid integer.")


def prompt_str(text):
    while True:
        val = input(f"  {text}: ").strip()
        if val:
            return val
        print("  [!] Input cannot be empty.")


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.10f}"
    return str(v)


def print_table(headers, table):
    if not table:
        print("  (no iteration rows)")
        return

    widths = []
    for col in range(len(headers)):
        col_width = max(len(str(headers[col])),
                        max((len(_fmt(row[col])) for row in table), default=0))
        widths.append(min(col_width, 16))

    header_line = " | ".join(f"{h:^{w}}" for h, w in zip(headers, widths))
    sep = "-" * len(header_line)
    print("\n" + sep)
    print(header_line)
    print(sep)
    for row in table:
        print(" | ".join(f"{_fmt(v):^{w}}" for v, w in zip(row, widths)))
    print(sep)


def collect_inputs(method):
    print(f"\n--- {method.name} : Inputs ---")
    params = {}
    for key, prompt, typ in method.input_spec:
        if typ is float:
            params[key] = prompt_float(prompt)
        elif typ is int:
            params[key] = prompt_int(prompt)
        else:
            params[key] = prompt_str(prompt)
    return params