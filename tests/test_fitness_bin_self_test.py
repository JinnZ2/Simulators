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
        self.assertIn("VERDICT: PASS   checks=75 failed=0", output.getvalue())

    def test_sample_is_complete_default_output(self):
        p = subprocess.run([sys.executable, str(TOOL)], capture_output=True,
                           text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 0, p.stderr)
        sample = (ROOT / "tools" / "samples" /
                  "fitness_bin_self_test_wo8.sample.txt").read_text()
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


class T5PlusLedger(unittest.TestCase):
    def test_selection_entropy_can_increase(self):
        # Selection is not a theorem of monotone marginal entropy loss.
        before, retained = ["N", "N", "N", "E"], ["N", "E"]
        self.assertLess(fb.allele_entropy(before), fb.allele_entropy(retained))
        self.assertEqual(fb.lost_support(before, retained), [])

    def test_entropy_drop_is_not_last_copy_erasure(self):
        before, retained = ["N", "N", "E", "E"], ["N", "N", "E"]
        self.assertGreater(fb.allele_entropy(before), fb.allele_entropy(retained))
        self.assertEqual(fb.lost_support(before, retained), [])
        self.assertEqual(fb.lost_support(before, ["N", "N"]),
                         [{"locus": 0, "allele": "E", "copies_before": 2}])

    def test_marginal_entropy_misses_lost_linkage(self):
        before, retained = ["NN", "EE", "NE", "EN"], ["NN", "EE"]
        self.assertEqual(fb.allele_entropy(before), 2.0)
        self.assertEqual(fb.allele_entropy(retained), 2.0)
        self.assertEqual(fb.lost_support(before, retained), [])
        self.assertEqual(set(before) - set(retained), {"NE", "EN"})

    def test_actual_mutation_rule_wait_and_cost_units(self):
        self.assertAlmostEqual(fb.rediscovery_wait(2, 1, 2), 4 / 3)
        self.assertEqual(fb.rediscovery_wait(1, 1, 2), 2.0)
        self.assertEqual(fb.archive_ratio(2, 4, 3), "UNRATED")
        self.assertEqual(fb.archive_ratio(2, 4, 3, "work_units"), 1.5)
        self.assertEqual(fb.archive_ratio(2, 4, 0, "work_units"), 0.0)

    def test_t5plus_does_not_rewrite_original_winners_or_archives(self):
        original = (ROOT / "tools" / "samples" /
                    "fitness_bin_self_test.sample.txt").read_text()
        extended = fb.render(fb.experiment(seed=7, size=9, length=24,
                                          population=40, generations=60,
                                          retained=8, top=5))
        for line in original.splitlines():
            if line.startswith(("winner ", "  T2 ", "T5 archived", "RUN_A:", "CONTROL_B:")):
                self.assertIn(line, extended)


class BehaviorLedger(unittest.TestCase):
    def test_handbuilt_population(self):
        result = fb.behavior_metrics([(0, 0), (0, 0), (1, 1), (1, 1)])
        self.assertEqual(result, {"distinct": 2, "entropy_bits": 1.0, "largest_share": 0.5})
        self.assertIsNone(fb.behavior_metrics([])["entropy_bits"])

    def test_last_copy_loss_and_rediscovery_are_windowed(self):
        result = fb.behavior_ledger([["a", "b"], ["a"], ["b"]], 8)
        self.assertEqual((result["loss_events"], result["rediscovered"], result["lost_within_window"]), (2, 1, 1))
        states = {event["descriptor_value"]: event["state"] for event in result["losses"]}
        self.assertEqual(states, {"a": "LOST_WITHIN_WINDOW", "b": "REDISCOVERED"})
        self.assertEqual(result["rows"][2]["rediscovered_loss_events"], 1)

    def test_half_threshold_strict_and_early_fixed(self):
        self.assertIsNone(fb.behavior_half_gen([4, 2, 2]))
        self.assertEqual(fb.behavior_half_gen([4, 2, 1]), 2)
        result = fb.behavior_ledger([["a", "b", "c", "d"], ["a", "b"], ["a"]], 8)
        self.assertTrue(result["early_collapse"])
        self.assertEqual(result["early_cutoff"], 2)

    def test_separation_verdict_controls(self):
        self.assertEqual(fb.separation_verdict([True, True], [False, False]), "POSITIVE")
        self.assertEqual(fb.separation_verdict([False, False], [False, False]), "NEGATIVE")
        self.assertEqual(fb.separation_verdict([True, False], [False, False]), "INCONCLUSIVE")
        self.assertEqual(fb.separation_verdict([], []), "INCONCLUSIVE")


class SelectorReading(unittest.TestCase):
    def test_predeclared_P2_interpretations_are_not_interchanged(self):
        def run(f, v, p):
            return {"half": {"0.5": {"F": f, "V": v, "P": p}}}
        paired = {"OBJ-F": run(2, None, 2), "NOV-F": run(None, None, None),
                  "OBJ-V": run(None, None, 2), "NOV-V": run(None, None, None)}
        self.assertEqual(fb.wo9_seed_reading(paired, allow_path_scalar=True)["verdict"], "SUPPORTED")
        self.assertEqual(fb.wo9_seed_reading(paired, allow_path_scalar=False)["verdict"], "FALSIFIED")

    def test_seed_or_sensitivity_variation_is_inconclusive(self):
        self.assertEqual(fb.aggregate_wo9({"0.4": [{"verdict": "SUPPORTED"}],
                                          "0.5": [{"verdict": "FALSIFIED"}]}), "INCONCLUSIVE")
        self.assertEqual(fb.aggregate_wo9({"0.5": [{"verdict": "SUPPORTED"},
                                                   {"verdict": "SUPPORTED"}]}), "SUPPORTED")


if __name__ == "__main__":
    unittest.main()
