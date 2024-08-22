import numpy as np

from ncs.memory import PROP_CONSISTENCY, new_data_by_values, new_domains_by_values
from ncs.problems.problem import Problem
from ncs.propagators.propagators import ALG_ALLDIFFERENT, compute_domains


class TestAlldifferent:

    def test_compute_domains_1(self) -> None:
        domains = new_domains_by_values([(3, 6), (3, 4), (2, 5), (2, 4), (3, 4), (1, 6)])
        data = new_data_by_values([])
        assert compute_domains(ALG_ALLDIFFERENT, domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[6, 6], [3, 4], [5, 5], [2, 2], [3, 4], [1, 1]]))

    def test_compute_domains_2(self) -> None:
        domains = new_domains_by_values([(0, 0), (2, 2), (1, 2)])
        data = new_data_by_values([])
        assert compute_domains(ALG_ALLDIFFERENT, domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[0, 0], [2, 2], [1, 1]]))

    def test_compute_domains_3(self) -> None:
        domains = new_domains_by_values([(0, 0), (0, 4), (0, 4), (0, 4), (0, 4)])
        data = new_data_by_values([])
        assert compute_domains(ALG_ALLDIFFERENT, domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[0, 0], [1, 4], [1, 4], [1, 4], [1, 4]]))

    def test_filter(self) -> None:
        problem = Problem(
            shr_domains=[(0, 0), (2, 2), (0, 2)],
            dom_indices=[0, 1, 2, 0, 1, 2],
            dom_offsets=[0, 0, 0, 0, 1, 2],
        )
        problem.set_propagators(
            [
                ([0, 1, 2], ALG_ALLDIFFERENT, []),
                ([3, 4, 5], ALG_ALLDIFFERENT, []),
            ]
        )
        assert not problem.filter(np.ones((3, 2), dtype=bool))