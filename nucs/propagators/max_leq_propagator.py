import numpy as np
from numba import njit  # type: ignore
from numpy.typing import NDArray

from nucs.memory import MAX, MIN, PROP_CONSISTENCY, PROP_ENTAILMENT, PROP_INCONSISTENCY, new_triggers


def get_triggers_max_leq(n: int, data: NDArray) -> NDArray:
    """
    Returns the triggers for this propagator.
    :param n: the number of variables
    :return: an array of triggers
    """
    triggers = new_triggers(n, False)
    for i in range(n - 1):
        triggers[i, MIN] = True
    triggers[-1, MAX] = True
    return triggers


@njit(cache=True)
def compute_domains_max_leq(domains: NDArray, data: NDArray) -> int:
    """
    Implements Max_i x_i <= x_{n-1}.
    :param domains: the domains of the variables
    :param data: unused here
    """
    x = domains[:-1]
    y = domains[-1]
    if np.max(x[:, MAX]) <= y[MIN]:
        return PROP_ENTAILMENT
    y[MIN] = max(y[MIN], np.max(x[:, MIN]))
    if y[MIN] > y[MAX]:
        return PROP_INCONSISTENCY
    for i in range(len(x)):
        x[i, MAX] = min(x[i, MAX], y[MAX])
        if x[i, MAX] < x[i, MIN]:
            return PROP_INCONSISTENCY
    return PROP_CONSISTENCY
