import unittest
from helpers import *
from playground.continuity import ContinuityMatrix, READINGS


class T(unittest.TestCase):
    def test_undeclared_is_not_defaulted(self):
        self.assertEqual(set(ContinuityMatrix().read([0, 1], [{}, {}]).values()), {"UNDECLARED"})

    def test_reorganization_is_not_an_ending(self):
        c = ContinuityMatrix(lambda s: s["mass"] > 0, lambda s: s["shape"], basis="fixture")
        r = c.read([0, 1, 2], [dict(mass=1, shape="net"), dict(mass=1, shape="blob"), dict(mass=1, shape="blob")])
        self.assertEqual(r["system_continuity"], "CONTINUOUS")
        self.assertEqual(r["recovery_and_reorganization"], "REORGANIZED")
        self.assertEqual(len(r["transition_dynamics"]), 1)

    def test_lapse_and_recovery_are_kept_apart(self):
        c = ContinuityMatrix(lambda s: s["mass"] > 0, lambda s: "one", basis="fixture")
        r = c.read([0, 1, 2], [dict(mass=1), dict(mass=0), dict(mass=1)])
        self.assertEqual(r["system_continuity"], "INTERRUPTED_THEN_RECOVERED")
        self.assertEqual(r["configuration_continuity"], "UNCHANGED")
        self.assertEqual(sorted(r), sorted(READINGS))


if __name__ == "__main__":
    unittest.main()
