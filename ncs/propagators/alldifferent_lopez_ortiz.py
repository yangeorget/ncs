from typing import List, Optional

import numpy as np
from numpy.typing import NDArray

from ncs.problems.problem import MAX, MIN
from ncs.propagators.propagator import Propagator

MIN_RANK = 2
MAX_RANK = 3


class AlldifferentLopezOrtiz(Propagator):
    def compute_domains(self, domains: NDArray) -> Optional[NDArray]:
        bound_len = 2 * self.size + 2
        bounds = [0] * bound_len
        t = [0] * bound_len
        d = [0] * bound_len
        h = [0] * bound_len
        rank_domains = np.zeros((self.size, 4), dtype=int)
        rank_domains[:, [MIN, MAX]] = domains.copy()
        min_sorted_vars = np.argsort(rank_domains[:, MIN])
        max_sorted_vars = np.argsort(rank_domains[:, MAX])
        nb = self.compute_nb(rank_domains, min_sorted_vars, max_sorted_vars, bounds)
        if not self.filter_lower(nb, t, d, h, bounds, rank_domains, max_sorted_vars):
            return None
        if not self.filter_upper(nb, t, d, h, bounds, rank_domains, min_sorted_vars):
            return None
        return rank_domains[:, [MIN, MAX]]

    def compute_nb(
        self, rank_domains: NDArray, min_sorted_vars: NDArray, max_sorted_vars: NDArray, bounds: List[int]
    ) -> int:
        min = rank_domains[min_sorted_vars[0], MIN]
        max = rank_domains[max_sorted_vars[0], MAX] + 1
        bounds[0] = last = min - 2
        i = j = nb = 0
        while True:
            if i < self.size and min <= max:
                if min != last:
                    nb += 1
                    bounds[nb] = last = min
                rank_domains[min_sorted_vars[i], MIN_RANK] = nb
                i += 1
                if i < self.size:
                    min = rank_domains[min_sorted_vars[i], MIN]
            else:
                if max != last:
                    nb += 1
                    bounds[nb] = last = max
                rank_domains[max_sorted_vars[j], MAX_RANK] = nb
                j += 1
                if j == self.size:
                    break
                max = rank_domains[max_sorted_vars[j], MAX] + 1
        bounds[nb + 1] = bounds[nb] + 2
        return nb

    def filter_lower(
        self,
        nb: int,
        t: List[int],
        d: List[int],
        h: List[int],
        bounds: List[int],
        rank_domains: NDArray,
        max_sorted_vars: NDArray,
    ) -> bool:
        for i in range(0, nb + 1):
            t[i + 1] = h[i + 1] = i
            d[i + 1] = bounds[i + 1] - bounds[i]
        for i in range(0, self.size):
            x = rank_domains[max_sorted_vars[i], MIN_RANK]
            y = rank_domains[max_sorted_vars[i], MAX_RANK]
            z = self.path_max(t, x + 1)
            j = t[z]
            d[z] -= 1
            if d[z] == 0:
                t[z] = z + 1
                z = self.path_max(t, t[z])
                t[z] = j
            self.path_set(t, x + 1, z, z)  # path compression
            if d[z] < bounds[z] - bounds[y]:
                return False
            if h[x] > x:
                w = self.path_max(h, h[x])
                rank_domains[max_sorted_vars[i], MIN] = bounds[w]
                self.path_set(h, x, w, w)  # path compression
            if d[z] == bounds[z] - bounds[y]:
                self.path_set(h, h[y], j - 1, y)  # mark hall interval
                h[y] = j - 1  # hall interval[bounds[j], bounds[y]]
        return True

    def filter_upper(
        self,
        nb: int,
        t: List[int],
        d: List[int],
        h: List[int],
        bounds: List[int],
        rank_domains: NDArray,
        min_sorted_vars: NDArray,
    ) -> bool:
        for i in range(0, nb + 1):
            t[i] = h[i] = i + 1
            d[i] = bounds[i + 1] - bounds[i]
        for i in range(self.size - 1, -1, -1):
            x = rank_domains[min_sorted_vars[i], MAX_RANK]
            y = rank_domains[min_sorted_vars[i], MIN_RANK]
            z = self.path_min(t, x - 1)
            j = t[z]
            d[z] -= 1
            if d[z] == 0:
                t[z] = z - 1
                z = self.path_min(t, t[z])
                t[z] = j
            self.path_set(t, x - 1, z, z)  # path compression
            if d[z] < bounds[y] - bounds[z]:
                return False
            if h[x] < x:
                w = self.path_min(h, h[x])
                rank_domains[min_sorted_vars[i], MAX] = bounds[w] - 1
                self.path_set(h, x, w, w)  # path compression
            if d[z] == bounds[y] - bounds[z]:
                self.path_set(h, h[y], j + 1, y)  # mark hall interval
                h[y] = j + 1  # hall interval[bounds[j], bounds[y]]
        return True

    def path_set(self, t: List[int], start: int, end: int, to: int) -> None:
        p = start
        while p != end:
            tmp = t[p]
            t[p] = to
            p = tmp

    def path_min(self, t: List[int], i: int) -> int:
        while t[i] < i:
            i = t[i]
        return i

    def path_max(self, t: List[int], i: int) -> int:
        while t[i] > i:
            i = t[i]
        return i
