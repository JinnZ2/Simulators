"""tools/provenance_marker.py in the repo suite: the selftest (refusals,
inheritance, STALE/MISSING, chain tamper, a tool editing itself mid-run),
and three properties of the committed ledger -- the chain is unbroken,
every marker carries all five passes, and on the latest marker of each
CURRENT tool every RUNS/PARTIAL basis resolves to a non-blank line. Currency (CURRENT vs STALE) is NOT asserted:
a stale marker is the instrument reporting that a tool changed since it was
last run, which is information, not a failure of the suite."""
import importlib.util
import io
import json
import os
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "tools", "provenance_marker.py")


def _load():
    spec = importlib.util.spec_from_file_location("provenance_marker", PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ProvenanceMarkerTest(unittest.TestCase):
    def setUp(self):
        self.m = _load()

    def test_selftest(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.m.selftest()
        self.assertEqual(rc, 0, buf.getvalue())

    def test_ledger_chain_intact(self):
        self.assertEqual(self.m.verify(self.m.LEDGER), [])

    def test_ledger_bases_resolve_and_passes_complete(self):
        # Every marker carries all five passes. Basis lines are checked only
        # on the LATEST marker per tool, and only while that tool is CURRENT:
        # a superseded marker, or one whose tool has since been edited (STALE,
        # reported by `check`), points at lines of a file that no longer
        # exists in that form, so its basis is not expected to resolve.
        rows = self.m.read_ledger(self.m.LEDGER)
        self.assertTrue(rows, "committed ledger is empty")
        for line in rows:
            r = json.loads(line)
            self.assertEqual(sorted(r["passes"]), list(self.m.PASS_IDS))
            for p in r["passes"].values():
                self.assertIn(p["state"], self.m.STATES)
        res = self.m.check(self.m.LEDGER, ROOT)
        self.assertTrue(any(s == "CURRENT" for s, _ in res.values()),
                        "no CURRENT marker: the basis check would run on none")
        for rel, (status, r) in res.items():
            if status != "CURRENT":
                continue
            for pid, p in r["passes"].items():
                if p["state"] in ("RUNS", "PARTIAL"):
                    ok, why = self.m.basis_resolves(p["basis"], ROOT)
                    self.assertTrue(ok, "%s %s: %s" % (r["path"], pid, why))
                if p["state"] == "PARTIAL":
                    self.assertTrue(p["note"], "%s %s PARTIAL w/o note"
                                    % (r["path"], pid))


if __name__ == "__main__":
    unittest.main()
