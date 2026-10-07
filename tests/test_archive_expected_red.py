"""
Repo-level test: every archived build's suite is in the state DECLARED here.

License: CC0
Dependencies: stdlib only (unittest, subprocess)

archive/<folder>/ holds the build of <folder> that the 2026-09-30 restore
commits did not pick (KNOWN_RED section 13.3, section 14). Each archived
build's own suite is run from inside its archive folder and its outcome is
compared to a DECLARED state. A change in EITHER direction is a FAIL: an
archived suite that was red turning green, or one that was green turning
red, is something changing that nobody declared.

The order that created this test expected every archived suite to be red.
Three of five are green, because the losing build moved whole and its suite
needs nothing the live folder kept. That is recorded as the declared state,
not smoothed into an expectation: a GREEN row here is a build that still
runs from its archive, and the test holds it there.

    python3 -m unittest discover tests
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(ROOT, "archive")
TIMEOUT = 300

# folder -> (suite file or None, expected, signature that must appear in
# the output). Expected is "RED" (nonzero exit) or "GREEN" (exit 0).
# NO_SUITE: the archived build shipped no test file; only its presence
# and PROVENANCE.md are checked.
DECLARED = {
    "assessor-coupling": ("selftest.py", "RED",
                          "FileNotFoundError"),          # reads WORK_ORDER.md from HERE; it stayed live
    "crediting-rate": ("test_crediting_v2.py", "RED",
                       "No module named 'crediting_rate'"),  # imports the shared v1 module, kept live
    "cooperative-substrate-proof": ("selftest.py", "GREEN", "checks: 82   failed: 0"),
    "instrument-index": (None, "NO_SUITE", ""),
    "chain-position": ("selftest.py", "GREEN", "checks: 96   failed: 0"),
    "stability-trigger-envelope": ("test_envelope.py", "GREEN", "217 checks, 0 failed"),
    "interaction_class": ("test_interaction_class.py", "GREEN", "33/33"),  # root build, pre-split rule
}


def run_suite(folder, suite):
    cwd = os.path.join(ARCHIVE, folder)
    r = subprocess.run([sys.executable, suite], cwd=cwd, capture_output=True,
                       text=True, timeout=TIMEOUT)
    return r.returncode, (r.stdout + r.stderr)


class ArchivedBuildsStayWhereDeclared(unittest.TestCase):

    def test_every_archive_folder_is_declared_and_has_provenance(self):
        present = sorted(d for d in os.listdir(ARCHIVE)
                         if os.path.isdir(os.path.join(ARCHIVE, d)))
        self.assertEqual(present, sorted(DECLARED),
                         "archive/ and DECLARED disagree; a folder was archived "
                         "or removed without this table moving")
        for d in present:
            self.assertTrue(os.path.exists(os.path.join(ARCHIVE, d, "PROVENANCE.md")),
                            "archive/%s has no PROVENANCE.md" % d)

    def test_each_archived_suite_is_in_its_declared_state(self):
        failures = []
        for folder, (suite, expected, signature) in sorted(DECLARED.items()):
            if suite is None:
                self.assertEqual(expected, "NO_SUITE")
                continue
            path = os.path.join(ARCHIVE, folder, suite)
            self.assertTrue(os.path.exists(path), path)
            rc, out = run_suite(folder, suite)
            got = "GREEN" if rc == 0 else "RED"
            tail = out.strip().splitlines()[-1] if out.strip() else ""
            if got != expected:
                failures.append("archive/%s/%s declared %s, ran %s (exit %d): %s"
                                % (folder, suite, expected, got, rc, tail[:120]))
            elif signature and signature not in out:
                failures.append("archive/%s/%s is %s as declared but not for the declared "
                                "reason; wanted %r, last line %r"
                                % (folder, suite, got, signature, tail[:120]))
        self.assertEqual(failures, [], "\n".join(failures))

    def test_the_check_can_fail(self):
        """A declared RED that comes back GREEN is a failure, not a pass."""
        rc, out = run_suite("chain-position", "selftest.py")
        self.assertEqual(rc, 0)
        got = "GREEN" if rc == 0 else "RED"
        self.assertNotEqual(got, "RED")


if __name__ == "__main__":
    unittest.main()
