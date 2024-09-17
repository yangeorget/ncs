from typing import Any

import numpy as np
import pytest

from nucs.constants import PROP_CONSISTENCY, PROP_ENTAILMENT, PROP_INCONSISTENCY
from nucs.numpy import new_data_by_values, new_shr_domains_by_values
from nucs.problems.problem import Problem
from nucs.propagators.lexicographic_leq_propagator import compute_domains_lexicographic_leq
from nucs.propagators.propagators import ALG_LEXICOGRAPHIC_LEQ
from nucs.solvers.backtrack_solver import BacktrackSolver
from nucs.statistics import STATS_SOLVER_SOLUTION_NB


class TestLexicographicLEQ:
    def test_compute_domains_1(self) -> None:
        domains = new_shr_domains_by_values([(0, 1), 0, 1, 1])
        data = new_data_by_values([])
        assert compute_domains_lexicographic_leq(domains, data) == PROP_ENTAILMENT
        assert np.all(domains == np.array([[0, 1], [0, 0], [1, 1], [1, 1]]))

    def test_compute_domains_2(self) -> None:
        domains = new_shr_domains_by_values([(0, 1), (0, 1), (0, 1), (0, 1)])
        data = new_data_by_values([])
        assert compute_domains_lexicographic_leq(domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[0, 1], [0, 1], [0, 1], [0, 1]]))

    @pytest.mark.parametrize(
        "values,state",
        [
            ([0, 0, 0, 0], PROP_ENTAILMENT),
            ([0, 0, 0, 1], PROP_ENTAILMENT),
            ([0, 0, 1, 0], PROP_ENTAILMENT),
            ([0, 0, 1, 1], PROP_ENTAILMENT),
            ([0, 1, 0, 0], PROP_INCONSISTENCY),
            ([0, 1, 0, 1], PROP_ENTAILMENT),
            ([0, 1, 1, 0], PROP_ENTAILMENT),
            ([0, 1, 1, 1], PROP_ENTAILMENT),
            ([1, 0, 0, 0], PROP_INCONSISTENCY),
            ([1, 0, 0, 1], PROP_INCONSISTENCY),
            ([1, 0, 1, 0], PROP_ENTAILMENT),
            ([1, 0, 1, 1], PROP_ENTAILMENT),
            ([1, 1, 0, 0], PROP_INCONSISTENCY),
            ([1, 1, 0, 1], PROP_INCONSISTENCY),
            ([1, 1, 1, 0], PROP_INCONSISTENCY),
            ([1, 1, 1, 1], PROP_ENTAILMENT),
        ],
    )
    def test_compute_domains_values(self, values: Any, state: int) -> None:
        domains = new_shr_domains_by_values(values)
        data = new_data_by_values([])
        assert compute_domains_lexicographic_leq(domains, data) == state

    def test_solve_1(self) -> None:
        problem = Problem(
            shr_domains_list=[(0, 1), (0, 1), (0, 1), (0, 1)],
            dom_indices_list=[0, 1, 2, 3],
            dom_offsets_list=[0, 0, 0, 0],
        )
        problem.add_propagator(([0, 1, 2, 3], ALG_LEXICOGRAPHIC_LEQ, []))
        solver = BacktrackSolver(problem)
        solver.find_all()
        assert problem.statistics[STATS_SOLVER_SOLUTION_NB] == 10

    def test_solve_2(self) -> None:
        problem = Problem(
            shr_domains_list=[(1, 1), (0, 1), (0, 1), (0, 1)],
            dom_indices_list=[0, 1, 2, 3],
            dom_offsets_list=[0, 0, 0, 0],
        )
        problem.add_propagator(([0, 1, 2, 3], ALG_LEXICOGRAPHIC_LEQ, []))
        solver = BacktrackSolver(problem)
        solver.find_all()
        assert problem.statistics[STATS_SOLVER_SOLUTION_NB] == 3
