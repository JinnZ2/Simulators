"""
Repo-level test: there is exactly one gate, and it is the current one.

License: CC0
Dependencies: stdlib only (unittest)

Five pre-repair copies of reasoning-gate files arrived across three drops.
Each ran, produced plausible output, and silently lacked the guard behaviour
the canonical version has. Nothing in the repo noticed until they were
diffed by hand.

This test is the thing that notices. It lives at repo root rather than in
reasoning-gate/tests/ because the property it asserts is about the repo, and
reasoning-gate/ is meant to stay promotable to its own repo.

    python3 -m unittest discover tests
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "check_gate_drift.py")

sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_gate_drift as drift  # noqa: E402


class GateIsSingular(unittest.TestCase):

    def test_the_tool_exists(self):
        self.assertTrue(os.path.exists(TOOL))

    def test_no_copies_of_the_gate_family(self):
        """
        Every gate-family file lives in reasoning-gate/ and nowhere else.
        A copy is reported whether it has drifted yet or not -- the only
        reason a copy is ever stale is that it started identical.
        """
        copies = drift.scan(ROOT)
        self.assertEqual(
            copies, [],
            "gate-family copies found outside %s/: %s. Import the gate "
            "instead; see tools/check_gate_drift.py."
            % (drift.CANONICAL_DIR,
               ", ".join("%s (copy of %s, %s)"
                         % (r, n, "identical" if i else "DRIFTED")
                         for r, n, i in copies)))

    def test_guards_md_is_in_sync(self):
        """GUARDS.md is generated. It must be what make_docs.py renders."""
        self.assertTrue(
            drift.docs_in_sync(ROOT),
            "GUARDS.md is not what make_docs.py renders from guards.json. "
            "Run: cd reasoning-gate && python3 make_docs.py")

    def test_tool_exits_zero_on_a_clean_repo(self):
        result = subprocess.run([sys.executable, TOOL, ROOT],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_tool_exits_nonzero_when_a_stale_copy_is_planted(self):
        """
        The check must be able to fail. A drift detector that cannot report
        drift is null-harness's CONSTANT_SILENT.
        """
        import shutil
        import tempfile

        tmp = tempfile.mkdtemp()
        try:
            shutil.copytree(os.path.join(ROOT, drift.CANONICAL_DIR),
                            os.path.join(tmp, drift.CANONICAL_DIR))
            shutil.copytree(os.path.join(ROOT, "tools"),
                            os.path.join(tmp, "tools"))
            planted = os.path.join(tmp, "somewhere", "gate.py")
            os.makedirs(os.path.dirname(planted))
            with open(os.path.join(ROOT, drift.CANONICAL_DIR, "gate.py")) as fh:
                text = fh.read()
            with open(planted, "w") as fh:
                fh.write(text.replace("class GateError(Exception):",
                                      "class GateError(Exception):  # stale"))

            self.assertEqual(len(drift.scan(tmp)), 1)
            self.assertFalse(drift.scan(tmp)[0][2])   # not identical

            result = subprocess.run([sys.executable, TOOL, tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("DRIFT", result.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_checker_does_not_flag_itself(self):
        """
        It has to quote the markers it searches for. Identifying itself by
        content rather than by path is what lets it scan a tree containing
        a copy of itself -- which is the case it exists for.
        """
        with open(TOOL) as fh:
            self.assertTrue(drift._defines_markers(fh.read()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
