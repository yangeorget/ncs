import numpy as np

from ncs.problems.problem import Problem
from ncs.propagators.propagator import Propagator


class QueensProblem(Problem):

    def __init__(self, n: int):
        super().__init__([(0, n - 1)] * n, list(range(0, n)) * 3, [0] * n + list(range(0, n)) + list(range(0, -n, -1)))
        self.n = n
        self.add_propagator(Propagator(np.array(list(range(0, n)), dtype=np.int32), "alldifferent_lopez_ortiz"))
        self.add_propagator(Propagator(np.array(list(range(n, 2 * n)), dtype=np.int32), "alldifferent_lopez_ortiz"))
        self.add_propagator(Propagator(np.array(list(range(2 * n, 3 * n)), dtype=np.int32), "alldifferent_lopez_ortiz"))