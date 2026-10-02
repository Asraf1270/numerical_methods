"""Abstract base class for every numerical method."""

from abc import ABC, abstractmethod


class NumericalMethod(ABC):
    """
    Every numerical method must inherit this class and implement:
        - name          : display name (str)
        - input_spec    : list of (key, prompt, type) for interactive input
        - solve(...)    : the actual algorithm
    """

    name: str = "Unnamed Method"
    # Each entry: (input_key, prompt_text, python_type)
    input_spec: list = []

    @abstractmethod
    def solve(self, f, params: dict, tol: float, max_iter: int):
        """
        Return (root, table, headers, iterations).

        f        : callable, user equation
        params   : dict of user-supplied inputs (keys match input_spec)
        tol      : tolerance
        max_iter : max iterations
        """
        raise NotImplementedError