# SPDX-License-Identifier: CC0-1.0
"""KNOWN_RED.md's stated figures against an actual run.

tools/known_red_check.py reads the PIN block in KNOWN_RED.md section 19.
It reruns tools/known_answer.py and tools/run_manifest.py and fails on any
pin that disagrees. This test puts that comparison in the suite, so a
figure that drifts turns the suite red. It does not sit in prose until
somebody notices (section 16 sat at "33 in 6" for two merges after it
became 28 in 5).

The suite.failing pins are NOT checked here. Checking them means running
the suite, and this file is part of the suite. They read NOT_CHECKED here,
which is a state, not a pass. `python3 tools/known_red_check.py --suite`
checks them from outside.
"""

import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(ROOT, "tools", "known_red_check.py")


class KnownRedPins(unittest.TestCase):

    def test_checker_selftest_passes(self):
        p = subprocess.run([sys.executable, TOOL, "--selftest"], cwd=ROOT,
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_stated_counts_match_the_run(self):
        p = subprocess.run([sys.executable, TOOL], cwd=ROOT,
                           capture_output=True, text=True)
        out = p.stdout + p.stderr
        self.assertEqual(p.returncode, 0, out)
        self.assertIn("VERDICT: PASS", out)

    def test_the_block_is_not_empty(self):
        # An empty PIN block compares nothing and would pass. Require the
        # two scalar figures section 16 got wrong to be pinned.
        with open(os.path.join(ROOT, "KNOWN_RED.md"), encoding="utf-8") as f:
            text = f.read()
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        try:
            import known_red_check as k
        finally:
            sys.path.pop(0)
        kinds = {p["kind"] for p in k.parse(text)}
        self.assertTrue({"ka.skipped.cases", "ka.skipped.metrics",
                         "rm.violation", "suite.failing"} <= kinds, kinds)


if __name__ == "__main__":
    unittest.main()
