# SPDX-License-Identifier: CC0-1.0
"""Pins the outside-case run after the tol-mode rule and the cue-sign split.

As run now: OC-1 AGREE (refused), OC-2..OC-5 DISAGREE (refused). None of the
five counts toward the lift: OC-1 and OC-2 are NON_INDEPENDENT (the code
changes answer them), OC-3..OC-5 are CASE_AUTHOR_ERROR (tol with no mode).
STATE SELF-GRADED until fresh cases, written from the spec text alone,
run as authored.

History these pins replace: before both changes, 3 of 5 agreed (OC-3..5),
recorded in samples/run_outside.sample.txt @ bd7d055.

Run: python3 threshold-states/test_outside.py
"""
import os
import subprocess
import sys
import unittest
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interaction as ix  # noqa: E402
import run_outside as ro  # noqa: E402

AUTHORED = {
    "OC-1": ({"kind": "REFUSE"}, [9, 1], 9.5, 0.1),
    "OC-2": ({"kind": "NOT", "relation": "BELOW_RESOLUTION"}, [5, -3], 4, 0.1),
    "OC-3": ({"kind": "EQUALS", "relation": "BELOW_RESOLUTION"}, [0, 0], 0, 0.1),
    "OC-4": ({"kind": "EQUALS", "relation": "ADDITIVE"}, [3, 2, 1], 6.0, 0.1),
    "OC-5": ({"kind": "EQUALS", "relation": "RESONANT"}, [1, 1], 10, 0.1),
}
STATUS = {"OC-1": "NON_INDEPENDENT", "OC-2": "NON_INDEPENDENT",
          "OC-3": "CASE_AUTHOR_ERROR", "OC-4": "CASE_AUTHOR_ERROR",
          "OC-5": "CASE_AUTHOR_ERROR"}


class Intake(unittest.TestCase):
    def test_expectations_are_as_authored(self):
        d = ro.load()
        self.assertEqual(d["author"], "chat-side")
        self.assertTrue(d["authored_outside_module"])
        got = {c["id"]: (c["expect"], c["separate"], c["joint"], c["tol"])
               for c in d["cases"]}
        self.assertEqual(got, AUTHORED)

    def test_statuses_recorded(self):
        d = ro.load()
        self.assertEqual({c["id"]: c["status"] for c in d["cases"]}, STATUS)
        for c in d["cases"]:
            self.assertTrue(c["status_note"].strip(), c["id"])

    def test_oc1_vector_matches_the_stated_references(self):
        c = ro.load()["cases"][0]
        self.assertEqual(ix.references(c["separate"]), (10, 9))


class Run(unittest.TestCase):
    def setUp(self):
        self.res = ro.run()
        self.by = {r["id"]: r for r in self.res["rows"]}

    def test_pinned_verdicts(self):
        self.assertEqual({k: r["verdict"] for k, r in self.by.items()}, {
            "OC-1": "AGREE", "OC-2": "DISAGREE", "OC-3": "DISAGREE",
            "OC-4": "DISAGREE", "OC-5": "DISAGREE"})
        for r in self.res["rows"]:
            self.assertEqual(r["got"][0], "REFUSE", r["id"])

    def test_nothing_counts_and_state_is_self_graded(self):
        self.assertEqual((self.res["counted"], self.res["counted_agree"]), (0, 0))
        self.assertEqual(self.res["state"], "SELF-GRADED")

    def test_informational_columns(self):
        a = {k: r["as_absolute"][1] for k, r in self.by.items()}
        rl = {k: r["as_relative"][1] for k, r in self.by.items()}
        self.assertEqual(a, {"OC-1": "ENHANCED_SUBADDITIVE",
                             "OC-2": "BELOW_RESOLUTION",
                             "OC-3": "BELOW_RESOLUTION",
                             "OC-4": "ADDITIVE", "OC-5": "RESONANT"})
        self.assertEqual([k for k in a if a[k] != rl[k]], ["OC-1"])

    def test_case_author_errors_would_agree_with_a_declared_mode(self):
        # Record, not a lift: with either mode declared, OC-3..5 read what
        # their authors expected.
        for k in ("OC-3", "OC-4", "OC-5"):
            want = AUTHORED[k][0]["relation"]
            self.assertEqual(self.by[k]["as_absolute"], ("RELATION", want))
            self.assertEqual(self.by[k]["as_relative"], ("RELATION", want))

    def test_oc2_is_below_resolution_for_every_joint_in_either_mode(self):
        # One facilitating cue: S+ - M = 0, so step 0 fires before joint is read.
        for mode in (ix.absolute, ix.relative_to_M):
            for joint in (-100, -3, 0, 2, 4, 5, 100):
                self.assertEqual(ix.classify(joint, [5, -3], mode(F(1, 10)))
                                 ["relation"], ix.BELOW_RESOLUTION)


class Judge(unittest.TestCase):
    def test_a_refusal_is_not_a_NOT(self):
        e = {"kind": "NOT", "relation": "BELOW_RESOLUTION"}
        self.assertFalse(ro.judge(e, ("REFUSE", "x")))
        self.assertTrue(ro.judge(e, ("RELATION", "ADDITIVE")))

    def test_refuse_expectation(self):
        self.assertTrue(ro.judge({"kind": "REFUSE"}, ("REFUSE", "x")))
        self.assertFalse(ro.judge({"kind": "REFUSE"}, ("RELATION", "ADDITIVE")))

    def test_lift_needs_an_independent_case_and_all_of_them_agreeing(self):
        d = ro.load()
        base = d["cases"][0]
        ok = dict(base, id="X-1", status="INDEPENDENT")          # OC-1 shape: refuses
        bad = dict(base, id="X-2", status="INDEPENDENT",
                   expect={"kind": "EQUALS", "relation": "ADDITIVE"})
        self.assertEqual(ro.run(dict(d, cases=[ok]))["state"], "OUTSIDE-AGREED")
        self.assertEqual(ro.run(dict(d, cases=[ok, bad]))["state"], "SELF-GRADED")
        self.assertEqual(ro.run(dict(d, cases=[base]))["state"], "SELF-GRADED")

    def test_unknown_status_raises(self):
        d = ro.load()
        with self.assertRaises(ValueError):
            ro.run(dict(d, cases=[dict(d["cases"][0], status="MAYBE")]))


class Cli(unittest.TestCase):
    def test_exit_codes(self):
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_outside.py")],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("STATE: SELF-GRADED", p.stdout)
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_outside.py"),
                            "--selftest"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
