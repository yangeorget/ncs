import numpy as np

from ncs.problems.problem import Problem
from ncs.propagators.alldifferent_puget_n2 import AlldifferentPugetN2
from ncs.propagators.sum import Sum
from ncs.solvers.backtrack_solver import BacktrackSolver


class TestBacktrackSolver:
    def test_solve_and_count(self) -> None:
        shr_domains = np.array([[0, 99], [0, 99]])
        dom_indices = [0, 1]
        dom_offsets = [0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        solver = BacktrackSolver(problem)
        for _ in solver.solve():
            pass
        assert solver.statistics["solver.solutions.nb"] == 10000
        assert solver.statistics["solver.cp.max"] == 2

    def test_solve(self) -> None:
        shr_domains = np.array([[0, 1], [0, 1]])
        dom_indices = [0, 1]
        dom_offsets = [0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert len(solutions) == 4
        assert np.all(solutions[0] == np.array([[0, 0], [0, 0]]))
        assert np.all(solutions[1] == np.array([[0, 0], [1, 1]]))
        assert np.all(solutions[2] == np.array([[1, 1], [0, 0]]))
        assert np.all(solutions[3] == np.array([[1, 1], [1, 1]]))
        assert solver.statistics["solver.solutions.nb"] == 4
        assert solver.statistics["solver.cp.max"] == 2

    def test_solve_sum_1(self) -> None:
        shr_domains = np.array([[0, 2], [0, 2], [4, 6]])
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets, [Sum([2, 0, 1])])
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert np.all(solutions == np.array([[2, 2], [2, 2], [4, 4]]))
        assert solver.statistics["solver.solutions.nb"] == 1
        assert solver.statistics["problem.filters.nb"] == 1
        assert solver.statistics["solver.cp.max"] == 0
        assert solver.statistics["solver.backtracks.nb"] == 0

    def test_solve_sum_3(self) -> None:
        shr_domains = np.array([[0, 1], [0, 1], [0, 1]])
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets, [Sum([2, 0, 1])])
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert len(solutions) == 3
        assert np.all(solutions[0] == np.array([[0, 0], [0, 0], [0, 0]]))
        assert np.all(solutions[1] == np.array([[0, 0], [1, 1], [1, 1]]))
        assert np.all(solutions[2] == np.array([[1, 1], [0, 0], [1, 1]]))
        assert solver.statistics["solver.solutions.nb"] == 3
        assert solver.statistics["solver.cp.max"] == 2

    def test_solve_sum_ko(self) -> None:
        shr_domains = np.array([[1, 2], [1, 2], [0, 1]])
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets, [Sum([2, 0, 1])])
        solver = BacktrackSolver(problem)
        for _ in solver.solve():
            pass
        assert solver.statistics["solver.solutions.nb"] == 0
        assert solver.statistics["problem.filters.nb"] == 1
        assert solver.statistics["solver.cp.max"] == 0

    def test_solve_alldifferent(self) -> None:
        shr_domains = np.array([[0, 2], [0, 2], [0, 2]])
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets, [AlldifferentPugetN2([0, 1, 2])])
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert len(solutions) == 6
        assert np.all(solutions[0] == np.array([[0, 0], [1, 1], [2, 2]]))
        assert np.all(solutions[1] == np.array([[0, 0], [2, 2], [1, 1]]))
        assert np.all(solutions[2] == np.array([[1, 1], [0, 0], [2, 2]]))
        assert np.all(solutions[3] == np.array([[1, 1], [2, 2], [0, 0]]))
        assert np.all(solutions[4] == np.array([[2, 2], [0, 0], [1, 1]]))
        assert np.all(solutions[5] == np.array([[2, 2], [1, 1], [0, 0]]))
