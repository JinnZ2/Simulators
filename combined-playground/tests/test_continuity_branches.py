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

    def test_six_cases(self):
        self.assertEqual(sorted(self.rows), ["bistable_loose", "bistable_sliver", "counts_word", "fib_exact",
                                             "lorenz_lossy", "spiral_lossy"])

    def test_measured_outcomes_match_ebr_direction(self):
        o = {k: r["outcome"] for k, r in self.rows.items()}
        self.assertEqual(o, {"fib_exact": "SAME", "spiral_lossy": "SAME", "lorenz_lossy": "NOT_SAME",
                             "counts_word": "NOT_SAME", "bistable_loose": "NOT_SAME",
                             "bistable_sliver": "NOT_SAME"})

    def test_spiral_ratio_reproduces_ebr017(self):
        c = next(c for c in K.cases() if c["case"] == "spiral_lossy")
        self.assertAlmostEqual(c["ratio"], 0.0498, places=3)

    def test_branch_cells_five_branches(self):
        b = {k: r["branches"] for k, r in self.rows.items()}
        S, N = "SAME", "NOT_SAME"
        WB, ND = "SAME_WITH_BOUND", "NOT_DECLARED"
        self.assertEqual(b["spiral_lossy"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": S, "D2": WB, "D2m": ND})
        self.assertEqual(b["lorenz_lossy"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": N, "D2": N, "D2m": ND})
        self.assertEqual(b["counts_word"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": N, "D2": N, "D2m": ND})
        self.assertEqual(b["bistable_loose"], {"C-A": N, "C-B": S, "C-C0": S, "C-C": N, "D": S, "D2": N, "D2m": N})
        self.assertEqual(b["bistable_sliver"]["D2"], N)
        self.assertEqual(b["bistable_sliver"]["D2m"], N)
        self.assertEqual(set(b["fib_exact"].values()) - {"NOT_DECLARED"}, {S})

    def test_d_holds_four_of_four_and_breaks_on_case_five(self):
        rows = list(self.rows.values())
        first4 = [r for r in rows if not r["case"].startswith("bistable")]
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

    def _case(self, name):
        return next(c for c in K.cases() if c["case"] == name)

    def test_n_required(self):
        self.assertEqual(K.n_required(0.04, 0.01), 113)
        self.assertEqual(K.n_required(0.01, 0.05), 299)        # rule-of-three neighbourhood (3/N ~ 0.01)

    def test_purpose_inputs_missing_untested_bad_refused(self):
        c = self._case("spiral_lossy")
        self.assertEqual(K.d2_bound(c).state, "UNTESTED")
        self.assertEqual(K.d2_bound(c, f_min=0.04).state, "UNTESTED")
        for bad in ((0.0, 0.01), (0.04, 1.0), (True, 0.01)):
            with self.assertRaises(ValueError):
                K.d2_bound(c, *bad)

    def test_same_with_bound_records_its_bound(self):
        v = K.d2_bound(self._case("spiral_lossy"), 0.04, 0.01)
        self.assertEqual((v.state, v.f_min, v.alpha, v.N, v.hits), ("SAME_WITH_BOUND", 0.04, 0.01, 113, 0))
        self.assertIn("confidence 0.99", v.reason)

    def test_hit_is_not_same(self):
        v = K.d2_bound(self._case("bistable_sliver"), 0.04, 0.01)
        self.assertEqual((v.state, v.N, v.hits), ("NOT_SAME", 113, 1))

    def test_d2_holds_six_of_six(self):
        self.assertTrue(all(r["matches"]["D2"] for r in self.rows.values()))

    def test_sliver_snapshot_is_across_the_separatrix_and_inside_the_ball(self):
        c = self._case("bistable_sliver")
        self.assertLessEqual(K._dist(c["state"], c["anchor"]), K.SLIVER_R)
        self.assertNotEqual(K._basin(c["state"]), K._basin(c["anchor"]))
        self.assertEqual(c["t4"], "STABLE_LOSSY")                     # global class misses it

    def test_exact_margin_path(self):
        c = self._case("bistable_sliver")
        state, m = K.d2_margin(c)
        self.assertEqual(state, "NOT_SAME")
        self.assertAlmostEqual(m, 0.0411, places=3)
        self.assertEqual(K.d2_margin(dict(c, radius=0.03)), ("SAME", m))          # ball inside basin
        self.assertEqual(K.d2_margin(self._case("spiral_lossy"))[0], "NOT_DECLARED")

    def test_margin_is_the_basin_boundary(self):
        import math
        c = self._case("bistable_sliver")
        a = c["anchor"]
        best = min((p for br in K._stable_manifold() for p in br), key=lambda p: math.hypot(p[0] - a[0], p[1] - a[1]))
        d = math.hypot(best[0] - a[0], best[1] - a[1])
        u = ((best[0] - a[0]) / d, (best[1] - a[1]) / d)
        side = lambda t: K._basin((a[0] + u[0] * d * t, a[1] + u[1] * d * t))
        self.assertNotEqual(side(0.95), side(1.05))

    def test_case6_at_bound_miss_rate_reported(self):
        N = K.n_required(K.F_MIN, K.ALPHA)
        m = K.miss_table(Ns=(N,), trials=400, pool=2000, seed=11)
        self.assertEqual(m["rows"][0]["N"], 113)
        self.assertAlmostEqual(m["rows"][0]["miss_rate"], 0.0125)               # 5 of 400, seed 11
        self.assertGreater(m["rows"][0]["miss_rate"], K.ALPHA)                  # the order's test: NOT met
        lo, hi = K._wilson(5, 400)
        self.assertLess(lo, K.ALPHA)
        self.assertGreater(hi, K.ALPHA)                                         # 400 trials cannot resolve it

    def test_miss_rate_falls_with_n_and_tracks_prediction(self):
        m = K.miss_table(Ns=(1, 16, 64, 256), trials=200, pool=600)
        rates = [r["miss_rate"] for r in m["rows"]]
        self.assertEqual(rates, sorted(rates, reverse=True))
        self.assertGreater(m["f_hat"], 0.0)
        self.assertLess(m["f_hat"], 0.1)                              # a thin sliver
        for r in m["rows"]:
            self.assertLess(abs(r["miss_rate"] - r["predicted"]), 0.12)

    def test_resolution_exact_sliver_above_threshold(self):
        self.assertAlmostEqual(K.f_threshold(113, 0.01), 0.039934, places=6)
        f = K.sliver_fraction_exact(M=40, bisect=20)                            # coarse recompute
        self.assertLess(abs(f - K.SLIVER_F_EXACT), 5e-4)
        self.assertGreater(K.SLIVER_F_EXACT, K.f_threshold(113, K.ALPHA))
        self.assertLess((1 - K.SLIVER_F_EXACT) ** 113, K.ALPHA)                  # exact miss 0.0065

    def test_resolution_direct_run_resolves_alpha(self):
        k, n = K.DIRECT_RUN["miss"], K.DIRECT_RUN["trials"]
        lo, hi = K._wilson(k, n)
        self.assertLess(hi, K.ALPHA)                                            # resolved: whole interval below alpha
        self.assertLess(lo, (1 - K.SLIVER_F_EXACT) ** 113)
        self.assertGreater(hi, (1 - K.SLIVER_F_EXACT) ** 113)                   # agrees with the exact miss
        self.assertEqual(K.direct_miss(5, 0), 5)                                # N 0 samples: every trial misses
        self.assertIn("VOID-9 -> DECIDED", K.render())

    def test_no_branch_picked(self):
        self.assertNotIn("winner", next(iter(self.rows.values())))


if __name__ == "__main__":
    unittest.main()
