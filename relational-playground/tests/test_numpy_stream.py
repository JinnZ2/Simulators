"""playground/numpy_stream.py against numpy's own recorded output (no numpy needed)."""
import json, os, unittest
from helpers import *
from playground import numpy_stream as ns

FX = os.path.join(ROOT, "experiments", "model_comparison", "forest_fire_regime", "fixtures", "numpy_stream_check.json")


class NumpyStream(unittest.TestCase):
    def test_matches_recorded_numpy_output(self):
        with open(FX) as f:
            fx = json.load(f)
        self.assertTrue(fx["numpy_version"])
        n = 0
        for seed, rec in fx["seeds"].items():
            g = ns.default_rng(int(seed))
            for i, want in enumerate(rec["calls"]):
                k = i % 7
                got = g.random().hex() if k in (0, 1, 3, 6) else g.integers({2: 100, 4: 120, 5: 3}[k])
                self.assertEqual(got, want, "seed %s call %d" % (seed, i))
                n += 1
            for want in rec["block"]:
                self.assertEqual(g.random().hex(), want)
                n += 1
        self.assertEqual(n, 6 * 735)

    def test_a_wrong_stream_is_seen(self):
        with open(FX) as f:
            fx = json.load(f)
        g = ns.default_rng(1)                      # seed 1 is not in the fixture
        self.assertNotEqual(g.random().hex(), fx["seeds"]["0"]["calls"][0])

    def test_refusals(self):
        g = ns.default_rng(0)
        self.assertRaises(ValueError, g.integers, 0)
        self.assertRaises(ValueError, ns.default_rng, -1)
        self.assertFalse(hasattr(g, "normal"))


if __name__ == "__main__":
    unittest.main()
