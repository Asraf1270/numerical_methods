"""Abstract base classes for all methods."""

from abc import ABC, abstractmethod


class BaseNumericalMethod(ABC):
    """Common contract every method (root-finding OR interpolation) must follow."""
    name: str = "Unnamed Method"
    description: str = ""
    category: str = "general"       # "root_finding" | "interpolation"
    input_spec: list = []           # list of (key, prompt, type)

    @abstractmethod
    def solve(self, params: dict, tol: float, max_iter: int):
        """
        Returns: (answer, table, headers, extra_info_dict)

        For root finders   : answer = root, tol/max_iter meaningful
        For interpolators  : answer = value at query point (or polynomial coefs),
                             tol/max_iter ignored
        """
        raise NotImplementedError


# Convenience alias — existing root methods inherit from this
class NumericalMethod(BaseNumericalMethod):
    category = "root_finding"