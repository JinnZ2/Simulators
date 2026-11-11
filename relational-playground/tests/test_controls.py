import unittest
from helpers import *
from playground.controls import ControlMatrix
from playground.experiments import comparison, runner, perturbation
from playground import known_answer_gate as gate

gate.certify_all()
OB = lambda st: dict(state=st, basis="fixture")
C = lambda **kw: config("allee", dict(r=1.0, a=1.0, K=10.0, h=0.1), dict(x=2.0), live=dict(mass=["x"]), t_end=6.0, **kw)


class T(unittest.TestCase):
    def test_fields_must_be_written(self):
        self.assertRaises(ValueError, ControlMatrix, held_constant="x")

    def test_observer_regimes_are_three_separate_fields(self):
        c = controls(observer_perturbation=OB("PRESENT"))
        self.assertEqual(c.observer_undeclared(), ["observer_reactivity", "observer_strategy"])
        self.assertRaises(ValueError, controls, observer_strategy="yes")

    def test_cross_system_refused_until_declared(self):
        self.assertRaises(comparison.RegimeUndeclared, comparison.cross_system, dict(a=[C()], b=[C()]), "x")
        full = controls(observer_perturbation=OB("ABSENT"), observer_reactivity=OB("UNKNOWN"), observer_strategy=OB("ABSENT"))
        r = comparison.cross_system(dict(a=[C(controls=full)], b=[C(controls=full)]), "x")
        self.assertFalse(r["regimes_differ"])

    def test_no_ranking(self):
        self.assertRaises(RuntimeError, comparison.rank, [])

    def test_perturbation_is_booked_at_the_boundary(self):
        r = perturbation.response(C(), "x", -1.0, 3.0)
        self.assertEqual(r["kicked"]["status"], "COMPLETE")
        self.assertIn("perturbation 1", r["kicked"]["boundary_audit"][0])
        self.assertNotEqual(r["recovered_at"], "NOT RECOVERED IN RUN")


if __name__ == "__main__":
    unittest.main()
