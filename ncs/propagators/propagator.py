from typing import List, Optional

import numpy as np
from numpy.typing import NDArray


class Propagator:
    """
    Abstraction for a bound-consistency algorithm.
    """

    def __init__(self, variables: List[int]):
        self.size = len(variables)
        self.variables = np.array(variables)
        self.triggers = np.ones((self.size, 2), dtype=bool)

    def compute_domains(self, domains: NDArray) -> Optional[NDArray]:
        """
        Computes new domains for the variables
        :param domains: the initial domains
        :return: the new domains or None if there is an inconsistency
        """
        return None

    def should_update(self, changes: NDArray) -> bool:
        return bool(np.any(changes[self.variables] & self.triggers))
