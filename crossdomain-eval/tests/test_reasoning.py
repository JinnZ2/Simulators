"""Tests for crossdomain_eval.reasoning."""

import pytest

from crossdomain_eval.reasoning import AssumptionTracker, RuleEngine


class TestAssumptionTracker:
    def test_add_and_check(self):
        t = AssumptionTracker()
        t.add("temperature > 100", confidence=0.9)
        assert t.check("temperature")
        assert t.check("Temperature")  # case-insensitive
        assert not t.check("pressure")

    def test_default_confidence(self):
        t = AssumptionTracker()
        t.add("friction is negligible")
        rep = t.report()
        assert rep[0]["confidence"] == 1.0
        assert rep[0]["statement"] == "friction is negligible"

    def test_invalid_confidence_raises(self):
        t = AssumptionTracker()
        with pytest.raises(ValueError):
            t.add("bad", confidence=1.5)

    def test_report_returns_copies(self):
        t = AssumptionTracker()
        t.add("a holds")
        rep = t.report()
        rep[0]["confidence"] = 0.0
        assert t.report()[0]["confidence"] == 1.0


class TestRuleEngine:
    def test_simple_rule(self):
        e = RuleEngine()
        e.add_rule("temp > 100", "alert = True")
        out = e.infer({"temp": 150})
        assert out["alert"] is True

    def test_rule_not_fired(self):
        e = RuleEngine()
        e.add_rule("temp > 100", "alert = True")
        out = e.infer({"temp": 50})
        assert "alert" not in out
        assert out["temp"] == 50

    def test_chaining_to_fixpoint(self):
        e = RuleEngine()
        e.add_rule("a > 0", "b = a * 2")
        e.add_rule("b > 10", "c = 'big'")
        out = e.infer({"a": 8})
        assert out["b"] == 16
        assert out["c"] == "big"

    def test_missing_facts_skip_rule(self):
        e = RuleEngine()
        e.add_rule("missing_var > 1", "x = 1")
        out = e.infer({"y": 2})
        assert "x" not in out

    def test_no_builtins(self):
        e = RuleEngine()
        # builtins like len/__import__ are unavailable and rules needing
        # them simply do not fire or apply
        e.add_rule("True", "x = len([1, 2])")
        e.add_rule("__import__('os') is not None", "y = 1")
        out = e.infer({"a": 0})
        assert "x" not in out and "y" not in out
        with pytest.raises(NameError):
            RuleEngine._eval("len([1])", {})

    def test_input_not_mutated(self):
        e = RuleEngine()
        e.add_rule("a > 0", "b = 1")
        facts = {"a": 1}
        e.infer(facts)
        assert facts == {"a": 1}

    def test_bare_expression_conclusion(self):
        e = RuleEngine()
        e.add_rule("x > 0", "x * 2")
        out = e.infer({"x": 3})
        assert out["x_2"] == 6
