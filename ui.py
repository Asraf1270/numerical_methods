"""Terminal user interface helpers."""

from config import APP_NAME, APP_VERSION


def print_banner():
    print("\n" + "=" * 70)
    print(f"  {APP_NAME}  v{APP_VERSION}".center(70))
    print("=" * 70)


def print_menu(methods):
    print_banner()
    print("  Available Methods:\n")
    for idx, m in enumerate(methods, start=1):
        print(f"   [{idx}] {m.name}")
        print(f"        {m.description}")
    print(f"\n   [0] Exit")
    print("=" * 70)


def prompt_float(text):
    while True:
        try:
            return float(input(f"  {text}: ").strip())
        except ValueError:
            print("  [!] Please enter a valid number.")


def prompt_int(text):
    while True:
        try:
            return int(input(f"  {text}: ").strip())
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
    widths = []
    for col in range(len(headers)):
        col_width = max(len(str(headers[col])),
                        max((len(_fmt(row[col])) for row in table), default=0))
        widths.append(min(col_width, 14))

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