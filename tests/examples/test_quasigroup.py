import argparse
from pprint import pprint

import pytest

from nucs.problems.quasigroup_problem import Quasigroup5Problem
from nucs.solvers.backtrack_solver import BacktrackSolver
from nucs.solvers.heuristics import DOM_HEURISTIC_MIN_VALUE, VAR_HEURISTIC_SMALLEST_DOMAIN
from nucs.statistics import STATS_SOLVER_SOLUTION_NB, get_statistics


class TestQuasigroup:
    @pytest.mark.parametrize(
        "size, solution_nb",
        [
            (7, 3),
            (8, 1),
            (9, 0),
            (10, 0),
            # (11, 5),
            # (12, 0),
        ],
    )
    def test_quasigroup5(self, size: int, solution_nb: int) -> None:
        problem = Quasigroup5Problem(size)
        solver = BacktrackSolver(problem, VAR_HEURISTIC_SMALLEST_DOMAIN, DOM_HEURISTIC_MIN_VALUE)
        solver.find_all()
        assert problem.statistics[STATS_SOLVER_SOLUTION_NB] == solution_nb


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args()
    problem = Quasigroup5Problem(args.n)
    solver = BacktrackSolver(problem, VAR_HEURISTIC_SMALLEST_DOMAIN, DOM_HEURISTIC_MIN_VALUE)
    solver.find_all()
    pprint(get_statistics(problem.statistics))
