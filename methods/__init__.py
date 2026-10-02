"""
Auto-discovers every subclass of NumericalMethod inside this package.
To add a new method: drop a new file here with a NumericalMethod subclass.
"""

import importlib
import pkgutil
from pathlib import Path

from .base import NumericalMethod


def _discover_methods():
    registry = []
    package_dir = Path(__file__).parent

    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        if module_name in ("base", "__init__"):
            continue

        module = importlib.import_module(f"{__name__}.{module_name}")
        for attr in vars(module).values():
            if (
                isinstance(attr, type)
                and issubclass(attr, NumericalMethod)
                and attr is not NumericalMethod
            ):
                registry.append(attr())

    return registry


AVAILABLE_METHODS = _discover_methods()