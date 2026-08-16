"""
Tests for gate.py.

Two halves, deliberately separated:

  GuardBehaviour   — the eight guards do what guards.json says they do.
  RepairedDefects  — the defects found on landing, now fixed. These tests
                     asserted the broken behaviour until the repair; they
                     now assert the fix, so a regression turns them red.

The defects and their repairs are documented in ../AUDIT_NOTES.md.

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


class RepairedDefects(unittest.TestCase):
    """
    D1-D4, found on landing and since fixed. Each test asserted the broken
    behaviour before the repair and asserts the fix now.
    """

    # ---- D1: the docstring's usage example must actually run ----

    def test_d1_docstring_example_runs(self):
        """
        The module docstring declared instrument=0.39 against feature=0.063
        and then continued through record/claim/close. It could not: G-RES
        denied at pre(). The example now declares a resolution that passes,
        and the SIM-A numbers are kept in a clearly labelled DENIAL EXAMPLE.
        """
        g = opened(resolution=[Resolution("k-grid vs Bragg peak width",
                                          instrument=0.020, feature=0.063)])
        g.control_result("c", "peaks resolved")
        g.record("alpha_tail_AB", -1.529, "physical", "AB tiling")
        g.claim("AB is quasi-crystalline", supported_by=["alpha_tail_AB"])
        report = g.close(observed="only k=0 present", diverged=True,
                         write=False)
        self.assertEqual(report["claims"][0]["status"], "supported")

    def test_d1_the_denial_example_still_denies(self):
        with self.assertRaises(GateError) as cm:
            opened(resolution=[Resolution("k-grid vs Bragg peak width",
                                          instrument=0.39, feature=0.063)])
        self.assertIn("G-RES", str(cm.exception))

    # ---- D2: promote() and ratio() must not overwrite ----

    def test_d2_promote_refuses_to_overwrite(self):
        g = opened()
        g.record("x", 1.0, "generator", "A")
        g.record("y", 99.0, "physical", "A")
        with self.assertRaises(GateError) as cm:
            g.promote("x", "y", "physical",
                      "a justification long enough to clear the length check")
        self.assertIn("already recorded", str(cm.exception))
        self.assertEqual(g.quantities["y"]["value"], 99.0)   # preserved

    def test_d2_ratio_refuses_to_overwrite(self):
        g = opened()
        g.record("a", 10.0, "physical", "A")
        g.record("b", 2.0, "physical", "A")
        g.record("r", 77.0, "physical", "A")
        with self.assertRaises(GateError) as cm:
            g.ratio("r", "a", "b")
        self.assertIn("already recorded", str(cm.exception))
        self.assertEqual(g.quantities["r"]["value"], 77.0)   # preserved

    def test_d2_promote_and_ratio_still_work_on_fresh_names(self):
        g = opened()
        g.record("x", 1.0, "generator", "A")
        g.promote("x", "x_phys", "physical",
                  "measured independently downstream of the generator")
        g.record("b", 2.0, "physical", "A")
        self.assertEqual(g.quantities["x_phys"]["layer"], "physical")
        self.assertEqual(g.ratio("q", "x_phys", "b"), 0.5)

    # ---- D3: a denied close must leave a record and close the gate ----

    def test_d3_strict_close_writes_a_denial_record(self):
        d = tempfile.mkdtemp()
        g = opened(strict=True, log_dir=d)
        with self.assertRaises(GateError):
            g.close(observed="o")
        self.assertEqual(os.listdir(d), ["gate_T.denied.json"])
        with open(os.path.join(d, "gate_T.denied.json")) as fh:
            rec = json.load(fh)
        self.assertEqual(rec["outcome"], "DENIED")
        self.assertEqual(rec["denied_by"], "G-CTRL")

    def test_d3_the_retry_bypass_is_closed(self):
        """
        Catching the denial, answering the control with a placeholder and
        closing again used to produce a clean report claiming run: True.
        The gate now closes before denying, so nothing further is accepted.
        """
        d = tempfile.mkdtemp()
        g = opened(strict=True, log_dir=d)
        with self.assertRaises(GateError):
            g.close(observed="o")
        self.assertTrue(g._closed)
        with self.assertRaises(GateError):
            g.control_result("c", "n/a")
        with self.assertRaises(GateError):
            g.close(observed="o")

    def test_d3_pre_stage_denials_also_leave_a_record(self):
        d = tempfile.mkdtemp()
        with self.assertRaises(GateError):
            Gate("DENIED", guards=GUARDS, log_dir=d).pre(
                question="q", statistic="s", discriminates="d", expected="e",
                resolution=[Resolution("too coarse", 0.39, 0.063)],
                controls=[Control("c", predicted="p")])
        with open(os.path.join(d, "gate_DENIED.denied.json")) as fh:
            rec = json.load(fh)
        self.assertEqual(rec["denied_by"], "G-RES")

    def test_d3_empty_control_result_is_refused(self):
        g = opened()
        with self.assertRaises(GateError):
            g.control_result("c", "   ")

    # ---- D4: a registry without fail_messages must not load ----

    def test_d4_registry_missing_fail_message_is_rejected_at_load(self):
        reg = _load_registry()
        for g in reg["guards"]:
            g.pop("fail_message", None)
        with self.assertRaises(GateError) as cm:
            Gate("T", guards=_write_registry(reg))
        self.assertIn("no fail_message", str(cm.exception))

    def test_d4_one_blank_fail_message_is_enough_to_reject(self):
        reg = _load_registry()
        for g in reg["guards"]:
            if g["id"] == "G-DIM":
                g["fail_message"] = "   "
        with self.assertRaises(GateError) as cm:
            Gate("T", guards=_write_registry(reg))
        self.assertIn("G-DIM", str(cm.exception))


class DivergenceCall(unittest.TestCase):
    """close(diverged=...) — the author's explicit call, not inferred."""

    def test_diverged_defaults_to_unassessed(self):
        g = opened(strict=False)
        g.control_result("c", "ran")
        self.assertIsNone(g.close(observed="o", write=False)["diverged"])

    def test_diverged_is_recorded_verbatim(self):
        for value in (True, False):
            g = opened(strict=False)
            g.control_result("c", "ran")
            report = g.close(observed="o", diverged=value, write=False)
            self.assertIs(report["diverged"], value)

    def test_diverged_rejects_a_non_verdict(self):
        g = opened(strict=False)
        g.control_result("c", "ran")
        with self.assertRaises(GateError):
            g.close(observed="o", diverged="maybe")

    def test_summary_shows_the_divergence_call(self):
        g = opened(strict=False)
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertIn("NOT ASSESSED", g.summary(report))


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

    def test_generator_support_downgrades_a_physical_claim(self):
        """
        AUDIT_NOTES section 2, repaired. summary() used to print 'no
        physical claim permitted' directly above a claim resting on one,
        recorded as supported, with findings empty. G-LAYER guarded the
        tagging of quantities and not their use.
        """
        g = opened(strict=True)
        g.record("Df_AB", 1.889, "physical", "Ammann-Beenker tiling")
        g.record("Df_cascade", 1.555, "generator", "branching_walk output")
        g.claim("the two sets do not share a fractal dimension",
                supported_by=["Df_AB", "Df_cascade"])
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)

        claim = report["claims"][0]
        self.assertEqual(claim["status"], "qualified")
        self.assertIn("Df_cascade", claim["layer_note"])
        self.assertIn("G-LAYER", [f["guard"] for f in report["findings"]])
        text = g.summary(report)
        self.assertIn("no physical claim permitted", text)
        self.assertIn("[qualified]", text)
        self.assertNotIn("[supported]", text)

    def test_a_generator_scoped_claim_is_not_downgraded(self):
        """The downgrade is about scope, not about touching the generator."""
        g = opened(strict=True)
        g.record("Df_cascade", 1.555, "generator", "branching_walk output")
        g.claim("the branching walk produces D_f = 1.555 at these parameters",
                supported_by=["Df_cascade"], scope="generator")
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertEqual(report["claims"][0]["status"], "supported")
        self.assertEqual(report["findings"], [])

    def test_a_purely_physical_claim_is_not_downgraded(self):
        g = opened(strict=True)
        g.record("Df_AB", 1.889, "physical", "Ammann-Beenker tiling")
        g.record("spread", 0.075, "instrument", "box-count estimator")
        g.claim("AB sits in the space-filling cluster",
                supported_by=["Df_AB", "spread"])
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertEqual(report["claims"][0]["status"], "supported")

    def test_physical_claim_with_no_physical_support_is_downgraded(self):
        """
        A residual count is a property of the classifier; an artifact floor
        of the estimator. Neither becomes a property of the system by being
        counted. A physical claim resting only on instrument quantities is
        a promotion without a step.
        """
        g = opened(strict=True)
        g.record("residual_count", 3, "instrument", "the coverage classifier")
        g.record("threshold", 0.6, "instrument", "the coverage classifier")
        g.claim("the design has 3 unmeasured quantities",
                supported_by=["residual_count", "threshold"])
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)

        claim = report["claims"][0]
        self.assertEqual(claim["status"], "qualified")
        self.assertIn("no physical-level support", claim["layer_note"])
        self.assertIn("G-LAYER", [f["guard"] for f in report["findings"]])

    def test_instrument_support_alongside_physical_is_not_downgraded(self):
        """
        The bound case. 'The separation exceeds the estimator's error bar'
        needs the error bar, and downgrading that would be wrong.
        """
        g = opened(strict=True)
        g.record("separation", 0.334, "physical", "AB tiling vs cascade set")
        g.record("error_bar", 0.075, "instrument", "box-count estimator")
        g.claim("the separation exceeds the estimator's error bar",
                supported_by=["separation", "error_bar"])
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertEqual(report["claims"][0]["status"], "supported")
        self.assertEqual(report["findings"], [])

    def test_instrument_scoped_claim_on_instrument_support_stands(self):
        g = opened(strict=True)
        g.record("residual_count", 3, "instrument", "the coverage classifier")
        g.claim("the classifier reports 3 unreached questions",
                supported_by=["residual_count"], scope="instrument")
        g.control_result("c", "ran")
        report = g.close(observed="o", write=False)
        self.assertEqual(report["claims"][0]["status"], "supported")

    def test_an_unknown_claim_scope_denies(self):
        g = opened(strict=False)
        g.record("x", 1.0, "physical", "A")
        with self.assertRaises(GateError):
            g.claim("c", supported_by=["x"], scope="hypothesis")

    def test_g_fit_is_documented_at_the_stage_it_fires(self):
        """AUDIT_NOTES section 3, repaired: G-FIT was labelled 'post'."""
        entry = next(g for g in _load_registry()["guards"] if g["id"] == "G-FIT")
        self.assertEqual(entry["stage"], "pre")
        with self.assertRaises(GateError) as cm:
            opened(discriminates="")
        self.assertIn("G-FIT", str(cm.exception))

    def test_g_ctrl_declares_both_stages_it_fires_at(self):
        entry = next(g for g in _load_registry()["guards"] if g["id"] == "G-CTRL")
        self.assertEqual(entry["stage"], ["pre", "post"])

    def test_delivered_registry_carries_the_doc_fields(self):
        reg = _load_registry()
        self.assertEqual(reg["layers"], ["generator", "physical", "instrument"])
        for g in reg["guards"]:
            for field in ("id", "stage", "name", "rule", "fail_message",
                          "rationale"):
                self.assertIn(field, g)


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
        # Passes -- no denial -- but its claim is qualified, not supported:
        # Df_cascade is generator-level and the claim is physical-scope.
        self.assertEqual(rep["outcome"], "CLOSED")
        self.assertEqual(rep["claims"][0]["status"], "qualified")
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


class RepairedTools(unittest.TestCase):
    """
    mine_logs.py and explore.py, repaired. AUDIT_NOTES.md section 9.
    """

    def setUp(self):
        self.here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, self.here)
        self.guards = os.path.join(self.here, "guards.json")

    def _corpus(self):
        """One sound run, one that fired guards, one denied outright."""
        d = tempfile.mkdtemp()

        sound = opened(strict=False, log_dir=d)
        sound.record("x", 1.0, "physical", "A")
        sound.control_result("c", "ran")
        sound.close(observed="a restatement of the expectation, other words",
                    diverged=False)

        dirty = Gate("DIRTY", guards=GUARDS, strict=False, log_dir=d)
        dirty.pre(question="q", statistic="s", discriminates="d", expected="e",
                  resolution=[Resolution("r", 1.0, 10.0)],
                  controls=[Control("c", predicted="p")])
        dirty.control_result("c", "ran")
        dirty.claim("unsupported thing", supported_by=[])
        dirty.close(observed="o", diverged=True)

        with self.assertRaises(GateError):
            Gate("DENIED", guards=GUARDS, strict=False, log_dir=d).pre(
                question="q", statistic="s", discriminates="d", expected="e",
                resolution=[Resolution("too coarse", 0.39, 0.063)],
                controls=[Control("c", predicted="p")])
        return d

    def test_a_sound_run_is_no_longer_flagged_as_a_divergence(self):
        """
        The growth edge used to test expected != observed on free text,
        which is never equal, so every guard-free run landed in it. It now
        reads the author's explicit diverged call.
        """
        import mine_logs
        out = mine_logs.mine(self._corpus(), self.guards)
        self.assertEqual([sim for sim, _, _ in out["uncaught"]], [])

    def test_a_real_uncaught_divergence_is_still_reported(self):
        """diverged=True with no guard fired is the case worth surfacing."""
        d = tempfile.mkdtemp()
        g = opened(strict=False, log_dir=d)
        g.record("x", 1.0, "physical", "A")
        g.control_result("c", "ran")
        g.close(observed="nothing like the prediction", diverged=True)

        import mine_logs
        out = mine_logs.mine(d, self.guards)
        self.assertEqual([sim for sim, _, _ in out["uncaught"]], ["T"])

    def test_unassessed_runs_are_named_not_guessed(self):
        d = tempfile.mkdtemp()
        g = opened(strict=False, log_dir=d)
        g.control_result("c", "ran")
        g.close(observed="o")                      # no diverged call

        import mine_logs
        out = mine_logs.mine(d, self.guards)
        self.assertEqual(out["unassessed"], ["T"])
        self.assertEqual(out["uncaught"], [])

    def test_mine_logs_counts_denials(self):
        """
        A guard that stops a run used to leave no log and report NEVER
        FIRED. Denial records are now written and counted.
        """
        import mine_logs
        out = mine_logs.mine(self._corpus(), self.guards)
        self.assertEqual(out["denied"], 1)
        self.assertEqual(out["closed"], 2)
        self.assertEqual(out["denies"].get("G-RES"), 1)
        self.assertEqual(out["fires"].get("G-SUP"), 1)

    def test_explore_finds_sim_id_in_a_gate_report(self):
        import explore as explore_mod
        d = tempfile.mkdtemp()
        g = opened(strict=False, log_dir=d)
        g.control_result("c", "ran")
        report = g.close(observed="o")
        with open(report["_path"]) as fh:
            loaded = json.load(fh)

        doc = explore_mod.explore(loaded)
        self.assertEqual(doc["sim"], "T")
        self.assertEqual(doc["question"], "q")
        self.assertEqual(len(doc["candidates"]), 21)

    def test_explore_still_accepts_a_bare_declaration(self):
        import explore as explore_mod
        doc = explore_mod.explore({"question": "q", "statistic": "s"})
        self.assertIsNone(doc["sim"])
        self.assertEqual(doc["question"], "q")


class GeneratedDocs(unittest.TestCase):

    def test_guards_md_matches_a_fresh_render(self):
        sys.path.insert(0, os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        import make_docs
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, "GUARDS.md")) as fh:
            self.assertEqual(fh.read(), make_docs.render(_load_registry()))

    def test_a_multi_stage_guard_renders_under_each_stage(self):
        sys.path.insert(0, os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        import make_docs
        text = make_docs.render(_load_registry())
        pre = text.index("## PRE"), text.index("## MID")
        post = text.index("## POST")
        self.assertTrue(pre[0] < text.index("### G-CTRL") < pre[1])
        self.assertTrue(post < text.rindex("### G-CTRL"))
        self.assertIn("Also fires at: post", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
