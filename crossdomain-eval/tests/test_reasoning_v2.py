"""Tests for crossdomain_eval.reasoning (OWNER: agent-exp)."""

import pytest

from crossdomain_eval.reasoning_v2 import AssumptionTracker, RuleEngine


# ---------------------------------------------------------------------------
# AssumptionTracker
# ---------------------------------------------------------------------------

class TestAssumptionTracker:
    def test_add_defaults_certain_and_active(self):
        t = AssumptionTracker()
        aid = t.add("friction_is_negligible")
        assert aid == 1
        rep = t.report()
        assert rep == [{"id": 1, "statement": "friction_is_negligible",
                        "confidence": 1.0, "active": True}]

    def test_ids_increase(self):
        t = AssumptionTracker()
        assert t.add("a") == 1
        assert t.add("b") == 2
        assert t.add("c") == 3

    def test_add_strips_whitespace(self):
        t = AssumptionTracker()
        t.add("  laminar_flow  ", 0.9)
        assert t.check("laminar_flow")

    def test_add_rejects_bad_input(self):
        t = AssumptionTracker()
        with pytest.raises(ValueError):
            t.add("")
        with pytest.raises(ValueError):
            t.add("   ")
        with pytest.raises(ValueError):
            t.add("x", confidence=1.5)
        with pytest.raises(ValueError):
            t.add("x", confidence=-0.1)

    def test_check_unknown_is_false(self):
        t = AssumptionTracker()
        assert t.check("never_added") is False

    def test_check_respects_confidence_threshold(self):
        t = AssumptionTracker()
        t.add("weak_hunch", 0.3)
        t.add("coin_flip", 0.5)
        assert t.check("weak_hunch") is False
        assert t.check("coin_flip") is True

    def test_check_uses_most_recent_duplicate(self):
        t = AssumptionTracker()
        t.add("steady_state", 0.9)
        t.add("steady_state", 0.1)  # later, weaker belief shadows earlier
        assert t.check("steady_state") is False
        assert t.confidence_of("steady_state") == 0.1

    def test_retract(self):
        t = AssumptionTracker()
        t.add("ideal_gas")
        assert t.check("ideal_gas") is True
        assert t.retract("ideal_gas") is True
        assert t.check("ideal_gas") is False
        # audit trail preserved
        rep = t.report()
        assert len(rep) == 1 and rep[0]["active"] is False
        # second retract is a no-op
        assert t.retract("ideal_gas") is False
        assert t.retract("never_there") is False

    def test_report_is_a_copy(self):
        t = AssumptionTracker()
        t.add("a")
        rep = t.report()
        rep[0]["active"] = False
        assert t.check("a") is True


# ---------------------------------------------------------------------------
# RuleEngine
# ---------------------------------------------------------------------------

class TestRuleEngine:
    def test_simple_assignment_rule(self):
        e = RuleEngine()
        e.add_rule("temp > 100", "state = 'hot'")
        out = e.infer({"temp": 120})
        assert out["state"] == "hot"
        assert out["_fired"] == [0]

    def test_rule_does_not_fire(self):
        e = RuleEngine()
        e.add_rule("temp > 100", "state = 'hot'")
        out = e.infer({"temp": 20})
        assert "state" not in out
        assert out["_fired"] == []

    def test_chaining_to_fixpoint(self):
        e = RuleEngine()
        e.add_rule("temp > 100", "state = 'hot'")
        e.add_rule("state == 'hot' and pressure > 5", "alarm = True")
        e.add_rule("alarm", "action = 'vent'")
        out = e.infer({"temp": 150, "pressure": 7})
        assert out["state"] == "hot"
        assert out["alarm"] is True
        assert out["action"] == "vent"
        assert out["_fired"] == [0, 1, 2]

    def test_missing_name_in_condition_means_no_fire(self):
        e = RuleEngine()
        e.add_rule("missing_var > 3", "x = 1")
        out = e.infer({})
        assert "x" not in out

    def test_bare_expression_conclusion(self):
        e = RuleEngine()
        e.add_rule("n > 0", "n * 2")
        out = e.infer({"n": 4})
        assert out["conclusion_0"] == 8

    def test_input_facts_not_mutated(self):
        e = RuleEngine()
        e.add_rule("a > 0", "b = a + 1")
        facts = {"a": 1}
        e.infer(facts)
        assert facts == {"a": 1}

    def test_no_infinite_loop_on_self_referential_stable_rule(self):
        e = RuleEngine()
        e.add_rule("x >= 0", "x = x")  # fires but never changes facts
        out = e.infer({"x": 5})
        assert out["x"] == 5

    def test_idempotent_value_stops_firing(self):
        e = RuleEngine()
        e.add_rule("x > 0", "y = 2 * x")
        out1 = e.infer({"x": 3})
        out2 = e.infer(out1)  # re-inferring derived facts is stable
        assert out1["y"] == 6 and out2["y"] == 6

    def test_numeric_expressions(self):
        e = RuleEngine()
        e.add_rule("m > 0 and v > 0", "ke = 0.5 * m * v**2")
        out = e.infer({"m": 2.0, "v": 3.0})
        assert out["ke"] == pytest.approx(9.0)

    def test_add_rule_validation(self):
        e = RuleEngine()
        with pytest.raises(ValueError):
            e.add_rule("", "x = 1")
        with pytest.raises(ValueError):
            e.add_rule("x > 1", "")
        with pytest.raises(ValueError):
            e.add_rule("x >", "y = 1")            # condition doesn't compile
        with pytest.raises(ValueError):
            e.add_rule("x > 1", "2bad = 3")       # invalid target name
        with pytest.raises(ValueError):
            e.add_rule("__import__('os')", "x = 1")
        with pytest.raises(ValueError):
            e.add_rule("x > 1", "evil = open('f')")

    def test_sandbox_blocks_builtins_at_runtime(self):
        e = RuleEngine()
        # 'abs' is not available without builtins
        e.add_rule("abs(x) > 1", "y = 1")
        out = e.infer({"x": -5})
        assert "y" not in out  # NameError in condition -> no fire

    def test_physics_style_scenario(self):
        """End-to-end: classify a flow regime like a domain check would."""
        e = RuleEngine()
        e.add_rule("reynolds < 2300", "regime = 'laminar'")
        e.add_rule("reynolds >= 2300 and reynolds < 4000",
                   "regime = 'transitional'")
        e.add_rule("reynolds >= 4000", "regime = 'turbulent'")
        e.add_rule("regime == 'turbulent'", "needs_tripped_bc = True")
        assert e.infer({"reynolds": 1500})["regime"] == "laminar"
        assert e.infer({"reynolds": 3000})["regime"] == "transitional"
        out = e.infer({"reynolds": 50000})
        assert out["regime"] == "turbulent"
        assert out["needs_tripped_bc"] is True
