import numpy as np

from ncs.problems.problem import Problem, compute_shared_domains_changes
from ncs.propagators.propagator import ALLDIFFERENT_LOPEZ_ORTIZ, SUM, Propagator


class TestProblem:
    def test_domains(self) -> None:
        shr_domains = [(0, 2), (4, 6)]
        dom_indices = [0, 0, 1]
        dom_offsets = [0, 1, 2]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        assert np.all(problem.get_domains() == np.array([[0, 2], [1, 3], [6, 8]]))

    def test_is_not_instantiated(self) -> None:
        shr_domains = [(0, 2), (0, 0)]
        dom_indices = [0, 0, 1]
        dom_offsets = [0, 1, 2]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        assert problem.is_not_instantiated(0)
        assert problem.is_not_instantiated(1)
        assert not problem.is_not_instantiated(2)

    def test_is_not_solved_ok(self) -> None:
        shr_domains = [(0, 2), (0, 2), (4, 6)]
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        assert problem.is_not_solved()

    def test_is_not_solved_ko(self) -> None:
        shr_domains = [(2, 2), (2, 2), (6, 6)]
        dom_indices = [0, 1, 2]
        dom_offsets = [0, 0, 0]
        problem = Problem(shr_domains, dom_indices, dom_offsets)
        assert not problem.is_not_solved()

    def test_filter_1(self) -> None:
        problem = Problem(shr_domains=[(0, 2), (0, 2), (4, 6)], dom_indices=[0, 1, 2], dom_offsets=[0, 0, 0])
        problem.add_propagator(Propagator(np.array([2, 0, 1], dtype=np.int32), SUM))
        assert problem.filter()
        assert not problem.is_not_solved()
        assert np.all(problem.shr_domains == np.array([[2, 2], [2, 2], [4, 4]]))

    def test_filter_2(self) -> None:
        problem = Problem(
            shr_domains=[(0, 0), (2, 2), (0, 2)],
            dom_indices=[0, 1, 2, 0, 1, 2],
            dom_offsets=[0, 0, 0, 0, 1, 2],
        )
        problem.add_propagator(Propagator(np.array([0, 1, 2], dtype=np.int32), ALLDIFFERENT_LOPEZ_ORTIZ))
        problem.add_propagator(Propagator(np.array([3, 4, 5], dtype=np.int32), ALLDIFFERENT_LOPEZ_ORTIZ))
        assert not problem.filter()

    def test_compute_shr_domain_changes(self) -> None:
        problem = Problem(
            shr_domains=[(0, 2), (0, 2), (0, 2)],
            dom_indices=[0, 1, 2],
            dom_offsets=[0, 0, 0],
        )
        shr_domain_changes = compute_shared_domains_changes(
            prop_indices=np.array([0, 1]),
            prop_offsets=np.array([0, 0]),
            prop_domains=np.array([(0, 2), (0, 2)]),
            new_prop_domains=np.array([(0, 1), (1, 2)]),
            shr_domains=problem.shr_domains,
        )
        assert np.all(np.equal(shr_domain_changes, np.array([(False, True), (True, False), (False, False)])))
