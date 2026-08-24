# SPDX-License-Identifier: CC0-1.0
"""
Repo-level test: study-watch opens a pull request and merges nothing, and
never emits a count, a rate or a trend.

Both are stated in comments and in a README. A statement in a comment is a
promise; this is the property. Same reason tests/test_gate_drift.py exists.

    python3 -m unittest discover tests
"""

import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "study-watch.yml")
MODULE = os.path.join(ROOT, "notes", "study_watch.py")

sys.path.insert(0, os.path.join(ROOT, "notes"))
import study_watch as sw  # noqa: E402


def _uncommented(path):
    """
    Comment lines stripped. The workflow's own header says there is no
    `gh pr merge` and no `--auto`, so a naive substring search finds the
    words in the sentence forbidding them -- the third use/mention catch of
    this kind in this folder's history. The check reads code, not prose.
    """
    out = []
    for line in open(path, encoding="utf-8"):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        out.append(line.split(" #")[0] if " #" in line else line)
    return "".join(out)


class MergesNothing(unittest.TestCase):

    def test_workflow_exists(self):
        self.assertTrue(os.path.exists(WORKFLOW))

    def test_no_merge_invocation(self):
        body = _uncommented(WORKFLOW)
        for pat in (r"gh\s+pr\s+merge", r"--auto\b", r"auto_merge",
                    r"merge_method", r"pull-request-merge"):
            self.assertIsNone(
                re.search(pat, body, re.I),
                "workflow contains %r outside a comment. The pull request "
                "is the gate; no merge path may exist." % pat)

    def test_no_standing_model_approver(self):
        body = _uncommented(WORKFLOW)
        for pat in (r"approve", r"review_event\s*:\s*APPROVE"):
            self.assertIsNone(
                re.search(pat, body, re.I),
                "workflow contains %r outside a comment; no model is a "
                "standing approver." % pat)

    def test_opens_a_pull_request(self):
        self.assertIn("gh pr create", _uncommented(WORKFLOW))

    def test_null_test_runs_before_retrieval(self):
        body = _uncommented(WORKFLOW)
        self.assertLess(body.index("--null"), body.index("--live"),
                        "the null test must run before the first real run")


class NotificationOnly(unittest.TestCase):

    def test_guard_refuses_a_count(self):
        with self.assertRaises(sw.MetricEmitted):
            sw.assert_no_metric("14 papers were retrieved")

    def test_guard_refuses_a_trend(self):
        with self.assertRaises(sw.MetricEmitted):
            sw.assert_no_metric("the publication rate rose")

    def test_guard_refuses_a_percentage(self):
        with self.assertRaises(sw.MetricEmitted):
            sw.assert_no_metric("about 40% of candidates")

    def test_guard_admits_ordinary_notification(self):
        sw.assert_no_metric("a candidate is listed below with its residue")

    def test_guard_matches_the_word_not_the_quantity(self):
        """
        Recorded, not repaired. The guard refuses a sentence FORBIDDING a
        rate, because it matches the word. Left strict: over-refusing a
        line the module authored is the cheap direction, and an exemption
        list is the first thing a real rate would arrive through.
        """
        with self.assertRaises(sw.MetricEmitted):
            sw.assert_no_metric("no count, rate or trend is emitted")


class SkipPathIsExercised(unittest.TestCase):

    def test_selftest_exits_clean(self):
        p = subprocess.run([sys.executable, MODULE, "--selftest"], cwd=ROOT,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout.decode()[-2000:])

    def test_entries_without_would_measure_are_listed_not_invented(self):
        watchable, unwatchable = sw.split_watchable(sw.load_entries())
        self.assertTrue(watchable)
        self.assertTrue(unwatchable,
                        "no NOT WATCHABLE entry; the skip path would be "
                        "unexercised and the rule untested")
        for e in unwatchable:
            self.assertIsNone(e["would_measure"])

    def test_matches_would_measure_is_never_filled_mechanically(self):
        row = sw.stage2("We show that populations declined at all sites.")
        self.assertEqual(row["matches_would_measure"], sw.UNADJUDICATED)

    def test_an_instruction_is_recognised_not_transformed(self):
        v = sw.verbalize("count caveats issued per account type")
        self.assertEqual(v["route"], sw.IMPERATIVE)
        self.assertIn("count caveats", v["form"])

    def test_a_non_instruction_is_refused_not_mangled(self):
        """
        Fronting these produced `seting tasks` and `houring off`. A residue
        that is not a sentence cannot be judged for whether it needs a
        bearer, so verbalize() returns a reason instead of a string.
        """
        v = sw.verbalize("bidirectional protocol; each side sets tasks in "
                         "its own modality")
        self.assertEqual(v["route"], sw.NOT_VERBALIZABLE)
        self.assertIsNone(v["form"])

    def test_verbalizable_would_measure_reads_process(self):
        r = sw.would_measure_reading(
            {"would_measure": "count caveats issued per account type"})
        self.assertEqual(r["reading"], sw.PROCESS)

    def test_null_test_arms_build_and_match(self):
        r = sw.null_test(verbose=False)
        self.assertTrue(r["assessability_arms_ok"])
        self.assertTrue(r["reading_arms_ok"])
        self.assertTrue(r["blocked_nouns"],
                        "no head noun blocked on the reading arm; the "
                        "finding about word-list-decided nouns would be "
                        "unearned")


if __name__ == "__main__":
    unittest.main()
