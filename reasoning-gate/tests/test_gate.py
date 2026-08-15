"""
Tests for gate.py.

Two halves, deliberately separated:

  GuardBehaviour  — the eight guards do what guards.json says they do.
  ShippedDefects  — four defects found on landing, locked in as tests so
                    a fix flips a test rather than passing silently.

gate.py is checked in exactly as delivered and has not been repaired. The
defects are documented in ../README.md under "Audit of the gate itself".

Run:  python3 -m unittest discover tests
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gate import Control, Gate, GateError, Resolution  # noqa: E402

GUARDS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "guards.json")


def _load_registry():
    with open(GUARDS) as fh:
        return json.load(fh)


def _write_registry(reg):
    path = os.path.join(tempfile.mkdtemp(), "g.json")
    with open(path, "w") as fh:
        json.dump(reg, fh)
    return path


def opened(strict=True, log_dir=None, **overrides):
    """A gate past pre() with everything declared and passing."""
    kw = dict(
        question="q", statistic="s", discriminates="d", expected="e",
        resolution=[Resolution("r", instrument=1.0, feature=10.0)],
        controls=[Control("c", predicted="p")],
    )
    kw.update(overrides)
    g = Gate("T", guards=GUARDS, strict=strict, log_dir=log_dir or tempfile.mkdtemp())
    g.pre(**kw)
    return g


class GuardBehaviour(unittest.TestCase):

    # ---- registry ----

    def test_missing_registry_denies(self):
        with self.assertRaises(GateError):
            Gate("T", guards="/nonexistent/guards.json")

    def test_incomplete_registry_denies(self):
        reg = _load_registry()
        reg["guards"] = [g for g in reg["guards"] if g["id"] != "G-DIM"]
        path = _write_registry(reg)
        with self.assertRaises(GateError) as cm:
            Gate("T", guards=path)
        self.assertIn("G-DIM", str(cm.exception))

    def test_registry_ships_all_eight(self):
        ids = {g["id"] for g in _load_registry()["guards"]}
        self.assertEqual(ids, {"G-PRE", "G-FIT", "G-RES", "G-CTRL",
                               "G-LAYER", "G-DIM", "G-SUP", "G-IND"})

    # ---- G-PRE ----

    def test_nothing_runs_before_pre(self):
        g = Gate("T", guards=GUARDS)
        for call in (lambda: g.record("x", 1.0, "physical", "A"),
                     lambda: g.claim("c", supported_by=[]),
                     lambda: g.close(observed="o")):
            with self.assertRaises(GateError):
                call()

    def test_empty_declaration_field_denies(self):
        for field in ("question", "statistic", "expected"):
            with self.assertRaises(GateError):
                opened(**{field: "  "})

    def test_close_requires_an_observed_summary(self):
        g = opened()
        g.control_result("c", "ran")
        with self.assertRaises(GateError):
            g.close(observed="")

    def test_pre_is_not_reentrant(self):
        g = opened()
        with self.assertRaises(GateError):
            g.pre(question="q", statistic="s", discriminates="d", expected="e",
                  resolution=[Resolution("r", 1.0, 10.0)],
                  controls=[Control("c", predicted="p")])

    # ---- G-FIT ----

    def test_undeclared_discrimination_denies(self):
        with self.assertRaises(GateError) as cm:
            opened(discriminates="")
        self.assertIn("G-FIT", str(cm.exception))

    # ---- G-RES ----

    def test_coarse_instrument_denies(self):
        with self.assertRaises(GateError) as cm:
            opened(resolution=[Resolution("r", instrument=0.39, feature=0.063)])
        self.assertIn("G-RES", str(cm.exception))

    def test_margin_is_the_policy_dial(self):
        """Same two scales; only the margin differs."""
        with self.assertRaises(GateError):
            opened(resolution=[Resolution("r", 0.252, 0.334, margin=2.0)])
        self.assertTrue(
            opened(resolution=[Resolution("r", 0.252, 0.334, margin=1.0)])._opened)

    def test_resolution_is_mandatory(self):
        with self.assertRaises(GateError) as cm:
            opened(resolution=[])
        self.assertIn("G-RES", str(cm.exception))

    # ---- G-CTRL ----

    def test_controls_are_mandatory(self):
        with self.assertRaises(GateError) as cm:
            opened(controls=[])
        self.assertIn("G-CTRL", str(cm.exception))

    def test_control_without_a_prediction_denies(self):
        with self.assertRaises(GateError) as cm:
            opened(controls=[Control("c", predicted="")])
        self.assertIn("G-CTRL", str(cm.exception))

    def test_undeclared_control_result_denies(self):
        g = opened()
        with self.assertRaises(GateError):
            g.control_result("never declared", "1.0")

    def test_unrun_control_is_a_finding(self):
        g = opened(strict=False)
        report = g.close(observed="o", write=False)
        self.assertIn("G-CTRL", [f["guard"] for f in report["findings"]])
        self.assertFalse(report["declaration"]["controls"][0]["run"])

    # ---- G-LAYER ----

    def test_untagged_quantity_is_not_recorded(self):
        g = opened()
        with self.assertRaises(GateError):
            g.record("x", 1.0, "not-a-layer", "A")
        with self.assertRaises(GateError):
            g.record("x", 1.0, "physical", "   ")
        self.assertEqual(g.quantities, {})

    def test_promotion_needs_a_substantive_justification(self):
        g = opened()
        g.record("x", 1.0, "generator", "A")
        with self.assertRaises(GateError):
            g.promote("x", "x_phys", "physical", "because")

    def test_promotion_records_its_provenance(self):
        g = opened()
        g.record("x", 1.0, "generator", "A")
        g.promote("x", "x_phys", "physical",
                  "the generator parameter is measured independently downstream")
        self.assertEqual(g.quantities["x_phys"]["layer"], "physical")
        self.assertIn("promoted from x (generator)", g.quantities["x_phys"]["note"])

    def test_generator_quantities_are_flagged_at_close(self):
        g = opened(strict=False)
        g.record("seed", 42, "generator", "A")
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertEqual(report["generator_level_quantities"], ["seed"])

    # ---- G-DIM ----

    def test_ratio_across_unlike_objects_is_void(self):
        g = opened(strict=False)
        g.record("a", 0.0812, "physical", "lattice model")
        g.record("b", 0.0015, "physical", "cascade set")
        self.assertIsNone(g.ratio("r", "a", "b"))
        self.assertNotIn("r", g.quantities)
        self.assertEqual(g.voided[0]["name"], "r")

    def test_ratio_within_one_object_is_admissible(self):
        g = opened()
        g.record("a", 10.0, "physical", "A")
        g.record("b", 2.0, "physical", "A")
        self.assertEqual(g.ratio("r", "a", "b"), 5.0)
        self.assertEqual(g.quantities["r"]["object_of"], "A")

    def test_comparing_one_statistic_across_objects_is_untouched(self):
        """G-DIM voids ratios, not comparisons. A difference is fine."""
        g = opened()
        g.record("D_f_AB", 1.889, "physical", "AB tiling")
        g.record("D_f_cascade", 1.555, "physical", "cascade set")
        g.claim("the dimensions differ", supported_by=["D_f_AB", "D_f_cascade"])
        self.assertEqual(g.claims[0]["status"], "supported")

    def test_ratio_on_unknown_quantity_denies(self):
        g = opened(strict=False)
        g.record("a", 1.0, "physical", "A")
        with self.assertRaises(GateError):
            g.ratio("r", "a", "nope")

    # ---- G-SUP ----

    def test_claim_without_support_is_unsupported(self):
        g = opened(strict=False)
        g.claim("big result", supported_by=[])
        self.assertEqual(g.claims[0]["status"], "unsupported")

    def test_claim_naming_an_unrecorded_quantity_is_unsupported(self):
        g = opened(strict=False)
        g.claim("big result", supported_by=["ghost"])
        self.assertEqual(g.claims[0]["status"], "unsupported")

    def test_supported_claim_carries_its_support_layers(self):
        g = opened()
        g.record("x", 1.0, "physical", "A")
        g.record("s", 42, "generator", "A")
        g.claim("c", supported_by=["x", "s"])
        self.assertEqual(g.claims[0]["support_layers"], ["generator", "physical"])

    # ---- G-IND ----

    def test_convergence_without_named_shared_input_is_a_finding(self):
        g = opened(strict=False)
        g.convergence(across=["A", "B"], shared=[])
        self.assertIn("G-IND", [f["guard"] for f in g.findings])
        self.assertEqual(g.claims, [])

    def test_convergence_with_named_shared_input_is_qualified(self):
        g = opened()
        g.convergence(across=["A", "B"], shared=["the same point set"])
        self.assertEqual(g.claims[0]["status"], "qualified")

    # ---- strict vs non-strict ----

    def test_strict_raises_where_non_strict_records(self):
        with self.assertRaises(GateError):
            opened(strict=True).claim("c", supported_by=[])
        g = opened(strict=False)
        g.claim("c", supported_by=[])
        self.assertEqual(len(g.findings), 1)

    def test_pre_stage_denies_even_when_not_strict(self):
        """strict=False downgrades post-stage guards only."""
        with self.assertRaises(GateError):
            opened(strict=False, resolution=[Resolution("r", 10.0, 1.0)])

    # ---- report ----

    def test_close_writes_a_report_and_summarises(self):
        d = tempfile.mkdtemp()
        g = opened(strict=False, log_dir=d)
        g.record("x", 1.0, "physical", "A")
        g.control_result("c", "ran")
        report = g.close(observed="o")
        self.assertTrue(os.path.exists(report["_path"]))
        with open(report["_path"]) as fh:
            self.assertEqual(json.load(fh)["sim_id"], "T")
        self.assertIn("GATE T", g.summary(report))

    def test_gate_cannot_be_closed_twice(self):
        g = opened(strict=False)
        g.control_result("c", "ran")
        g.close(observed="o", write=False)
        with self.assertRaises(GateError):
            g.close(observed="o", write=False)


class ShippedDefects(unittest.TestCase):
    """
    Four defects in gate.py as delivered. Each test asserts the CURRENT
    behaviour, so fixing the module turns the test red on purpose.
    """

    def test_defect_1_docstring_example_denies_at_pre(self):
        """
        gate.py's module docstring presents a usage example that continues
        through record/claim/close. It cannot: 0.39 x 2.0 > 0.063, so
        G-RES denies at pre() and the example never reaches line two.
        """
        with self.assertRaises(GateError) as cm:
            opened(resolution=[Resolution("k-grid vs Bragg peak width",
                                          instrument=0.39, feature=0.063)])
        self.assertIn("G-RES", str(cm.exception))

    def test_defect_2_promote_silently_overwrites(self):
        """
        record() refuses to overwrite a recorded name. promote() does not
        check, so a promotion can replace an unrelated physical quantity —
        in the one operation G-LAYER exists to make explicit.
        """
        g = opened()
        g.record("x", 1.0, "generator", "A")
        g.record("y", 99.0, "physical", "A")
        g.promote("x", "y", "physical",
                  "a justification long enough to clear the length check")
        self.assertEqual(g.quantities["y"]["value"], 1.0)  # 99.0 is gone

    def test_defect_2b_ratio_silently_overwrites(self):
        """Same missing check in ratio()."""
        g = opened()
        g.record("a", 10.0, "physical", "A")
        g.record("b", 2.0, "physical", "A")
        g.record("r", 77.0, "physical", "A")
        g.ratio("r", "a", "b")
        self.assertEqual(g.quantities["r"]["value"], 5.0)  # 77.0 is gone

    def test_defect_3_strict_close_writes_no_report(self):
        """
        In strict mode an unrun control raises from close() before the
        report is written and before _closed is set. The gate denies, which
        is correct — but the forensic record is lost, and the gate is left
        open for a retry.
        """
        d = tempfile.mkdtemp()
        g = opened(strict=True, log_dir=d)
        with self.assertRaises(GateError):
            g.close(observed="o")
        self.assertEqual(os.listdir(d), [])
        self.assertFalse(g._closed)

    def test_defect_3b_retry_after_deny_reports_the_control_as_run(self):
        """
        The retry path. control_result() accepts any string, so answering a
        denied close() with a placeholder produces a clean report whose
        controls block says run=True. The finding survives in findings[],
        but summary() prints the control as "run" — the two disagree.
        """
        d = tempfile.mkdtemp()
        g = opened(strict=True, log_dir=d)
        with self.assertRaises(GateError):
            g.close(observed="o")
        g.control_result("c", "n/a")
        report = g.close(observed="o")
        self.assertTrue(report["declaration"]["controls"][0]["run"])
        self.assertIn("G-CTRL", [f["guard"] for f in report["findings"]])
        self.assertIn("control  : c                            run",
                      g.summary(report))

    def test_defect_4_malformed_registry_loads_then_crashes(self):
        """
        _load_guards checks that all eight ids are present but not that each
        carries a fail_message. A registry missing one loads fine and then
        raises KeyError — not GateError — at the moment that guard fires.
        A fail-closed tool should reject the registry at load.
        """
        reg = _load_registry()
        for g in reg["guards"]:
            g.pop("fail_message", None)
        path = _write_registry(reg)

        gate = Gate("T", guards=path)  # loads, wrongly
        with self.assertRaises(KeyError):
            gate.record("x", 1.0, "physical", "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
