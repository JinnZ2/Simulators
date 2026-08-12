"""Tests for crossdomain_eval.experiments."""

import numpy as np
import pytest

from crossdomain_eval.experiments import SweepResult, parameter_sweep, propose_experiments


class TestParameterSweep:
    def test_grid_shape_and_values(self):
        res = parameter_sweep(lambda x, y: x + y, {"x": (0, 1, 3), "y": (0, 2, 3)})
        assert res.results.shape == (3, 3)
        assert res.params["x"].tolist() == [0.0, 0.5, 1.0]
        # results[i, j] = x_i + y_j
        assert res.results[2, 2] == pytest.approx(3.0)

    def test_fixed_params(self):
        res = parameter_sweep(lambda x, c: x * c, {"x": (0, 1, 5)}, fixed={"c": 3})
        assert res.results[-1] == pytest.approx(3.0)
        assert res.fixed == {"c": 3}

    def test_best_max_and_min(self):
        res = parameter_sweep(lambda x: -(x - 2) ** 2, {"x": (0, 4, 9)})
        best = res.best(maximize=True)
        assert best["x"] == pytest.approx(2.0)
        assert best["value"] == pytest.approx(0.0)
        worst = res.best(maximize=False)
        assert worst["x"] in (0.0, 4.0)

    def test_sensitivity_normalized(self):
        # f = x + 0.1*y -> x dominates
        res = parameter_sweep(lambda x, y: x + 0.1 * y, {"x": (0, 1, 11), "y": (0, 1, 11)})
        sens = res.sensitivity()
        assert set(sens) == {"x", "y"}
        # global range is 1.1; marginal effects are 1.0 and 0.1
        assert sens["x"] == pytest.approx(1.0 / 1.1)
        assert sens["y"] == pytest.approx(0.1 / 1.1)
        assert sens["x"] > sens["y"]

    def test_sensitivity_zero_range(self):
        res = parameter_sweep(lambda x: 5.0, {"x": (0, 1, 4)})
        assert res.sensitivity() == {"x": 0.0}


class TestSweepResultDirect:
    def test_construction(self):
        r = SweepResult(results=np.array([1.0, 2.0]), params={"x": np.array([0.0, 1.0])})
        assert r.best()["value"] == 2.0


class TestProposeExperiments:
    def test_full_factorial_two_levels(self):
        plan = propose_experiments("max yield", ["a", "b", "c"], levels=2)
        assert len(plan) == 8
        for run in plan:
            assert run["a"] in (-1.0, 1.0)
            assert run["objective"] == "max yield"
        combos = {(r["a"], r["b"], r["c"]) for r in plan}
        assert len(combos) == 8

    def test_three_levels(self):
        plan = propose_experiments("obj", ["x"], levels=3)
        assert [r["x"] for r in plan] == [-1.0, 0.0, 1.0]
        assert [r["run"] for r in plan] == [1, 2, 3]
