import argparse
from pprint import pprint

import numpy as np
import pytest

from nucs.memory import MIN
from nucs.problems.golomb_problem import GolombProblem, index, init_domains
from nucs.solvers.backtrack_solver import BacktrackSolver
from nucs.statistics import get_statistics


class TestGolomb:

    @pytest.mark.parametrize(
        "mark_nb,i,j,idx", [(4, 0, 1, 0), (4, 0, 2, 1), (4, 0, 3, 2), (4, 1, 2, 3), (4, 1, 3, 4), (4, 2, 3, 5)]
    )
    def test_index(self, mark_nb: int, i: int, j: int, idx: int) -> None:
        assert index(mark_nb, i, j) == idx

    def test_init_domains(self) -> None:
        domains = init_domains(6, 4)
        assert domains[:, MIN].tolist() == [1, 3, 6, 1, 3, 1]

    def test_golomb_4_filter(self) -> None:
        problem = GolombProblem(4)
        problem.shr_domains_lst[0] = 1
        problem.shr_domains_lst[1] = 4
        problem.shr_domains_lst[2] = 6
        problem.shr_domains_lst[3] = 3
        problem.shr_domains_lst[4] = 5
        problem.shr_domains_lst[5] = 2
        assert problem.filter(np.ones((6, 2), dtype=bool))

    @pytest.mark.parametrize("mark_nb,solution_nb", [(4, 6), (5, 11), (6, 17), (7, 25), (8, 34), (9, 44)])
    def test_golomb(self, mark_nb: int, solution_nb: int) -> None:
        problem = GolombProblem(mark_nb)
        solver = BacktrackSolver(problem)
        solution = solver.minimize(problem.length_idx)
        assert solution
        assert solution[problem.length_idx] == solution_nb


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args()
    problem = GolombProblem(args.n)
    solver = BacktrackSolver(problem)
    solution = solver.minimize(problem.length_idx)
    pprint(get_statistics(problem.statistics))
    print(solution)
    print(solution[problem.length_idx])  # type: ignore
