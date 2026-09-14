"""Tree-level invariants for tools/run_manifest.py.

The module's own --selftest grades the classifier against constructed fixtures.
This file grades it against the real tree, which is where the two defects found
during the build came from: a `sys.exit(2)` in an unrelated `else:` attributed
to the --selftest path, and `re.compile` tripping the no-exec check. Neither was
reachable from a fixture written by the same hand that wrote the classifier.

The current contract violation is PINNED. Repairing anchor-position/normalize.py
turns this red on purpose: a row that disappears cannot be told from a row
nobody re-ran, so the repair has to come with an update to KNOWN_RED.md.
"""

import ast
import io
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import run_manifest as rm  # noqa: E402

RECORDS = None
SOURCE = None


def setUpModule():
    global RECORDS, SOURCE
    RECORDS, SOURCE = rm.build()


class TestRecordShape(unittest.TestCase):

    def test_every_record_carries_the_declared_fields(self):
        want = set(["path", "class", "invoke", "declared_exit",
                    "redirect_target", "target_resolves", "contract_ok",
                    "reason"])
        for r in RECORDS:
            self.assertEqual(set(r.keys()), want, r["path"])

    def test_every_class_is_declared(self):
        for r in RECORDS:
            self.assertIn(r["class"], rm.CLASSES, r["path"])

    def test_nothing_is_silently_unclassified(self):
        # UNCLASSIFIED is a state, not a bucket. It may be empty -- a visible
        # zero -- but anything in it must say why it matched no shape.
        for r in RECORDS:
            if r["class"] == "UNCLASSIFIED":
                self.assertTrue(r["reason"].strip(), r["path"])

    def test_unparseable_carries_its_reason_and_is_not_a_verdict(self):
        unp = [r for r in RECORDS if r["class"] == "UNPARSEABLE"]
        for r in unp:
            self.assertTrue(r["reason"].strip(), r["path"])
            self.assertIsNone(r["contract_ok"], r["path"])

    def test_absent_is_not_zero(self):
        for r in RECORDS:
            if r["class"] in ("LIBRARY", "CLI", "TEST_FILE"):
                self.assertIsNone(r["contract_ok"], r["path"])


class TestRedirectContract(unittest.TestCase):

    def test_redirects_exist_and_are_the_large_class(self):
        red = [r for r in RECORDS if r["class"] == "REDIRECT"]
        self.assertGreater(len(red), 50)

    def test_compliant_redirects_declare_exit_two(self):
        for r in RECORDS:
            if r["class"] == "REDIRECT" and r["contract_ok"]:
                self.assertEqual(r["declared_exit"], rm.REDIRECT_EXIT, r["path"])

    def test_no_redirect_names_a_target_that_is_missing(self):
        # D-4's shape at the redirect layer: the pointer outliving the artifact.
        missing = [r["path"] for r in RECORDS
                   if r["class"] == "REDIRECT" and r["target_resolves"] is False]
        self.assertEqual(missing, [], "redirect names a file that is not there")

    def test_the_one_known_violation_is_pinned(self):
        v = rm.violations(RECORDS)
        paths = sorted(r["path"] for r in v)
        self.assertEqual(
            paths, ["anchor-position/normalize.py"],
            "the contract-violation set moved. If this is a repair, say so in "
            "KNOWN_RED.md and update this pin; if it is a new violation, that "
            "is the finding.")


class TestRunsNothingItScans(unittest.TestCase):

    def _exec_hits(self, source):
        got = []
        for n in ast.walk(ast.parse(source)):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in (
                        "exec", "eval", "compile", "__import__"):
                    got.append(n.func.id)
                if getattr(n.func, "attr", None) == "import_module":
                    got.append("import_module")
        return got

    def _subprocess_argv0(self, source):
        out = []
        for n in ast.walk(ast.parse(source)):
            if isinstance(n, ast.Call):
                nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
                if nm in ("run", "Popen", "call", "check_output") and n.args:
                    a = n.args[0]
                    if isinstance(a, ast.List) and a.elts:
                        f = a.elts[0]
                        if isinstance(f, ast.Constant):
                            out.append(f.value)
        return out

    def _own_source(self):
        return io.open(os.path.join(ROOT, "tools", "run_manifest.py"),
                       encoding="utf-8").read()

    def test_module_executes_no_scanned_code(self):
        self.assertEqual(self._exec_hits(self._own_source()), [])

    def test_the_only_subprocess_is_git(self):
        self.assertEqual(self._subprocess_argv0(self._own_source()), ["git"])

    def test_both_checks_fire_on_a_plant(self):
        # A check nobody has seen fire is not a check.
        self.assertEqual(self._exec_hits('exec("x = 1")'), ["exec"])
        self.assertEqual(
            self._exec_hits('import importlib\nimportlib.import_module("m")'),
            ["import_module"])
        self.assertEqual(
            self._subprocess_argv0('import subprocess\n'
                                   'subprocess.run(["python3", "x.py"])'),
            ["python3"])

    def test_the_exec_check_reads_the_receiver(self):
        # A first pass flagged re.compile. The receiver decides, not the name.
        self.assertEqual(self._exec_hits('import re\nre.compile("x")'), [])


class TestSelfReference(unittest.TestCase):

    def test_the_manifest_appears_in_its_own_manifest(self):
        # Recorded rather than excluded: a path skip breaks on the one case
        # that matters, a tree holding a copy of the tool.
        mine = [r for r in RECORDS if r["path"] == "tools/run_manifest.py"]
        self.assertEqual(len(mine), 1)
        self.assertEqual(mine[0]["class"], "SELFTEST")

    def test_enumeration_source_is_reported(self):
        self.assertIn(SOURCE, ("git ls-files", "os.walk (git unavailable)"))


class TestSelftestPasses(unittest.TestCase):

    def test_module_selftest_returns_zero(self):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = rm.selftest()
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("VERDICT: PASS", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
