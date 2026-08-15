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


class DeliveredRegistryAndReplay(unittest.TestCase):
    """
    Findings against the delivered guards.json and replay_sim_stack.py.
    Documented in ../AUDIT_NOTES.md sections 1-3. Each asserts CURRENT
    behaviour, so a repair turns a test red on purpose.
    """

    def test_g_res_verdict_depends_on_which_pair_is_declared(self):
        """
        AUDIT_NOTES section 1. Same sim, same guard, opposite verdicts,
        because replay declares the geometric resolution and retro
        declares the statistical one. Nothing forces the binding pair.
        """
        # replay: smallest box vs mean nearest-neighbour spacing
        self.assertTrue(
            opened(resolution=[Resolution("geometric", 0.05, 0.20)])._opened)
        # retro: estimator artifact floor vs claimed separation
        with self.assertRaises(GateError):
            opened(resolution=[Resolution("statistical", 0.252, 0.334)])

    def test_generator_quantity_can_support_a_physical_claim(self):
        """
        AUDIT_NOTES section 2. summary() prints 'no physical claim
        permitted' for generator-level quantities while claim() records a
        claim resting on one as supported, with no finding. G-LAYER
        guards tagging, not use.
        """
        g = opened(strict=True)
        g.record("Df_AB", 1.889, "physical", "Ammann-Beenker tiling")
        g.record("Df_cascade", 1.555, "generator", "branching_walk output")
        g.claim("the two sets do not share a fractal dimension",
                supported_by=["Df_AB", "Df_cascade"])
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)

        self.assertEqual(report["claims"][0]["status"], "supported")
        self.assertIn("generator", report["claims"][0]["support_layers"])
        self.assertEqual(report["findings"], [])          # nothing fired
        text = g.summary(report)
        self.assertIn("no physical claim permitted", text)
        self.assertIn("[supported]", text)                # both, same page

    def test_g_fit_documented_post_but_enforced_pre(self):
        """
        AUDIT_NOTES section 3. guards.json labels G-FIT stage 'post';
        gate.py denies on it inside pre().
        """
        entry = next(g for g in _load_registry()["guards"] if g["id"] == "G-FIT")
        self.assertEqual(entry["stage"], "post")
        with self.assertRaises(GateError) as cm:
            opened(discriminates="")       # denied before anything runs
        self.assertIn("G-FIT", str(cm.exception))

    def test_delivered_registry_carries_the_doc_fields(self):
        reg = _load_registry()
        self.assertEqual(reg["layers"], ["generator", "physical", "instrument"])
        for g in reg["guards"]:
            for field in ("id", "stage", "name", "rule", "fail_message",
                          "rationale"):
                self.assertIn(field, g)

    def test_guards_md_is_in_sync_with_guards_json(self):
        """GUARDS.md is generated. It must match a fresh render."""
        sys.path.insert(0, os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        import make_docs
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, "GUARDS.md")) as fh:
            on_disk = fh.read()
        self.assertEqual(on_disk, make_docs.render(_load_registry()))


class DeliveredReplayBehaviour(unittest.TestCase):
    """replay_sim_stack.py must keep doing what its docstring says."""

    def setUp(self):
        sys.path.insert(0, os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        self.cwd = os.getcwd()
        os.chdir(tempfile.mkdtemp())      # gate writes gate_<SIM>.json to cwd

    def tearDown(self):
        os.chdir(self.cwd)

    def test_sim_b_passes(self):
        import replay_sim_stack
        g, rep = replay_sim_stack.sim_b()
        self.assertEqual(rep["claims"][0]["status"], "supported")
        self.assertTrue(all(c["run"] for c in rep["declaration"]["controls"]))

    def test_sim_a_denies_at_pre(self):
        import replay_sim_stack
        with self.assertRaises(GateError) as cm:
            replay_sim_stack.sim_a()
        self.assertIn("G-RES", str(cm.exception))

    def test_sim_c_runs_but_voids_its_ratio(self):
        import replay_sim_stack
        g, rep = replay_sim_stack.sim_c()
        self.assertEqual(rep["voided_ratios"][0]["name"], "knee_over_Esplit")
        self.assertEqual(rep["claims"][0]["status"], "unsupported")
        fired = [f["guard"] for f in rep["findings"]]
        self.assertEqual(set(fired), {"G-DIM", "G-SUP", "G-IND"})


class DeliveredTools(unittest.TestCase):
    """
    Findings against mine_logs.py and explore.py. AUDIT_NOTES.md section 9.
    Assert CURRENT behaviour so a repair turns a test red.
    """

    def setUp(self):
        self.here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, self.here)

    def _corpus(self):
        """A gate log dir with one clean run and one that fired guards."""
        d = tempfile.mkdtemp()
        clean = opened(strict=False, log_dir=d)
        clean.record("x", 1.0, "physical", "A")
        clean.control_result("c", "ran")
        clean.close(observed="a restatement of the expectation, in other words")

        dirty = Gate("DIRTY", guards=GUARDS, strict=False, log_dir=d)
        dirty.pre(question="q", statistic="s", discriminates="d", expected="e",
                  resolution=[Resolution("r", 1.0, 10.0)],
                  controls=[Control("c", predicted="p")])
        dirty.control_result("c", "ran")
        dirty.claim("unsupported thing", supported_by=[])
        dirty.close(observed="o")
        return d

    def test_mine_logs_flags_a_sound_run_as_a_divergence(self):
        """
        The 'growth edge' section tests expected != observed on two
        free-text strings, which are never equal. Any run that fires no
        guard lands in the list -- including a sound one.
        """
        import mine_logs
        out = mine_logs.mine(self._corpus(), os.path.join(self.here, "guards.json"))
        flagged = [sim for sim, _, _ in out["uncaught"]]
        self.assertIn("T", flagged)          # the clean run, wrongly flagged
        self.assertNotIn("DIRTY", flagged)   # fired a guard, so excluded

    def test_mine_logs_cannot_see_denials(self):
        """
        A pre-stage deny raises before close(), so it writes no gate_*.json.
        The guard that stopped a run is invisible to the miner and reports
        as NEVER FIRED -- precisely because it worked.
        """
        d = tempfile.mkdtemp()
        with self.assertRaises(GateError):
            Gate("DENIED", guards=GUARDS, strict=False, log_dir=d).pre(
                question="q", statistic="s", discriminates="d", expected="e",
                resolution=[Resolution("too coarse", 0.39, 0.063)],
                controls=[Control("c", predicted="p")])
        self.assertEqual(os.listdir(d), [])

        import mine_logs
        out = mine_logs.mine(d, os.path.join(self.here, "guards.json"))
        self.assertEqual(out["runs"], 0)
        self.assertEqual(out["fires"], {})

    def test_explore_reads_sim_id_as_none_on_a_gate_report(self):
        """
        __main__ passes d["declaration"] into explore(), which then looks
        for sim_id inside it -- but sim_id is top-level in a gate report.
        """
        import explore as explore_mod
        d = tempfile.mkdtemp()
        g = opened(strict=False, log_dir=d)
        g.control_result("c", "ran")
        report = g.close(observed="o")
        with open(report["_path"]) as fh:
            loaded = json.load(fh)

        doc = explore_mod.explore(loaded["declaration"])
        self.assertIsNone(doc["sim"])                     # lost
        self.assertEqual(loaded["sim_id"], "T")           # present one level up
        self.assertEqual(len(doc["candidates"]), 21)


if __name__ == "__main__":
    unittest.main(verbosity=2)
