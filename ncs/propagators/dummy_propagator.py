import numpy as np
from numba import jit  # type: ignore
from numpy.typing import NDArray

from ncs.memory import PROP_CONSISTENCY, new_triggers


def get_triggers(n: int, data: NDArray) -> NDArray:
    """
    This propagator is triggered whenever there is a change in the domain of a variable.
    :param n: the number of variables
    :return: an array of triggers
    """
    return new_triggers(n, True)


@jit("int8(int32[::1,:], int32[:])", nopython=True, cache=True)
def compute_domains(domains: NDArray, data: NDArray) -> np.int8:
    """
    A propagator that does nothing.
    """
    return PROP_CONSISTENCY
