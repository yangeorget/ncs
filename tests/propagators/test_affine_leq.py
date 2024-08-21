import numpy as np

from ncs.memory import (
    PROP_CONSISTENCY,
    PROP_ENTAILMENT,
    new_data_by_values,
    new_domains_by_values,
)
from ncs.propagators.propagators import ALG_AFFINE_LEQ, compute_domains, get_triggers


class TestAffineLEQ:
    def test_get_triggers(self) -> None:
        data = new_data_by_values([1, -1, 8])
        assert np.all(get_triggers(ALG_AFFINE_LEQ, 2, data) == np.array([[True, False], [False, True]]))

    def test_compute_domains_1(self) -> None:
        domains = new_domains_by_values([(1, 10), (1, 10)])
        data = new_data_by_values([1, -1, -1])
        assert compute_domains(ALG_AFFINE_LEQ, domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[1, 9], [2, 10]]))

    def test_compute_domains_2(self) -> None:
        domains = new_domains_by_values([(1, 10), (1, 10)])
        data = new_data_by_values([1, 1, 8])
        assert compute_domains(ALG_AFFINE_LEQ, domains, data) == PROP_CONSISTENCY
        assert np.all(domains == np.array([[1, 7], [1, 7]]))

    def test_compute_domains_3(self) -> None:
        domains = new_domains_by_values([(2, 3), (1, 2)])
        data = new_data_by_values([1, 1, 5])
        assert compute_domains(ALG_AFFINE_LEQ, domains, data) == PROP_ENTAILMENT
        assert np.all(domains == np.array([[2, 3], [1, 2]]))
