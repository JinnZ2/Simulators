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


if __name__ == "__main__":
    unittest.main()
