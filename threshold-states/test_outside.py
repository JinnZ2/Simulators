# SPDX-License-Identifier: CC0-1.0
"""Pins the outside-case run: 3 AGREE, 2 DISAGREE, STATE SELF-GRADED.

These pins record the module as it stands (interaction.py @ 697023e). A
repair that makes OC-1 or OC-2 agree turns this file red on purpose: the
pin and its note are corrected in the same commit, and because the repair
was made after the cases were seen, those two cases no longer count as
independent for lifting the flag (fresh outside cases are needed).

Run: python3 threshold-states/test_outside.py
"""
import os
import subprocess
import sys
import unittest

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


class Intake(unittest.TestCase):
    def test_file_carries_the_authored_cases_unedited(self):
        d = ro.load()
        self.assertEqual(d["author"], "chat-side")
        self.assertTrue(d["authored_outside_module"])
        got = {c["id"]: (c["expect"], c["separate"], c["joint"], c["tol"])
               for c in d["cases"]}
        self.assertEqual(got, AUTHORED)

    def test_oc1_vector_matches_the_stated_references(self):
        c = ro.load()["cases"][0]
        self.assertEqual(ix.references(c["separate"]), (10, 9))


class Run(unittest.TestCase):
    def setUp(self):
        self.res = ro.run()
        self.by = {r["id"]: r for r in self.res["rows"]}

    def test_pinned_verdicts(self):
        self.assertEqual({k: r["verdict"] for k, r in self.by.items()}, {
            "OC-1": "DISAGREE", "OC-2": "DISAGREE",
            "OC-3": "AGREE", "OC-4": "AGREE", "OC-5": "AGREE"})
        self.assertEqual((self.res["agree"], self.res["n"]), (3, 5))
        self.assertEqual(self.res["state"], "SELF-GRADED")

    def test_pinned_outcomes(self):
        self.assertEqual(self.by["OC-1"]["got"],
                         ("RELATION", "ENHANCED_SUBADDITIVE"))
        self.assertEqual(self.by["OC-2"]["got"],
                         ("RELATION", "BELOW_RESOLUTION"))

    def test_units_readings_differ_on_oc1_only(self):
        # The informational column: tol absolute vs tol * M.
        differ = sorted(k for k, r in self.by.items() if not r["readings_agree"])
        self.assertEqual(differ, ["OC-1"])
        self.assertEqual(self.by["OC-1"]["relative_reading"],
                         ("RELATION", "BELOW_RESOLUTION"))

    def test_oc2_is_below_resolution_for_every_joint(self):
        # Before the cue-sign split: the negative cue made S - M negative.
        # After it: one facilitating cue, so S+ - M = 0. Step 0 fires before
        # joint is read either way.
        for joint in (-100, -3, 0, 2, 4, 5, 100):
            self.assertEqual(ix.classify(joint, [5, -3], 0.1)["relation"],
                             ix.BELOW_RESOLUTION)


    def test_second_build_gives_the_same_outcomes(self):
        # interaction_class.py (repo root, another session) implemented the
        # same precedence; on these five cases it matched this build (sample
        # @ bd7d055), so both disagreements belong to the spec, not to one
        # build. It is now a shim over interaction.py, so this check no
        # longer compares two builds; the identity check below says so.
        for k, r in self.by.items():
            self.assertEqual(r["second_build"][0], "RELATION", k)
            self.assertEqual(r["second_build"][1], r["got"][1], k)


    def test_second_build_is_now_the_canonical_module(self):
        root = os.path.dirname(HERE)
        sys.path.insert(0, root)
        try:
            import interaction_class as ic
        finally:
            sys.path.remove(root)
        self.assertIs(ic.classify, ix.classify)


class Judge(unittest.TestCase):
    def test_a_refusal_is_not_a_NOT(self):
        e = {"kind": "NOT", "relation": "BELOW_RESOLUTION"}
        self.assertFalse(ro.judge(e, ("REFUSE", "x")))
        self.assertTrue(ro.judge(e, ("RELATION", "ADDITIVE")))

    def test_refuse_expectation(self):
        self.assertTrue(ro.judge({"kind": "REFUSE"}, ("REFUSE", "x")))
        self.assertFalse(ro.judge({"kind": "REFUSE"}, ("RELATION", "ADDITIVE")))

    def test_all_agree_lifts_state(self):
        d = ro.load()
        d["cases"] = [c for c in d["cases"] if c["id"] not in ("OC-1", "OC-2")]
        self.assertEqual(ro.run(d)["state"], "OUTSIDE-AGREED")


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
