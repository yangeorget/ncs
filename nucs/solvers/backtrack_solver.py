from typing import Iterator, List, Optional

from nucs.heuristics.heuristic import Heuristic
from nucs.heuristics.variable_heuristic import (
    VariableHeuristic,
    first_not_instantiated_var_heuristic,
    min_value_dom_heuristic,
)
from nucs.memory import PROBLEM_INCONSISTENT, PROBLEM_SOLVED, new_shr_domain_changes
from nucs.problems.problem import Problem
from nucs.solvers.solver import Solver
from nucs.statistics import (
    STATS_OPTIMIZER_SOLUTION_NB,
    STATS_SOLVER_BACKTRACK_NB,
    STATS_SOLVER_CHOICE_DEPTH,
    STATS_SOLVER_CHOICE_NB,
    STATS_SOLVER_SOLUTION_NB,
)


class BacktrackSolver(Solver):
    """
    A solver relying on a backtracking mechanism.
    """

    def __init__(
        self,
        problem: Problem,
        heuristic: Heuristic = VariableHeuristic(first_not_instantiated_var_heuristic, min_value_dom_heuristic),
    ):
        super().__init__(problem)
        self.choice_points = []  # type: ignore
        self.shr_domain_changes = new_shr_domain_changes(len(self.problem.shr_domains_lst))
        self.heuristic = heuristic

    def solve(self) -> Iterator[List[int]]:
        while (solution := self.solve_one()) is not None:
            yield solution
            if not self.backtrack():
                break

    def solve_one(self) -> Optional[List[int]]:
        """
        Find at most one solution.
        :return: the solution if it exists or None
        """
        while True:
            status = self.filter()
            if status == PROBLEM_INCONSISTENT:
                return None
            elif status == PROBLEM_SOLVED:
                self.problem.statistics[STATS_SOLVER_SOLUTION_NB] += 1
                return self.problem.get_values()  # problem is solved
            else:
                self.heuristic.choose(
                    self.choice_points,
                    self.problem.shr_domains_arr,
                    self.shr_domain_changes,
                    self.problem.dom_indices_arr,
                )
                self.problem.statistics[STATS_SOLVER_CHOICE_NB] += 1
                self.problem.statistics[STATS_SOLVER_CHOICE_DEPTH] = max(
                    self.problem.statistics[STATS_SOLVER_CHOICE_DEPTH], len(self.choice_points)
                )

    def minimize(self, variable_idx: int) -> Optional[List[int]]:
        solution = None
        while (new_solution := self.solve_one()) is not None:
            solution = new_solution
            self.problem.statistics[STATS_OPTIMIZER_SOLUTION_NB] += 1
            self.reset()
            self.problem.set_max_value(variable_idx, solution[variable_idx] - 1)
        return solution

    def maximize(self, variable_idx: int) -> Optional[List[int]]:
        solution = None
        while (new_solution := self.solve_one()) is not None:
            solution = new_solution
            self.problem.statistics[STATS_OPTIMIZER_SOLUTION_NB] += 1
            self.reset()
            self.problem.set_min_value(variable_idx, solution[variable_idx] + 1)
        return solution

    def backtrack(self) -> bool:
        """
        Backtracks and updates the problem's domains
        :return: true iff it is possible to backtrack
        """
        if len(self.choice_points) == 0:
            return False
        self.problem.statistics[STATS_SOLVER_BACKTRACK_NB] += 1
        self.shr_domain_changes.fill(True)
        self.problem.shr_domains_arr = self.choice_points.pop()
        self.problem.reset_not_entailed_propagators()
        return True

    def filter(self) -> int:
        """
        Achieves bound consistency and backtracks if necessary.
        """
        while True:
            status = self.problem.filter(self.shr_domain_changes)
            if status == PROBLEM_INCONSISTENT:
                if self.backtrack():
                    continue
            return status

    def reset(self) -> None:
        """
        Resets the solver by resetting the problem and the choice points.
        """
        self.choice_points.clear()
        self.shr_domain_changes.fill(True)
        self.problem.reset_shr_domains()
        self.problem.reset_not_entailed_propagators()
