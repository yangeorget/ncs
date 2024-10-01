import numpy as np
from numba import njit  # type: ignore
from numpy.typing import NDArray

from nucs.constants import MAX, MIN, PROP_CONSISTENCY, PROP_INCONSISTENCY
from nucs.numpy import new_triggers


def get_complexity_min_eq(n: int, parameters: NDArray) -> float:
    return 3 * n


def get_triggers_min_eq(n: int, parameters: NDArray) -> NDArray:
    """
    Returns the triggers for this propagator.
    :param n: the number of variables
    :return: an array of triggers
    """
    return new_triggers(n, True)


@njit(cache=True)
def compute_domains_min_eq(domains: NDArray, parameters: NDArray) -> int:
    """
    Implements Min_i x_i = x_{n-1}.
    :param domains: the domains of the variables, x is an alias for domains
    :param parameters: unused here
    """
    x = domains[:-1]
    y = domains[-1]
    y[MIN] = max(y[MIN], np.min(x[:, MIN]))
    y[MAX] = min(y[MAX], np.min(x[:, MAX]))
    if y[MIN] > y[MAX]:
        return PROP_INCONSISTENCY
    candidates_nb = 0
    candidate_idx = -1
    for i in range(len(x)):
        if x[i, MIN] <= y[MIN]:
            x[i, MIN] = y[MIN]
            candidate_idx = i
            candidates_nb += 1
    if candidates_nb == 1:
        x[candidate_idx, MAX] = y[MAX]
    return PROP_CONSISTENCY
