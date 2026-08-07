"""Tests for crossdomain_eval.numerical."""

import math

import numpy as np

from crossdomain_eval.numerical import optimize, root_find, solve_ode


def test_root_find_quadratic():
    r = root_find(lambda x: x ** 2 - 2, (0.0, 2.0))
    assert math.isclose(r, math.sqrt(2), rel_tol=1e-10)


def test_root_find_kwargs():
    r = root_find(lambda x: x ** 3 - x - 2, (1.0, 2.0), xtol=1e-12)
    assert math.isclose(r, 1.5213797068045676, rel_tol=1e-9)


def test_solve_ode_exponential_decay():
    sol = solve_ode(lambda t, y: [-y[0]], [1.0], (0.0, 2.0), n=101)
    assert sol["t"].shape == (101,)
    assert sol["y"].shape == (1, 101)
    assert math.isclose(sol["y"][0, -1], math.exp(-2), rel_tol=1e-5)


def test_solve_ode_harmonic():
    def rhs(t, y):
        return [y[1], -y[0]]

    sol = solve_ode(rhs, [1.0, 0.0], (0.0, math.pi), n=200)
    assert math.isclose(sol["y"][0, -1], -1.0, abs_tol=1e-4)


def test_optimize_unbounded():
    res = optimize(lambda x: (x[0] - 3) ** 2 + (x[1] + 1) ** 2, [0.0, 0.0])
    assert res["success"]
    assert math.isclose(res["x"][0], 3.0, abs_tol=1e-5)
    assert math.isclose(res["x"][1], -1.0, abs_tol=1e-5)
    assert res["fun"] < 1e-10


def test_optimize_bounded():
    res = optimize(lambda x: (x[0] - 5) ** 2, [0.0], bounds=[(0.0, 2.0)])
    assert res["success"]
    assert math.isclose(res["x"][0], 2.0, abs_tol=1e-5)
    assert math.isclose(res["fun"], 9.0, abs_tol=1e-5)


def test_optimize_explicit_method():
    res = optimize(lambda x: float(np.sum(x ** 2)), [1.0, -2.0], method="Nelder-Mead")
    assert res["success"]
    assert res["fun"] < 1e-8
