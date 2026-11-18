"""G5 item 9: continuity identity branches C-A exact / C-B tolerance / C-C lineage, side by side.

Written before cplay/continuity_branches.py. No branch is picked.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import continuity_branches as K  # noqa: E402


class Criteria(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(K.c_exact((1.0, 2.0), (1.0, 2.0)), "SAME")
        self.assertEqual(K.c_exact((1.0, 2.0), (1.0, 2.0000001)), "NOT_SAME")

    def test_tolerance_reuses_m8(self):
        self.assertEqual(K.c_tolerance({"x": 1.0}, {"x": 1.0004}, {"x": 1e-3}), "SAME")
        self.assertEqual(K.c_tolerance({"x": 1.0}, {"x": 1.01}, {"x": 1e-3}), "NOT_SAME")

    def test_lineage_needs_unbroken_verified_chain(self):
        a, s = (1.2345,), (1.234,)
        good = [K.Transition("round", K.h(a), K.h(s), lambda v: tuple(round(x, 3) for x in v))]
        self.assertEqual(K.c_lineage(a, s, good, {K.h(a): a}), "SAME")
        bad_replay = [K.Transition("round", K.h(a), K.h(s), lambda v: v)]
        self.assertEqual(K.c_lineage(a, s, bad_replay, {K.h(a): a}), "NOT_SAME")
        self.assertEqual(K.c_lineage(a, s, [], {}), "NOT_SAME")
        mid = (9.9,)
        broken = [K.Transition("t1", K.h(a), K.h(mid), lambda v: mid),
                  K.Transition("t2", K.h((0.0,)), K.h(s), lambda v: s)]
        self.assertEqual(K.c_lineage(a, s, broken, {K.h(a): a, K.h((0.0,)): (0.0,)}), "NOT_SAME")


class Table(unittest.TestCase):
    def setUp(self):
        self.rows = {r["case"]: r for r in K.table()}

    def test_four_known_cases(self):
        self.assertEqual(sorted(self.rows), ["counts_word", "fib_exact", "lorenz_lossy", "spiral_lossy"])

    def test_measured_outcomes_match_ebr_direction(self):
        o = {k: r["outcome"] for k, r in self.rows.items()}
        self.assertEqual(o, {"fib_exact": "SAME", "spiral_lossy": "SAME",
                             "lorenz_lossy": "NOT_SAME", "counts_word": "NOT_SAME"})

    def test_spiral_ratio_reproduces_ebr017(self):
        c = next(c for c in K.cases() if c["case"] == "spiral_lossy")
        self.assertAlmostEqual(c["ratio"], 0.0498, places=3)

    def test_branch_cells_and_split(self):
        b = {k: r["branches"] for k, r in self.rows.items()}
        self.assertEqual(b["spiral_lossy"], {"C-A": "NOT_SAME", "C-B": "SAME", "C-C": "SAME"})
        self.assertEqual(b["lorenz_lossy"], {"C-A": "NOT_SAME", "C-B": "SAME", "C-C": "SAME"})
        self.assertEqual(b["counts_word"], {"C-A": "NOT_SAME", "C-B": "SAME", "C-C": "SAME"})
        self.assertEqual(set(b["fib_exact"].values()), {"SAME"})
        self.assertEqual([k for k, r in sorted(self.rows.items()) if r["split"]],
                         ["counts_word", "lorenz_lossy", "spiral_lossy"])

    def test_no_branch_matches_all_four(self):
        for k in ("C-A", "C-B", "C-C"):
            self.assertLess(sum(r["matches"][k] for r in self.rows.values()), 4, k)
        self.assertNotIn("winner", next(iter(self.rows.values())))


if __name__ == "__main__":
    unittest.main()
