from typing import Optional

from numba import jit  # type: ignore
from numpy.typing import NDArray


@jit(nopython=True, nogil=True)
def compute_domains(domains: NDArray) -> Optional[NDArray]:
    return domains.copy()
