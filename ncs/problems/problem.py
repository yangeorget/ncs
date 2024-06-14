from typing import Dict, List, Optional, Set

import numpy as np
from numpy.typing import NDArray

from ncs.propagators.propagator import Propagator

MIN = 0
MAX = 1


class Problem:
    """
    A problem is defined by a list of variable domains and a list of propagators.
    """

    def __init__(self, shr_domains: NDArray, dom_indices: List[int], dom_offsets: List[int], propagators=None):
        self.shr_domains = shr_domains
        self.size = len(dom_indices)
        self.dom_indices = np.array(dom_indices)
        self.dom_offsets = np.array(dom_offsets)
        self.propagators = propagators if propagators is not None else []

    def get_domains(self) -> NDArray:
        """
        Returns the domains of the problem variables.
        :return: an NDArray
        """
        return self.shr_domains[self.dom_indices] + self.dom_offsets.reshape(self.size, 1)

    def is_not_instantiated(self, var_idx: int) -> bool:
        """
        Returns a boolean indicating if a variable is not instantiated.
        :param var_idx: the index of the variable
        :return: True iff the variable is not instantiated
        """
        var_domain = self.dom_indices[var_idx]
        return bool(self.shr_domains[var_domain, MIN] < self.shr_domains[var_domain, MAX])

    def is_inconsistent(self) -> bool:
        """
        Returns true iff the problem is consistent.
        :return: a boolean
        """
        return np.any(np.greater(self.shr_domains[:, MIN], self.shr_domains[:, MAX]))  # type: ignore

    def is_not_solved(self) -> bool:
        """
        Returns true iff the problem is not solved.
        :return: a boolean
        """
        return np.any(np.not_equal(self.shr_domains[:, MIN], self.shr_domains[:, MAX]))  # type: ignore

    def __str__(self) -> str:
        return f"domains={self.shr_domains}, propagators={self.propagators}"

    def filter(self, changes: Optional[NDArray] = None, statistics: Optional[Dict] = None) -> bool:
        """
        Filters the problem's domains by applying the propagators until a fix point is reached.
        :param changes: an array of boolean describing the variable domain changes
        :param statistics: where to record the statistics of the computation
        :return: False if the problem is not consistent
        """
        if statistics is not None:
            statistics["problem.filters.nb"] += 1
        propagators_to_filter: Set[Propagator] = set()
        self.update_propagators_to_filter(propagators_to_filter, changes, None)
        while len(propagators_to_filter) > 0:
            propagator = propagators_to_filter.pop()
            if statistics is not None:
                statistics["problem.propagators.filters.nb"] += 1
            new_changes = self.update_domains(propagator)
            if new_changes is None:
                return False
            self.update_propagators_to_filter(propagators_to_filter, new_changes, propagator)
        return True

    def update_domains(self, propagator: Propagator) -> Optional[NDArray]:
        """
        Updates problem variable domains.
        :param propagator: a propagator
        :return: a boolean array of variable changes
        """
        prop_offsets = self.dom_offsets[propagator.variables]  # TODO: could be computed at init time
        prop_indices = self.dom_indices[propagator.variables]  # TODO: could be computed at init time
        prop_domains = self.shr_domains[prop_indices] + prop_offsets.reshape(propagator.size, 1)
        new_prop_domains = propagator.compute_domains(prop_domains)

        if new_prop_domains is None:
            return None
        # TODO: compute changes here
        self.shr_domains[prop_indices, MIN] = np.maximum(new_prop_domains[:, MIN], prop_domains[:, MIN]) - prop_offsets
        self.shr_domains[prop_indices, MAX] = np.minimum(new_prop_domains[:, MAX], prop_domains[:, MAX]) - prop_offsets
        if self.is_inconsistent():
            return None
        prop_changes = np.full((propagator.size, 2), False)
        np.greater(new_prop_domains[:, MIN], prop_domains[:, MIN], out=prop_changes[:, MIN])
        np.less(new_prop_domains[:, MAX], prop_domains[:, MAX], out=prop_changes[:, MAX])
        shr_changes = np.full((len(self.shr_domains), 2), False)
        shr_changes[prop_indices] = prop_changes
        return shr_changes[self.dom_indices]

    def update_propagators_to_filter(
        self, propagators_to_filter: Set[Propagator], changes: Optional[NDArray], last_propagator: Optional[Propagator]
    ) -> None:
        for propagator in self.propagators:
            if last_propagator and propagator == last_propagator:
                continue
            if changes is not None and not propagator.should_update(changes):
                continue
            propagators_to_filter.add(propagator)
