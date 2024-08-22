from ncs.problems.bibd_problem import BIBDProblem
from ncs.solvers.backtrack_solver import BacktrackSolver
from ncs.statistics import STATS_SOLVER_SOLUTION_NB, statistics_print


class TestBIBD:
    def test_6_10_5_3_2(self) -> None:
        problem = BIBDProblem(6, 10, 5, 3, 2)
        solver = BacktrackSolver(problem)
        solver.find_all()
        assert problem.statistics[STATS_SOLVER_SOLUTION_NB] == 1

    def test_8_14_7_4_3(self) -> None:
        problem = BIBDProblem(8, 14, 7, 4, 3)
        solver = BacktrackSolver(problem)
        solver.find_all()
        assert problem.statistics[STATS_SOLVER_SOLUTION_NB] == 92


if __name__ == "__main__":
    problem = BIBDProblem(8, 14, 7, 4, 3)
    solver = BacktrackSolver(problem)
    solver.find_all()
    statistics_print(problem.statistics)