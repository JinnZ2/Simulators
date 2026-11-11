import hashlib, json, os, unittest
from helpers import *
from playground.experiments import runner
from playground import known_answer_gate as gate

gate.certify_all()
EXP = os.path.join(ROOT, "experiments", "model_comparison", "forest_fire_regime")
sys.path.insert(0, EXP)
FIXTURE_SHA = "85fd1f785561d19c5a19eb200e0fc030874462c8d005aa98812492b91a203e28"


class T(unittest.TestCase):
    def test_same_seed_same_result(self):
        mk = lambda seed: config("mean_reverting", dict(theta=1.0, mu=2.0, sigma=0.3), dict(x=0.0), live=dict(mass=["x"]), seed=seed)
        f = lambda seed: runner.run(mk(seed))["observations_and_predictions"]["final_state"]["x"]
        self.assertEqual(f(3), f(3))
        self.assertNotEqual(f(3), f(4))

    def test_seed_must_be_explicit(self):
        self.assertRaises(ValueError, Environment, None)

    def test_grid_run_reproducible(self):
        import run as exp
        a, b = exp.grid_run(0.6, 0.0, 7), exp.grid_run(0.6, 0.0, 7)
        self.assertEqual(a, b)
        self.assertEqual((a["status"], a["verdict"]), ("COMPLETE", "CLOSED"))

    def test_fixture_unchanged(self):
        with open(os.path.join(EXP, "fixtures", "numpy_draws_seed0.json"), "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), FIXTURE_SHA)

    def test_port_defaults_match_the_forest_ledger_source(self):
        """The transcribed DEFAULTS and INIT against forest-model-ledger/model/base.py, read as text (no numpy)."""
        import ast, models
        src = os.path.join(ROOT, "..", "forest-model-ledger", "model", "base.py")
        if not os.path.exists(src):
            self.skipTest("forest-model-ledger not in this checkout")
        tree = ast.parse(open(src).read())
        got = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and node.targets[0].id in ("DEFAULTS", "INIT"):
                got[node.targets[0].id] = {k.arg: ast.literal_eval(k.value) for k in node.value.keywords}
        self.assertEqual(got["INIT"], models.INIT)
        self.assertEqual(got["DEFAULTS"], {k: v for k, v in models.DEFAULTS.items() if k != "fires"})

    def test_port_reproduces_run_9(self):
        import run as exp, models
        models.certify()
        rec = runner.run(exp.forest_config("replay_base", "REPLAY", 0))
        b = {r["budget"]: r for r in rec["l0_budgets"]}
        self.assertEqual(rec["status"], "COMPLETE")
        self.assertEqual(len(rec["events"]), 80)
        self.assertEqual(b["N"]["verdict"], "CLOSED")
        self.assertLess(abs(b["N"]["misclosure"]), 1e-9)
        for k, v in exp.RUN9["pools"].items():
            self.assertAlmostEqual(rec["observations_and_predictions"]["final_state"][k], v, places=4)

    def test_results_file_matches_its_json(self):
        with open(os.path.join(EXP, "out", "part2.json")) as f:
            p2 = json.load(f)
        text = open(os.path.join(EXP, "RESULTS.txt")).read()
        for feat in p2["features"]:
            self.assertIn("%s %-16s" % (feat["id"], feat["reading"]), text)
        self.assertEqual(len(p2["table"]["spot_0.00"]), 11)       # no level dropped


if __name__ == "__main__":
    unittest.main()
