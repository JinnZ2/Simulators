"""G3: rows 35-36 percolation (two families, Q10) and branching (Galton-Watson, Q11).

Known answers are VERIFY-tagged (recalled, no source read). Written before cplay/families.py.
"""
import math, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import families as F  # noqa: E402


class Percolation(unittest.TestCase):
    def test_site_threshold_near_known_answer(self):
        r = F.site_threshold(L=32, runs=60, seed=11)
        self.assertLess(abs(r["mean"] - F.SITE_PC_SQUARE), 0.03, r)
        self.assertIn("VERIFY", r["known_answer_status"])

    def test_bond_threshold_near_known_answer(self):
        r = F.bond_threshold(L=32, runs=60, seed=11)
        self.assertLess(abs(r["mean"] - F.BOND_PC_SQUARE), 0.03, r)

    def test_two_families_are_different_objects(self):
        s = F.site_threshold(L=24, runs=40, seed=3)
        b = F.bond_threshold(L=24, runs=40, seed=3)
        self.assertEqual((s["family"], b["family"]), ("site", "bond"))
        self.assertGreater(s["mean"] - b["mean"], 0.05)       # site ~0.59 vs bond ~0.5

    def test_seeded_reproducible(self):
        self.assertEqual(F.site_threshold(16, 10, 5)["mean"], F.site_threshold(16, 10, 5)["mean"])

    def test_bound_is_applicability_outside_domain(self):
        r = F.site_threshold(L=F.SITE_L_MAX + 1, runs=1, seed=0)
        self.assertEqual((r.field, r.status), ("APPLICABILITY", "OUTSIDE_DOMAIN"))
        r = F.bond_threshold(L=F.BOND_L_MAX + 1, runs=1, seed=0)
        self.assertEqual((r.field, r.status), ("APPLICABILITY", "OUTSIDE_DOMAIN"))

    def test_bad_input_refused(self):
        for bad in (1, 2.5, True):
            with self.assertRaises(F.FamilyError):
                F.site_threshold(L=bad, runs=1, seed=0)
        with self.assertRaises(F.FamilyError):
            F.bond_threshold(L=8, runs=0, seed=0)


class Branching(unittest.TestCase):
    def test_poisson_subcritical_and_critical_extinct(self):
        for lam in (0.0, 0.5, 1.0):
            self.assertEqual(F.extinction_poisson(lam), 1.0)

    def test_poisson_supercritical_fixed_point(self):
        for lam in (1.5, 2.0, 3.0):
            q = F.extinction_poisson(lam)
            self.assertLess(q, 1.0)
            self.assertLess(abs(q - math.exp(lam * (q - 1.0))), 1e-12)
        self.assertAlmostEqual(F.extinction_poisson(2.0), 0.2031878699, places=8)   # VERIFY

    def test_smallest_root_not_q_equal_one(self):
        q = F.extinction_poisson(2.0)
        self.assertLess(q, 0.5)                      # q = 1 is also a root; the smallest is taken

    def test_pmf_cases(self):
        self.assertEqual(F.extinction_pmf([0.5, 0.5]), 1.0)              # mean 0.5
        self.assertEqual(F.extinction_pmf([0.0, 1.0]), 0.0)              # exactly one child
        self.assertAlmostEqual(F.extinction_pmf([0.25, 0.25, 0.5]), 0.5)  # f(s)=s: .25+.25s+.5s^2
        self.assertEqual(F.extinction_pmf([0.25, 0.5, 0.25]), 1.0)       # mean exactly 1

    def test_pmf_bound_and_validation(self):
        big = [0.0] * (F.PMF_SUPPORT_MAX + 2)
        big[-1] = 1.0
        r = F.extinction_pmf(big)
        self.assertEqual((r.field, r.status), ("APPLICABILITY", "OUTSIDE_DOMAIN"))
        for bad in ([], [0.5, 0.6], [-0.1, 1.1]):
            with self.assertRaises(F.FamilyError):
                F.extinction_pmf(bad)
        with self.assertRaises(F.FamilyError):
            F.extinction_poisson(-1)


if __name__ == "__main__":
    unittest.main()
