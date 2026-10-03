A professional, terminal-based Python application that solves root-finding problems using **10 classical numerical methods**. Built with a clean, extensible architecture where every method lives in its own file and is auto-discovered at runtime.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![PRs](https://img.shields.io/badge/PRs-Welcome-orange)

---

## ✨ Features

- 🎯 **10 numerical methods** out of the box
- 🖥️ **Terminal-based** — zero GUI dependencies
- 🔌 **Plugin architecture** — add a new method in one file, no edits elsewhere
- 📊 **Iteration tables** with error tracking displayed live
- 💾 **Auto-saves unique reports** (`results/<Method>_<timestamp>.txt`) with equation, inputs, table, and final answer
- 🧮 **Safe equation parser** — supports `sin`, `cos`, `exp`, `log`, `sqrt`, `pi`, `e`, `^` as `**`, and more
- 🔢 **Numerical derivative** — Newton-Raphson needs no manual derivative input
- 🧩 **Fully typed & modular** — clean separation between UI, algorithms, and I/O

---

## Run

Python 3.9 or newer is required. The application uses only the Python standard library; no packages need to be installed.

From the project directory, start the interactive menu with:

```bash
python main.py
```

Choose a method by its menu number, enter the equation and requested starting values, then provide a tolerance and iteration limit. The defaults are `1e-4` and `50`. Enter `0` at the menu to exit.

## Available methods

| Method | Values requested |
| --- | --- |
| Bisection Method | Lower and upper bounds `a`, `b` |
| False Position Method | Lower and upper bounds `a`, `b` |
| Illinois False Position | Lower and upper bounds `a`, `b` |
| Brent's Method | Lower and upper bounds `a`, `b` |
| Newton-Raphson Method | Initial guess `x0` |
| Secant Method | Initial guesses `x0`, `x1` |
| Mullers Method | Initial guesses `x0`, `x1`, `x2` |
| Fixed Point Iteration | Iteration function `g(x)` and initial guess `x0` |
| Steffensen's Method | Iteration function `g(x)` and initial guess `x0` |
| Bairstow's Method | Polynomial coefficients and initial `r`, `s` |

The bracketing methods require `f(a)` and `f(b)` to have opposite signs. Fixed Point Iteration and Steffensen's Method ask for `g(x)` where the desired root satisfies `x = g(x)`. Bairstow's Method uses polynomial coefficients in descending powers, separated by spaces. For example, `1 -1 0 -2` represents `x**3 - x**2 - 2`; it reports a primary root approximation from the quadratic factor it finds.

## Entering equations

Use `x` for the variable and Python-style arithmetic operators: `+`, `-`, `*`, `/`, and `**` for powers. A caret is also converted to exponentiation, so `x^2` works. Examples:

```text
x**3 - x - 2
cos(x) - x
sqrt(x) - 2
```

Supported functions include `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `exp`, `log` (natural logarithm), `ln`, `log10`, `sqrt`, and `abs`. The constants `pi` and `e` are available. Write multiplication explicitly, for example `2*x` rather than `2x`.

## Results

Each successful run prints the approximate root, iteration count, and function value at the root. A report is also saved under `results/` with the method name and a timestamp in its filename. Reports include the entered inputs, iteration table, and final root approximation. The `results/` directory is created automatically when the first report is saved.

## Project layout

```text
main.py       Interactive application entry point
equation.py   Equation parsing and numerical derivative helper
methods/      Numerical method implementations and auto-discovery
reporter.py   Timestamped text report writer
results/      Generated run reports
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Asraf1270/numerical_methods.git
cd numerical_methods
```

Then start the application:

```bash
python main.py
```

## 🧩 Adding a New Method

The framework discovers `NumericalMethod` subclasses in the `methods/` package automatically. Create `methods/your_method.py`:

```python
from .base import NumericalMethod

class YourMethod(NumericalMethod):
    name = "Your Method Name"
    description = "One-line description shown in the menu."
    input_spec = [
        ("x0", "Initial guess", float),
        ("x1", "Second guess", float),
    ]

    def solve(self, f, params, tol, max_iter):
        # params["x0"], params["x1"], etc.
        root = ...
        table = [[i, ..., error], ...]
        headers = ["Iter", "x0", "x1", "Error"]
        iterations = ...
        return root, table, headers, iterations
```

The `solve` method returns `(root, table, headers, iterations)`. The `input_spec` entries define the values requested from the user. The method is then discovered automatically, displayed in the menu, and handled by the existing UI and report writer.

## 🤝 Contributing

Contributions are welcome! To add a new method:

- Fork the repository.
- Create a file in `methods/` following the pattern above.
- Run the application with `python main.py` and try the new method.
- Submit a pull request.

Please keep the style consistent with existing methods: use type hints where helpful, write descriptive docstrings, choose clear variable names, and raise `ValueError` with a helpful message when inputs are invalid.

## 📜 License

This project is licensed under the MIT License — see the LICENSE file for details.

## ⭐ Show Your Support

If this project helped you, please give it a star ⭐ — it helps others find it!

Built with ❤️ for students, engineers, and anyone learning numerical methods.
