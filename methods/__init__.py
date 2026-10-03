"""
Auto-discovers every BaseNumericalMethod subclass inside this package
(recursively, including sub-packages like root_finding/ and interpolation/).

To add a new method:
  - Root-finding  → drop a file in methods/root_finding/
  - Interpolation → drop a file in methods/interpolation/
  No other file needs editing.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path

from .base import BaseNumericalMethod


def _discover_methods():
    """Walk all modules under methods/ and collect concrete method instances."""
    registry = []
    package_dir = Path(__file__).parent

    for _, module_name, _ in pkgutil.walk_packages(
        [str(package_dir)], prefix=__name__ + "."
    ):
        # Skip base definitions and package markers
        if module_name.endswith(".base") or module_name.endswith(".__init__"):
            continue

        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            print(f"[!] Skipping {module_name}: {exc}")
            continue

        for attr in vars(module).values():
            if (
                isinstance(attr, type)
                and issubclass(attr, BaseNumericalMethod)
                and attr is not BaseNumericalMethod
                and getattr(attr, "name", None)
                and not inspect.isabstract(attr)
            ):
                registry.append(attr())

    # De-duplicate by method name
    seen, unique = set(), []
    for m in registry:
        if m.name not in seen:
            seen.add(m.name)
            unique.append(m)
    return unique


AVAILABLE_METHODS = _discover_methods()


def methods_by_category(category: str):
    """Return all registered methods belonging to a given category."""
    return [m for m in AVAILABLE_METHODS if m.category == category]