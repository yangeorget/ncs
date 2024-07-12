from ncs.problems.problem import ALG_ALLDIFFERENT, ALG_DUMMY, Problem
from ncs.solvers.backtrack_solver import BacktrackSolver
from ncs.utils import STATS_SOLVER_CP_MAX, STATS_SOLVER_SOLUTIONS_NB


class TestBacktrackSolver:
    def test_solve_and_count(self) -> None:
        problem = Problem(shr_domains=[(0, 99), (0, 99)], dom_indices=[0, 1], dom_offsets=[0, 0])
        problem.set_propagators([([], ALG_DUMMY, [])])
        solver = BacktrackSolver(problem)
        for _ in solver.solve():
            pass
        assert solver.statistics[STATS_SOLVER_SOLUTIONS_NB] == 10000
        assert solver.statistics[STATS_SOLVER_CP_MAX] == 2

    def test_solve(self) -> None:
        problem = Problem(shr_domains=[(0, 1), (0, 1)], dom_indices=[0, 1], dom_offsets=[0, 0])
        problem.set_propagators([([], ALG_DUMMY, [])])
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert len(solutions) == 4
        assert solutions[0] == [0, 0]
        assert solutions[1] == [0, 1]
        assert solutions[2] == [1, 0]
        assert solutions[3] == [1, 1]
        assert solver.statistics[STATS_SOLVER_SOLUTIONS_NB] == 4
        assert solver.statistics[STATS_SOLVER_CP_MAX] == 2

    def test_solve_alldifferent(self) -> None:
        problem = Problem(shr_domains=[(0, 2), (0, 2), (0, 2)], dom_indices=[0, 1, 2], dom_offsets=[0, 0, 0])
        problem.set_propagators([([0, 1, 2], ALG_ALLDIFFERENT, [])])
        solver = BacktrackSolver(problem)
        solutions = [solution for solution in solver.solve()]
        assert len(solutions) == 6
        assert solutions[0] == [0, 1, 2]
        assert solutions[1] == [0, 2, 1]
        assert solutions[2] == [1, 0, 2]
        assert solutions[3] == [1, 2, 0]
        assert solutions[4] == [2, 0, 1]
        assert solutions[5] == [2, 1, 0]
