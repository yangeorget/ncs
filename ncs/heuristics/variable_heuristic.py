from typing import List

from numpy.typing import NDArray

from ncs.heuristics.heuristic import Heuristic
from ncs.heuristics.value_heuristic import ValueHeuristic
from ncs.problem import Problem


class VariableHeuristic(Heuristic):
    """
    Chooses a variable and one or several values for this variable.
    """

    def __init__(self, value_heuristic: ValueHeuristic):
        self.value_heuristic = value_heuristic

    def choose(self, choice_points: List[NDArray], problem: Problem) -> bool:
        """
        Chooses a variable and a value for this variable.
        :param choice_points: the choice point list
        :param problem: the problem
        :return: True iff it is possible to make a choice
        """
        idx = self.choose_variable(problem)
        if idx == -1:
            return False
        domains = self.value_heuristic.choose(problem, idx)
        choice_points.append(domains)
        return True

    def choose_variable(self, problem: Problem) -> int:  # type: ignore
        """
        Chooses a variable.
        :param problem: a problem
        :return: the index of the variable
        """
        pass