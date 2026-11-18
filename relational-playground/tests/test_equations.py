import unittest
from helpers import *
from playground.experiments import runner, comparison, sensitivity, parameter_sweep
from playground.equations.base import ModelOutput, from_transfers, register as register_model, REGISTRY
from playground.analysis import identifiability, coincidence, applicability, transitions, model_limits
from playground.reporting import claims, results
from playground import known_answer_gate as gate, l0, anchor

TRUST = gate.certify_all()


def _leaky(state, env, rel, ctl, p):
    tr = [("in", None, "x", 1.0), ("out", "x", None, 0.5 * state["x"])]
    d = from_transfers(tr, ["x"])
    d["x"] -= p["leak"] * state["x"]
    return ModelOutput(d, transfers=tr)


if "leaky_fixture" not in REGISTRY:
    register_model("leaky_fixture", "nonlinear", "t", _leaky, "rate", requires=("leak",))
ALLEE = lambda **kw: config("allee", dict(r=1.0, a=1.0, K=10.0, h=0.1), dict(x=2.0), live=dict(mass=["x"]), t_end=6.0, **kw)


class Substitution(unittest.TestCase):
    def test_every_family_passes_the_gate(self):
        for name in ("linear", "allee", "network", "energy_store", "permeable", "mean_reverting", "percolation", "branching"):
            self.assertTrue(TRUST[name]["trusted"], (name, TRUST[name]))
            self.assertEqual((TRUST[name]["FP"], TRUST[name]["TP"]), (0.0, 1.0))

    def test_same_runner_two_equations(self):
        a = runner.run(ALLEE())
        b = runner.run(config("permeable", dict(perm0=1.0, perm_drift=0.0, outside=6.0, loss=0.2), dict(x=2.0), live=dict(mass=["x"]), t_end=6.0))
        self.assertEqual(sorted(a) , sorted(b))
        results.check(a)

    def test_missing_parameter_is_not_defaulted(self):
        self.assertRaises(KeyError, runner.run, config("allee", dict(r=1.0, a=1.0, K=10.0), dict(x=2.0), live=dict(mass=["x"])))

    def test_untrusted_model_run_is_incomplete(self):
        r = runner.run(config("leaky_fixture", dict(leak=0.0), dict(x=1.0), live=dict(mass=["x"])))
        self.assertEqual(r["l0_budgets"][0]["verdict"], "CLOSED")
        self.assertEqual(r["status"], "INCOMPLETE")
        self.assertIn("UNTRUSTED", r["model_trust"])


class L0(unittest.TestCase):
    def test_planted_leak_is_incomplete_whatever_the_fit(self):
        r = runner.run(config("leaky_fixture", dict(leak=0.01), dict(x=1.0), live=dict(mass=["x"])))
        self.assertEqual(r["l0_budgets"][0]["verdict"], "LEAK")
        self.assertIn("did not close", r["status_reason"])

    def test_no_live_budget_is_incomplete(self):
        r = runner.run(config("allee", dict(r=1.0, a=1.0, K=10.0, h=0.1), dict(x=2.0)))
        self.assertEqual(r["status"], "INCOMPLETE")
        self.assertTrue(all(b["verdict"] == "VOID" and b["reason"] for b in r["l0_budgets"]))

    def test_five_budgets_always_listed_and_energy_outside_the_energy_family(self):
        r = runner.run(ALLEE())
        self.assertEqual([b["budget"] for b in r["l0_budgets"]], list(l0.BUDGETS))
        self.assertRaises(ValueError, l0.declare, mass=l0.Budget("mass", pools=["x"]))
        self.assertRaises(ValueError, l0.Budget, "energy")

    def test_boundary_audit_line(self):
        self.assertTrue(runner.run(ALLEE())["boundary_audit"][0].startswith("boundary audit [mass]: in growth"))

    def test_noise_rule(self):
        self.assertEqual(l0.verdict(1e-3, 1.0, sigma_meas=1e-2), "NOISE")
        self.assertEqual(l0.verdict(1e-3, 1.0), "LEAK")
        self.assertEqual(l0.verdict(1e-12, 1.0), "CLOSED")


class Anchor(unittest.TestCase):
    def test_loop(self):
        c = ALLEE()
        a = anchor.freeze("A1", c, [], "fixture")
        self.assertEqual(anchor.verify(a, c, []), [])
        self.assertRaises(anchor.AnchorError, anchor.branch, c, "B", parameter="h", value=0.2, dt=0.02)
        self.assertRaises(anchor.AnchorError, anchor.branch, c, "B")
        b, change = anchor.branch(c, "B1", parameter="h", value=0.2)
        d = anchor.return_diff(a, runner.run(b), change)
        self.assertLess(d["rows"][0]["delta"], 0)
        self.assertNotIn("better", str(d))
        self.assertEqual(anchor.verify(a, b, []), ["configuration hash moved", "final state not bit-identical"])
        a2 = anchor.run_tests(a, c, [], [0, 1], ["r", "a", "K", "h"])
        self.assertEqual(a2["status"], "candidate")      # sigma_meas void and four budgets VOID: PARTIAL, not PASS
        self.assertEqual(a2["tests"]["independent_budgets_close_together"]["state"], "PARTIAL")


class Tools(unittest.TestCase):
    def test_tools_pass_the_gate(self):
        self.assertTrue(TRUST["tool:transitions.read"]["trusted"])
        self.assertTrue(TRUST["tool:model_limits.failure_region"]["trusted"])
        gate.require_tool("transitions.read")
        self.assertRaises(RuntimeError, gate.require_tool, "no_such_tool")

    def test_ramp_has_no_transition(self):
        xs = [0, 1, 2, 3]
        self.assertEqual(transitions.read(xs, [0, 2, 4, 6])["steepest_between"], "NONE")

    def test_identifiability(self):
        c = config("energy_store", dict(P_in=1.0, demand=0.5, k_diss=0.1), dict(E=1.0), live=dict(energy=["E"]), t_end=5.0)
        rows = {r["pair"]: r["reading"] for r in identifiability.pairs(c, "E", ["P_in", "demand", "k_diss"])["rows"]}
        self.assertEqual(rows[("P_in", "demand")], "NOT SEPARABLE by this output")
        self.assertEqual(rows[("P_in", "k_diss")], "SEPARABLE")

    def test_failed_points_stay_in_the_sweep(self):
        s = parameter_sweep.sweep(ALLEE(), {"a": [1.0, 0.0]}, "x")
        self.assertEqual([r["status"] for r in s["rows"]], ["MODEL FAILED", "COMPLETE"][::-1] if s["rows"][0]["point"]["a"] == 1.0 else ["MODEL FAILED", "COMPLETE"])
        self.assertEqual(model_limits.failure_region([dict(point=1, status="MODEL FAILED")])["counts"]["MODEL FAILED"], 1)

    def test_applicability_has_no_score(self):
        self.assertRaises(RuntimeError, applicability.score)
        r = applicability.record("allee", "fixture", stability=dict(finding="recovers", basis="test"))
        self.assertEqual(len(r["not_assessed"]), 9)
        self.assertRaises(ValueError, applicability.record, "allee", "fixture", stability="good")

    def test_claim_tags(self):
        self.assertRaises(ValueError, claims.claim, "x", "MEASURED", "b")
        self.assertRaises(ValueError, claims.claim, "x", "DERIVED", "")
        r = runner.run(ALLEE())
        self.assertEqual(claims.counts(r["claims"])["DERIVED"], 2)

    def test_coincidence_card(self):
        rows = [dict(model="a", family="energy", output=5.0), dict(model="b", family="boundary", output=5.0001),
                dict(model="c", family="boundary", output=5.0002), dict(model="d", family="nonlinear", output=9.0)]
        self.assertEqual(coincidence.on_agreement(rows, None, None)["state"], "NOT CHECKED")
        r = coincidence.on_agreement(rows, 1e-2, "fixture, before the run")
        self.assertEqual(len(r["cards"]), 2)                       # a-b and a-c; b-c is one family
        self.assertTrue(all(x == "OPEN" for _, x in r["readings"]))
        card = r["cards"][0]
        self.assertEqual(card["c_tests"]["C5"], "NOT RUN")
        self.assertRaises(ValueError, coincidence.run_c5, card, "a", "b", 0.9, 0.2, 0.1, "")
        self.assertTrue(coincidence.run_c5(card, "a", "b", 0.9, 0.2, 0.1, "fixture")["explained_by_normal_form"])
        self.assertFalse(coincidence.run_c5(card, "a", "b", 0.9, 0.85, 0.1, "fixture")["explained_by_normal_form"])
        self.assertTrue(coincidence.run_c6(card, "m", 0.05, "fixture", by_config={"rk4": 1.0, "euler": 1.5})["numerical_artifact"])
        self.assertIsNone(coincidence.run_c6(card, "m", 0.05, "fixture")["numerical_artifact"])   # no variation supplied: undecidable, not False
        self.assertRaises(ValueError, coincidence.run_none_of_above, card, dict(c1=True))         # a missing verdict is never inferred
        self.assertEqual(coincidence.run_none_of_above(card, {k: True for k in ("c1", "c2", "c3", "c4", "c5", "c6")})["status"], "SUPPORTED_OPENS_BRANCH")
        self.assertRaises(ValueError, coincidence.set_slot, card, "none_of_above", "supported", "x")
        self.assertRaises(ValueError, coincidence.set_slot, card, "shared_constraint", "supported", "void")
        for s in coincidence.CAUSES:
            coincidence.set_slot(card, s, "ruled_out", "fixture")
        self.assertRaises(ValueError, coincidence.read, card)        # CURIOSITY needs a branch
        card["branch"] = "BR_fixture"
        self.assertEqual(coincidence.read(card)[0], "CURIOSITY")
        if coincidence.source() is not None:
            self.assertTrue(coincidence.run_c1(card, "a", 5.0, "b", 5.0, "a = b", lambda v: v, 0.01)["collapses_to_one_hit"])
            self.assertFalse(coincidence.run_c2(card, 0.01, 20)["surprising_at_005"])


if __name__ == "__main__":
    unittest.main()
