"""Tests for crossdomain_eval.symbolic."""

import math

import sympy as sp

from crossdomain_eval.symbolic import EquationSet, parse


def test_parse_expression():
    e = parse("x**2 - 4")
    assert e == sp.Symbol("x") ** 2 - 4


def test_parse_equation():
    e = parse("y = 2*x + 1")
    assert isinstance(e, sp.Eq)
    assert e.lhs == sp.Symbol("y")
    assert e.rhs == 2 * sp.Symbol("x") + 1


def test_variables():
    es = EquationSet(["y = m*x + b", "z = x**2"])
    assert es.variables() == ["b", "m", "x", "y", "z"]


def test_substitute_numeric_and_symbolic():
    es = EquationSet(["y = m*x + b"]).substitute({"m": 2, "b": "c + 1"})
    eq = es.equations[0]
    assert eq.rhs == 2 * sp.Symbol("x") + sp.Symbol("c") + 1


def test_solve_target_single():
    es = EquationSet(["x**2 - 4"])
    sol = es.solve("x")
    assert set(sol["x"]) == {sp.Integer(-2), sp.Integer(2)}


def test_solve_target_unique():
    es = EquationSet(["y = 2*x + 1"])
    sol = es.solve("x")
    assert sol["x"] == (sp.Symbol("y") - 1) / 2


def test_solve_system():
    es = EquationSet(["x + y = 3", "x - y = 1"])
    sol = es.solve()
    assert sol["x"] == 2 and sol["y"] == 1


def test_differentiate():
    es = EquationSet(["y = x**3"]).differentiate("x")
    eq = es.equations[0]
    assert eq.rhs == 3 * sp.Symbol("x") ** 2


def test_integrate():
    es = EquationSet(["x"]).integrate("x")
    assert es.equations[0] == sp.Symbol("x") ** 2 / 2


def test_simplify():
    es = EquationSet(["x**2 + 2*x + 1 - (x + 1)**2"]).simplify()
    assert es.equations[0] == 0


def test_evaluate():
    es = EquationSet(["x**2 + y", "d = x - y"])
    out = es.evaluate({"x": 3.0, "y": 2.0, "d": 4.0})
    assert math.isclose(out["x**2 + y"], 11.0)
    assert math.isclose(out["d = x - y"], 3.0)  # lhs - rhs = d - (x - y)


def test_evaluate_solves_lone_unknown():
    es = EquationSet(["F = m*a"])
    out = es.evaluate({"m": 80.0, "a": 9.81})
    assert math.isclose(out["F"], 784.8)


def test_evaluate_multiple_unknowns_raises():
    import pytest

    es = EquationSet(["F = m*a"])
    with pytest.raises(ValueError):
        es.evaluate({"m": 80.0})


def test_immutability():
    es = EquationSet(["y = m*x"])
    es.substitute({"m": 5})
    assert sp.Symbol("m") in es.equations[0].free_symbols
