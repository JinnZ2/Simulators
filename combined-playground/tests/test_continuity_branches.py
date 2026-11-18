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

    def test_five_cases(self):
        self.assertEqual(sorted(self.rows), ["bistable_loose", "counts_word", "fib_exact", "lorenz_lossy",
                                             "spiral_lossy"])

    def test_measured_outcomes_match_ebr_direction(self):
        o = {k: r["outcome"] for k, r in self.rows.items()}
        self.assertEqual(o, {"fib_exact": "SAME", "spiral_lossy": "SAME", "lorenz_lossy": "NOT_SAME",
                             "counts_word": "NOT_SAME", "bistable_loose": "NOT_SAME"})

    def test_spiral_ratio_reproduces_ebr017(self):
        c = next(c for c in K.cases() if c["case"] == "spiral_lossy")
        self.assertAlmostEqual(c["ratio"], 0.0498, places=3)

    def test_branch_cells_five_branches(self):
        b = {k: r["branches"] for k, r in self.rows.items()}
        S, N = "SAME", "NOT_SAME"
        self.assertEqual(b["spiral_lossy"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": S})
        self.assertEqual(b["lorenz_lossy"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": N})
        self.assertEqual(b["counts_word"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": N})
        self.assertEqual(b["bistable_loose"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": S})
        self.assertEqual(set(b["fib_exact"].values()), {S})

    def test_d_holds_four_of_four_and_breaks_on_case_five(self):
        rows = list(self.rows.values())
        first4 = [r for r in rows if r["case"] != "bistable_loose"]
        self.assertTrue(all(r["matches"]["D"] for r in first4))
        self.assertFalse(self.rows["bistable_loose"]["matches"]["D"])
        self.assertEqual(self.rows["bistable_loose"]["t4"], "STABLE_LOSSY")   # class from the reference

    def test_d_with_growth_at_own_snapshot_holds_but_reads_the_outcome(self):
        self.assertEqual(self.rows["bistable_loose"]["d_own"], "NOT_SAME")
        self.assertTrue(all(r["d_own"] == r["outcome"] for r in self.rows.values()))

    def test_fixed_lineage_replays_against_exact(self):
        a, s = (1.2345,), (1.234,)
        t = [K.Transition("round", K.h(a), K.h(s), lambda v: tuple(round(x, 3) for x in v))]
        self.assertEqual(K.c_lineage(a, s, t, {K.h(a): a}), "SAME")               # C-C0
        self.assertEqual(K.c_lineage(a, s, t, {K.h(a): a}, exact={K.h(a): a}), "NOT_SAME")

    def test_t4_class_rule(self):
        self.assertEqual(K.t4_class("SUMMARY", None), "SUMMARY_ONLY")
        self.assertEqual(K.t4_class("FULL_STATE", "EXACT"), "CONTEXT_FREE_EXACT")
        self.assertEqual(K.t4_class("FULL_STATE", "LOSSY", 1.0), "STABLE_LOSSY")
        self.assertEqual(K.t4_class("FULL_STATE", "LOSSY", 1.01), "CHAOTIC_REFRESH")
        self.assertIsNone(K.t4_class("FULL_STATE", "LOSSY", None))
        self.assertEqual(K.c_class(None, 1, 1, ({}, {}, {})), "VOID")

    def test_no_branch_picked(self):
        self.assertNotIn("winner", next(iter(self.rows.values())))


if __name__ == "__main__":
    unittest.main()
