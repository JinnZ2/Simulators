"""The stdlib ports of forest runs 6, 7, 8 against the results recorded from the delivered code.

Targets are those of experiments/model_comparison/forest_fire_regime/PREREG_ORIGINALS.md.
No numpy is needed: fixtures/originals_expected.json was written once by export_originals.py.
"""
import hashlib, json, os, sys, unittest
from helpers import *

EXP = os.path.join(ROOT, "experiments", "model_comparison", "forest_fire_regime")
sys.path.insert(0, EXP)
import originals as O

H = float.fromhex
with open(os.path.join(EXP, "fixtures", "originals_expected.json")) as f:
    FX = json.load(f)
LEDGER = os.path.join(os.path.dirname(ROOT), "forest-model-ledger", "runs")


class Originals(unittest.TestCase):
    def test_fixture_names_its_libraries_and_sources(self):
        self.assertTrue(FX["numpy_version"] and FX["scipy_version"])
        for name, sha in FX["sources"].items():
            path = os.path.join(LEDGER, name)
            if os.path.exists(path):                      # the sibling folder may be absent in a promoted copy
                with open(path, "rb") as f:
                    self.assertEqual(hashlib.sha256(f.read()).hexdigest(), sha, name + " changed since the export")

    def test_run7_same_burns(self):
        for got, want in zip(O.run7(), FX["run_7"]):
            self.assertEqual(got["drought"], H(want["drought"]))
            self.assertLessEqual(abs(got["grid_mean"] - H(want["grid_mean"])), 1e-12)
            self.assertLessEqual(abs(got["grid_sd"] - H(want["grid_sd"])), 1e-12)
            self.assertLessEqual(abs(got["ode"] - H(want["ode"])), 1e-9)

    def test_run8_same_burns(self):
        for got, want in zip(O.run8(), FX["run_8"]):
            for c, d in zip(got["cells"], want["cells"]):
                self.assertLessEqual(abs(c["mean"] - H(d["mean"])), 1e-12)
                self.assertLessEqual(abs(c["sd"] - H(d["sd"])), 1e-12)
            self.assertLessEqual(abs(got["ode"] - H(want["ode"])), 1e-9)

    def test_run6_structure_fires_and_closure(self):
        st, e6 = O.run6_structure(), FX["run_6"]
        self.assertEqual([x for r in st[0] for x in r], [H(x) for x in e6["trait"]])
        self.assertEqual([x for r in st[1] for x in r], [H(x) for x in e6["aff"]])
        old = O.run6_old(st)
        self.assertEqual(["%.3f" % old[i] for i in (0, 1, 5, 10, -1)], ["%.3f" % H(e6["old_misclosure"][i]) for i in (0, 1, 5, 10, -1)])
        self.assertLess(old[-1], -20)                      # the old model leaks; the audit sees it
        for thr in (0.6, 1.2):
            c, e = O.run6_conserved(thr, struct=st), e6["conserved"][repr(thr)]
            self.assertEqual(c["fires"], e["fires"])
            self.assertLess(max(abs(x) for x in c["mis"]), 1e-8)
            s = O.run6_stats(c["B"])
            self.assertEqual("%.3f" % s["B_mean"], "%.3f" % H(e["B_mean"]))

    def test_a_wrong_seed_is_seen(self):
        rows = O.run8(seed=5, droughts=(0.6,), spots=(0.2,))
        want = [d for d in FX["run_8"] if d["drought"] == 0.6][0]["cells"][2]
        self.assertNotEqual(rows[0]["cells"][0]["mean"], H(want["mean"]))

    def test_np_sum_order(self):
        v = [0.1 * (i + 1) for i in range(12)]
        self.assertEqual(O.np_sum(v), ((v[0] + v[1]) + (v[2] + v[3])) + ((v[4] + v[5]) + (v[6] + v[7])) + v[8] + v[9] + v[10] + v[11])
        self.assertRaises(ValueError, O.np_sum, [0.0] * 129)


if __name__ == "__main__":
    unittest.main()
