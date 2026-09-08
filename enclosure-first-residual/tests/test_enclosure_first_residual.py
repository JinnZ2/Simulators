"""
Tests for enclosure-first-residual. stdlib unittest only. CC0.

    python3 -m unittest discover -s enclosure-first-residual/tests -p 'test_*.py'

method-layer is a declared external dependency; the tests that need it skip
with a printed reason when it is not on the path. Skipping is a state, and
the CI log shows it.
"""

import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import enclosure_first_residual as m  # noqa: E402


class TestEnclosureTerms(unittest.TestCase):
    def test_effective_exits_is_reachable_and_affordable(self):
        enc = {"option_set_size": 4, "exit_cost": [0.2, 1.0, 1.5, 0.3],
               "reachability": [1, 1, 1, 0], "reversibility": [1, 0, 0, 1]}
        self.assertEqual(m.effective_exits(enc), 2)
        f = m.enclosure_features(enc)
        self.assertEqual(f["option_set_size"], 4)
        self.assertEqual(f["reversible_count"], 2)

    def test_length_mismatch_is_schema_error(self):
        enc = {"option_set_size": 3, "exit_cost": [0.2], "reachability": [1, 1, 1], "reversibility": [1, 0, 0]}
        with self.assertRaises(m.SchemaError):
            m.enclosure_features(enc)


class TestSchemaGate(unittest.TestCase):
    def _panel(self, term, ops):
        enc = {"option_set_size": 1, "exit_cost": [0.1], "reachability": [1], "reversibility": [1]}
        return m.load_panel({"population": "x", "operationalizations": ops,
                             "windows": [{"person_id": "a", "t0": 1, "t1": 2, "change_origin": "baseline",
                                          "enclosure": enc, "behavior": {term: 1.0}}]})

    def test_unoperationalized_graded_term_is_blocked(self):
        self.assertIn("perseveration_rate", m.schema_gate(self._panel("perseveration_rate", {})))

    def test_operationalized_graded_term_passes(self):
        self.assertEqual(m.schema_gate(self._panel("perseveration_rate", {"perseveration_rate": "x"})), {})

    def test_closed_label_is_blocked_even_with_operationalization(self):
        self.assertIn("rigidity", m.schema_gate(self._panel("rigidity", {"rigidity": "scored 1-5"})))

    def test_blank_operationalization_is_blocked(self):
        self.assertIn("perseveration_rate", m.schema_gate(self._panel("perseveration_rate", {"perseveration_rate": "  "})))


class TestLeastSquares(unittest.TestCase):
    def test_exact_line(self):
        r, beta, dropped = m.ols_residual_fraction([[1.0], [2.0], [3.0]], [2.0, 4.0, 6.0])
        self.assertAlmostEqual(r, 0.0, places=12)
        self.assertAlmostEqual(beta[1], 2.0, places=9)
        self.assertEqual(dropped, [])

    def test_constant_regressor_dropped(self):
        r, beta, dropped = m.ols_residual_fraction([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]], [1.0, 2.0, 3.1])
        self.assertEqual(dropped, [1])

    def test_no_variance_returns_none(self):
        r, _, _ = m.ols_residual_fraction([[1.0], [2.0]], [3.0, 3.0])
        self.assertIsNone(r)


class TestReturns(unittest.TestCase):
    def test_scored_kinds_need_fraction(self):
        with self.assertRaises(Exception):
            m.make_return(m.KIND_ENCLOSURE_DOMINANT)  # no fraction
        r = m.make_return(m.KIND_ENCLOSURE_DOMINANT, fraction=0.5, ci=(0.4, 0.6))
        self.assertEqual(r["return_class"], m.ReturnClass.SCORED)

    def test_blocked_carries_named_blocker(self):
        r = m.make_return(m.KIND_BLOCKED, blocker=m.BLOCK_NO_WITHIN, reason="x")
        self.assertEqual(m.label(r), "BLOCKED(no_within_person_windows)")

    def test_out_of_envelope_status(self):
        r = m.make_return(m.KIND_OUT_OF_ENVELOPE, reason="chosen")
        self.assertEqual(r["envelope_status"], "out_of_envelope")

    def test_confound_rides_variable_unident(self):
        r = m.make_return(m.KIND_CONFOUND, reason="x")
        self.assertEqual(r["return_class"], m.ReturnClass.VARIABLE_UNIDENT)

    @unittest.skipIf(m.G is None, "method-layer absent: G enum mirror not cross-checked")
    def test_mirror_matches_G(self):
        for name in ("SCORED", "UNKNOWN_MEASURABLE", "BLOCKED", "OUT_OF_ENVELOPE", "VARIABLE_UNIDENT"):
            self.assertEqual(getattr(m.G.ReturnClass, name).value, getattr(m.ReturnClass, name))


class TestFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.buf = io.StringIO()
        cls.runs = m.demo(out=cls.buf)
        cls.kinds = {n: next(iter(r["results"].values()))["return"]["kind"] for n, r in cls.runs.items()}

    def test_cells(self):
        self.assertEqual(self.kinds["F1_enclosure_only"], m.KIND_ENCLOSURE_DOMINANT)
        self.assertEqual(self.kinds["F2_trait_only"], m.KIND_UNKNOWN)
        self.assertEqual(self.kinds["F3_trait_plus_enclosure"], m.KIND_TRAIT_RESIDUAL)
        self.assertEqual(self.kinds["F4_selection_into_windows"], m.KIND_CONFOUND)
        self.assertEqual(self.kinds["F5_chosen_change"], m.KIND_OUT_OF_ENVELOPE)
        self.assertEqual(self.kinds["F6_unoperationalized"], m.KIND_BLOCKED)
        self.assertEqual(self.kinds["F7_single_windows"], m.KIND_BLOCKED)

    def test_null_printed_before_between_fit(self):
        for block in self.buf.getvalue().split("== ")[1:]:
            if "   between arm  n=" in block:
                self.assertLess(block.index("NULL FIRST"), block.index("   between arm  n="))

    def test_choices_printed(self):
        self.assertIn('"DOMINANT_RATIO": 0.5', self.buf.getvalue())

    def test_f7_flags_single_window_persons(self):
        rec = self.runs["F7_single_windows"]["results"]["latency_to_approach_novel"]
        self.assertEqual(len(rec["envelope"]["single_window_persons"]), 40)
        self.assertEqual(rec["return"]["blocker"], m.BLOCK_NO_WITHIN)
        self.assertIn("between", rec)  # between arm still reported

    def test_f5_excludes_chosen_pairs(self):
        rec = self.runs["F5_chosen_change"]["results"]["latency_to_approach_novel"]
        self.assertEqual(rec["envelope"]["chosen"], 40)
        self.assertEqual(rec["envelope"]["exogenous"], 0)

    def test_literal_table_puts_f1_in_confound_cell(self):
        # EFR_003: the order's table as written
        panel = m.load_panel(m.make_fixture("F1", **dict(m.FIXTURES[0][1])))
        lit = m.run_panel(panel, seed=1, table_literal=True, out=io.StringIO())
        rec = lit["results"]["latency_to_approach_novel"]
        self.assertEqual(rec["compare"]["table_cell"], ">")
        self.assertEqual(rec["return"]["kind"], m.KIND_CONFOUND)

    def test_nominal_count_overstates(self):
        # the order's NOTE: option_set_size alone leaves more residual
        for name in ("F1_enclosure_only", "F3_trait_plus_enclosure"):
            bt = self.runs[name]["results"]["latency_to_approach_novel"]["between"]
            self.assertGreater(bt["residual_nominal_only"], bt["residual"])


class TestBranchSet(unittest.TestCase):
    def test_four_branches_and_origin(self):
        d = m.branch_set_dict()
        self.assertEqual([b["id"] for b in d["branches"]],
                         ["enclosure_constraint", "trait_plain", "selection_into_enclosure",
                          "measurement_artifact_of_label_set"])
        self.assertTrue(all(b["origin_pattern"] == m.ORIGIN_PATTERN for b in d["branches"]))
        self.assertTrue(all(b["predicts_elsewhere"][0]["domain"] != b["origin_pattern"] for b in d["branches"]))

    def test_enclosure_dominant_eliminates_trait_plain(self):
        run = {"population": "p", "results": {"t": {"return": m.make_return(
            m.KIND_ENCLOSURE_DOMINANT, fraction=0.6, ci=(0.5, 0.7))}}}
        d = m.branch_set_dict(run)
        tp = [b for b in d["branches"] if b["id"] == "trait_plain"][0]
        self.assertEqual(tp["status"], "eliminated")
        self.assertIn("K run", tp["eliminated_by"])

    @unittest.skipIf(m.F is None, "method-layer absent: branch set not round-tripped through F")
    def test_round_trips_through_F(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bs.json")
            m.emit_branch_set(path)
            bs = m.F.BranchSet.load(path)
            self.assertEqual(len(bs.branches), 4)
            self.assertEqual(len(bs.test_queue()), 4)


class TestCli(unittest.TestCase):
    def test_selftest_passes(self):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc = m.selftest()
        finally:
            sys.stdout = old
        self.assertEqual(rc, 0, buf.getvalue())

    def test_run_on_panel_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "p.json")
            with open(path, "w") as fh:
                json.dump(m.make_fixture("x", **dict(m.FIXTURES[0][1])), fh)
            buf = io.StringIO()
            old = sys.stdout
            sys.stdout = buf
            try:
                rc = m.main(["run", path, "--seed", "1"])
            finally:
                sys.stdout = old
            self.assertEqual(rc, 0)
            self.assertIn("NULL FIRST", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
