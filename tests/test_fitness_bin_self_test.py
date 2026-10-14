# SPDX-License-Identifier: CC0-1.0
"""WO-7 synthetic regression checks. Not external validation."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "fitness_bin_self_test.py"
SPEC = importlib.util.spec_from_file_location("fitness_bin_self_test", TOOL)
fb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fb)


class FitnessBinSelfTest(unittest.TestCase):
    def test_module_selftest(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = fb.selftest()
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn("VERDICT: PASS   checks=43 failed=0", output.getvalue())

    def test_sample_is_complete_default_output(self):
        p = subprocess.run([sys.executable, str(TOOL)], capture_output=True,
                           text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 0, p.stderr)
        sample = (ROOT / "tools" / "samples" /
                  "fitness_bin_self_test.sample.txt").read_text()
        self.assertEqual(p.stdout, sample)
        for test in ("T1", "T2", "T3", "T4", "T5", "T6"):
            self.assertIn(test, sample)

    def test_same_initial_population_in_both_worlds(self):
        # No selections: scores may rank differently; genotype multiset must not.
        a = fb.evolve(fb.LEAKY, generations=0, top=40)
        b = fb.evolve(fb.SEALED, generations=0, top=40)
        self.assertEqual(sorted(w["genome"] for w in a["winners"]),
                         sorted(w["genome"] for w in b["winners"]))

    def test_archive_preserves_each_selection_discard(self):
        r = fb.evolve(fb.LEAKY, population=12, retained=3, generations=4)
        self.assertEqual(len(r["archive"]), 36)
        for generation in range(4):
            self.assertEqual(sum(row["generation"] == generation
                                 for row in r["archive"]), 9)
        # Scores recorded in native substrate, not scored after a patch.
        for row in r["archive"]:
            self.assertEqual(row["score"], fb.replay(row["genome"], fb.LEAKY)["score"])

    def test_archive_export_is_full_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "discard.json"
            p = subprocess.run([sys.executable, str(TOOL), "--generations", "2",
                                "--archive", str(path)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            data = json.loads(path.read_text())
            self.assertEqual(len(data["A"]), 64)
            self.assertEqual(len(data["B"]), 64)
            self.assertEqual(data["budget"]["seed"], 7)

    def test_known_wrap_loses_when_topology_changes(self):
        a = fb.replay("WS", fb.LEAKY)
        b = fb.replay("WS", fb.SEALED)
        self.assertEqual(a["score"], 0)
        self.assertEqual(b["score"], -16)
        self.assertEqual(fb.fitness_drop(a["score"], b["score"]), 16)
        self.assertEqual(fb.readout(a, 1, b)["fact_kind"], "INSTRUMENT")

    def test_invalid_budget_is_skip_not_a_failed_measurement(self):
        p = subprocess.run([sys.executable, str(TOOL), "--retained", "40"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 3)
        self.assertIn("VERDICT: SKIP", p.stderr)
        self.assertNotIn("RUN_A:", p.stdout)

    def test_control_fault_is_not_a_positive_finding(self):
        a = fb.replay("WS", fb.LEAKY)
        changed = fb.replay("WS", fb.SEALED)
        self.assertEqual(fb.classify([a], [a], [changed]), "TOOL_FAULT")


if __name__ == "__main__":
    unittest.main()
