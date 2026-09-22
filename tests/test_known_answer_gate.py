# SPDX-License-Identifier: CC0-1.0
"""
Repo-level test: no metric ships without a known-answer run.

Twice in this repo a metric was wrong in a way reading it would not have
caught, and both times a case with a fixed-in-advance answer caught it.
`tools/known_answer.py` makes that a step rather than a habit. This test is
what makes the step fire without anyone remembering to run it.

    python3 -m unittest discover tests

THE MANIFEST IS THE WEAK POINT, and it is named here rather than hidden.
Coverage is a hand-kept list below, not a scan. Deciding whether a function
is a metric is not a lexical property of its name, and a repo-wide scan for
metric-shaped functions would be the word-list failure `nonidentity-census`
T1-1 measured, one level up. A metric added without being added to the
manifest is invisible to this test.

Enforcement is at the manifest, not at the callsite. Nothing in the repo
currently calls `require()` in anger, so the gate does not fire while a
metric is being used -- it fires here. That is a real limit: it catches an
unregistered metric at test time and not an unrun one at use time.
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "known_answer.py")

sys.path.insert(0, os.path.join(ROOT, "tools"))
import known_answer as ka  # noqa: E402


# Hand-kept. Every entry must be registered with a known-answer case.
MANIFEST = (
    "null-harness/null_harness.py::_verdict",
    "nonidentity-census/t6_window_declaration.py::decided_by_tracks_window",
    "nonidentity-census/t6_window_declaration.py::"
    "marginal_majority (REPLACED)",
    "shape-spec-audit/shadow_read.py::outline_area",
    "sim-span/sim_span.py::quad_fit",
    "sim-span/three_column.py::ols",
    "sheet-structure-scan/sheetmodel.py::rank",
    "agent-lifecycle-energy/phase_energy.py::integrate",
    "operator-machine-coupling/coupling_separation.py::interaction_fraction",
    "model-deprecation-backcast/null_check.py::lag_of_peak",
    "routing-data-layer/rate_form.py::sustained_excess",
    "frame-location-benchmark/score.py::false_positive_rate",
    "gap-existence-cases/commit_store.py::commit_specificity",
    "crediting-rate/crediting_rate.py::bin_gap",
    "anchor-measurand-crossing/amc.py::crossing_band",
    "anchor-position/normalize.py::crossing_count",
    "ontology-probe/probe.py::rates",
    "ontology-probe/probe.py::absent_coverage",
    "return-path/return_path.py::ratio",
    "trigger-geometry/trigger_geometry.py::accumulation_ratio",
    "terminal-crossing/crossing_rate.py::expected_crossings",
    "unowned-join/invariant.py::join_coverage",
    "failure-mode-register/register.py::fraction_cap",
    "failure-mode-register/register_v2.py::joint_survival",
    "internal-reference-boundary/radials.py::effective_origins",
    "internal-reference-boundary/radials.py::sanction_ratio_point",
    "move-set/move_set_sim_v2.py::coverage",
    "move-set/move_set_sim_v2.py::_halfwidth",
    "revision-survival/revision_survival.py::delta",
    "additivity-inheritance/additivity_inheritance.py::interaction_ss",
    "credential-channel/credential_channel.py::routing_cost",
    "criterion-externality/criterion_externality.py::expected_rate",
    "deep-research-correction/check.py::count_relation",
    "reporting-chain-loss/hop_compose.py::composed_bias",
    "chain-position/load_class.py::stability_product",
    "measurand-partition/wo4_lumber.py::stiffness_ratio",
)

# Cases known to fail today. A case that starts passing turns this red so
# the note in tools/known_answer.py has to be corrected.
PINNED = (
    ("null-harness/null_harness.py::_verdict",
     "half-signal vs full-signal"),
    ("nonidentity-census/t6_window_declaration.py::"
     "marginal_majority (REPLACED)", "matched set"),
)


class ToolRuns(unittest.TestCase):

    def test_the_tool_exists(self):
        self.assertTrue(os.path.exists(TOOL))

    def test_tool_exits_clean(self):
        """rc 0 means every case agrees with what the registry expects."""
        p = subprocess.run([sys.executable, TOOL], cwd=ROOT,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout.decode()[-2000:])


class ManifestIsCovered(unittest.TestCase):

    def setUp(self):
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.seed()

    def test_every_manifest_entry_is_registered(self):
        missing = [m for m in MANIFEST if m not in ka.registry_ids()]
        self.assertEqual(missing, [],
                         "manifest entries with no known-answer case: %r"
                         % missing)

    def test_every_registered_metric_runs(self):
        for mid in ka.registry_ids():
            ka.run(mid)
            self.assertTrue(ka.require(mid))

    def test_pinned_failures_still_fail(self):
        """
        These are defects, not passes. If one starts passing the defect was
        repaired and the note recording it is now wrong.
        """
        for mid, cname in PINNED:
            rows = {r["case"]: r for r in ka.run(mid)}
            self.assertIn(cname, rows)
            self.assertEqual(
                rows[cname]["status"], ka.FAIL,
                "%s :: %s now passes. The defect was repaired; update the "
                "note in tools/known_answer.py and drop it from PINNED."
                % (mid, cname))

    def test_no_case_disagrees_with_the_registry(self):
        for mid in ka.registry_ids():
            ka.run(mid)
            self.assertEqual(ka.unexpected(mid), [],
                             "%s has cases disagreeing with the registry"
                             % mid)


class TheGateFires(unittest.TestCase):
    """
    Planted violations. A gate nobody has seen refuse anything is not known
    to be a gate -- same reason tests/test_gate_drift.py plants a stale copy.
    """

    def test_require_raises_for_an_unregistered_metric(self):
        with self.assertRaises(ka.KnownAnswerNotRun):
            ka.require("no/such/metric::nowhere")

    def test_require_raises_when_registered_but_never_run(self):
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.register("planted::never_run", lambda x: x,
                    [ka.case("a", (1,), 1, "identity"),
                     ka.case("b", (2,), 2, "identity")])
        with self.assertRaises(ka.KnownAnswerNotRun):
            ka.require("planted::never_run")

    def test_case_set_with_one_expected_answer_is_refused(self):
        """
        The failure both seeds are instances of is a metric that returns the
        same thing regardless. A case set expecting one answer cannot detect
        it. This is the rule that refused the first draft of the seed.
        """
        with self.assertRaises(ka.BadCaseSet):
            ka.register("planted::constant_cases", lambda x: True,
                        [ka.case("a", (1,), True, "known"),
                         ka.case("b", (2,), True, "known")])

    def test_case_without_a_stated_basis_is_refused(self):
        with self.assertRaises(ka.BadCaseSet):
            ka.case("a", (1,), 1, "")

    def test_empty_case_set_is_refused(self):
        with self.assertRaises(ka.BadCaseSet):
            ka.register("planted::no_cases", lambda x: x, [])

    def test_the_registry_is_complete(self):
        """Expected against registered. A register(...) call shadowed by a
        `finally` inside a helper once landed and never executed: the
        registry reported one fewer metric than the file contains, every
        metric that DID register still passed, and nothing said so. A
        count taken from the calls cannot catch that; an expected set
        can."""
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.seed()
        comp = ka.completeness()
        self.assertEqual(comp["state"], "COMPLETE",
                         "missing=%s extra=%s"
                         % (comp["missing"], comp["extra"]))

    def test_completeness_catches_a_shadowed_registration(self):
        """The plant. A completeness check that cannot report SHORT is a
        line of prose, so this removes one registration and requires the
        check to name it."""
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.seed()
        victim = ka.EXPECTED_METRICS[0]
        del ka._REGISTRY[victim]
        comp = ka.completeness()
        self.assertEqual(comp["state"], "SHORT")
        self.assertIn(victim, comp["missing"])
        self.assertFalse(comp["ok"])
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.seed()

    def test_a_constant_metric_is_caught_by_a_valid_case_set(self):
        """End to end: the planted constant metric must FAIL, not error."""
        ka._REGISTRY.clear()
        ka._RESULTS.clear()
        ka.register("planted::always_true", lambda *a: True,
                    [ka.case("wants true", (1,), True, "constructed"),
                     ka.case("wants false", (2,), False, "constructed")])
        rows = {r["case"]: r["status"] for r in ka.run("planted::always_true")}
        self.assertEqual(rows["wants true"], ka.PASS)
        self.assertEqual(rows["wants false"], ka.FAIL)


class SeedReachability(unittest.TestCase):
    """Third occurrence of one shape: a register() call that runs at import
    and is not on seed()'s path. FMR_036 was a register after a `finally`,
    MSV_013 the same again, MSV_024 a helper called from the module tail.
    All three were repaired where they were found. This is the structural
    form -- a call graph closed from seed() -- so a fourth fails the run
    instead of waiting to be noticed."""

    def test_every_registration_is_reachable_from_seed(self):
        r = ka.seed_reachable()
        self.assertTrue(
            r["ok"],
            "register() call sites seed() cannot reach: %s" % r["unreachable"])

    def test_the_check_names_the_functions_that_register(self):
        """A reachability check that found no register() calls at all would
        also pass. This pins that it found them."""
        r = ka.seed_reachable()
        self.assertIn("seed", r["registering_functions"])
        self.assertIn("_seed_move_set", r["registering_functions"])

    def test_a_tail_only_registration_is_caught(self):
        """The plant, arm 1 -- MSV_024's exact shape."""
        src = ("def register(a): pass\n"
               "def _late():\n"
               "    register('x')\n"
               "def seed():\n"
               "    register('a')\n"
               "_late()\n")
        r = ka.seed_reachable(src=src)
        self.assertFalse(r["ok"])
        self.assertEqual([fn for fn, _ in r["unreachable"]], ["_late"])

    def test_a_module_level_registration_is_caught(self):
        """The plant, arm 2 -- a register() in no function at all."""
        src = ("def register(a): pass\n"
               "def seed():\n"
               "    register('a')\n"
               "register('b')\n")
        r = ka.seed_reachable(src=src)
        self.assertFalse(r["ok"])
        self.assertEqual([fn for fn, _ in r["unreachable"]], [None])

    def test_a_registration_seed_reaches_is_not_caught(self):
        """The negative. A check that refuses every file is not a check."""
        src = ("def register(a): pass\n"
               "def _late():\n"
               "    register('x')\n"
               "def seed():\n"
               "    register('a')\n"
               "    _late()\n")
        self.assertTrue(ka.seed_reachable(src=src)["ok"])

    def test_reachability_is_transitive(self):
        """seed -> a -> b -> register() is reachable. A one-hop check would
        report this as a violation and send the next reader to repair a
        registration that is fine."""
        src = ("def register(a): pass\n"
               "def _b():\n"
               "    register('x')\n"
               "def _a():\n"
               "    _b()\n"
               "def seed():\n"
               "    _a()\n")
        self.assertTrue(ka.seed_reachable(src=src)["ok"])

    def test_no_other_file_registers(self):
        """A register() in another file is outside seed() by construction.
        Currently a visible zero, kept so it stays one."""
        self.assertEqual(ka.registration_sites_elsewhere(), [])


if __name__ == "__main__":
    unittest.main()
