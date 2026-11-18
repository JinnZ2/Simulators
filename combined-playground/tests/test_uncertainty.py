"""M9 distribution-to-mean loss flag (COMBINED_SPEC section 8 rows 37, 39).

Written before cplay/uncertainty.py.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import uncertainty as U  # noqa: E402


class Flag(unittest.TestCase):
    def test_interval_containing_both_flags(self):
        # X uniform on {1, 3}: mean^2 = 4, E[X^2] = 5
        f = U.mean_loss_flag(lo=3.5, hi=6.0, samples=[1.0, 3.0])
        self.assertTrue(f.flag)
        self.assertEqual((f.mean_sq, f.e_x_sq), (4.0, 5.0))

    def test_interval_containing_one_does_not_flag(self):
        f = U.mean_loss_flag(lo=4.5, hi=6.0, samples=[1.0, 3.0])
        self.assertFalse(f.flag)

    def test_point_distribution_cannot_lose_information(self):
        f = U.mean_loss_flag(lo=0.0, hi=100.0, samples=[2.0, 2.0])
        self.assertEqual(f.mean_sq, f.e_x_sq)
        self.assertTrue(f.flag)     # contains both because they coincide; reported, not hidden
        self.assertTrue(f.coincide)

    def test_refusals(self):
        with self.assertRaises(U.UncertaintyError):
            U.mean_loss_flag(lo=2.0, hi=1.0, samples=[1.0])
        with self.assertRaises(U.UncertaintyError):
            U.mean_loss_flag(lo=0.0, hi=1.0, samples=[])

    def test_interval_propagation_rule_void(self):
        self.assertEqual(U.PROPAGATION.state, "VOID")


if __name__ == "__main__":
    unittest.main()
