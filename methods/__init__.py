"""
Auto-discovers every BaseNumericalMethod subclass in this package
(recursively, including sub-packages like root_finding/ and interpolation/).
"""

import importlib
import inspect
import pkgutil
from pathlib import Path

from .base import BaseNumericalMethod


def _discover_methods():
    registry = []
    package_dir = Path(__file__).parent

    # Walk every module in methods/ and its subpackages
    for _, module_name, is_pkg in pkgutil.walk_packages(
        [str(package_dir)], prefix=__name__ + "."
    ):
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

    # De-duplicate by name
    seen, unique = set(), []
    for m in registry:
        if m.name not in seen:
            seen.add(m.name)
            unique.append(m)
    return unique


AVAILABLE_METHODS = _discover_methods()


def methods_by_category(category: str):
    return [m for m in AVAILABLE_METHODS if m.category == category]