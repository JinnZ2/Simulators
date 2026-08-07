"""Parameter sweeps, sensitivity analysis, and DOE plan generation."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class SweepResult:
    """Result of a full-grid parameter sweep.

    Attributes:
        results: Array of objective values with shape
            ``(n1, n2, ...)`` matching the order of ``param_ranges``.
        params: Ordered mapping of parameter name to the grid values used
            (``np.ndarray`` per parameter).
        fixed: Fixed (non-swept) parameters passed to the function.
    """

    results: np.ndarray
    params: dict[str, np.ndarray] = field(default_factory=dict)
    fixed: dict = field(default_factory=dict)

    def sensitivity(self) -> dict[str, float]:
        """Return normalized effect size per swept parameter.

        For each parameter, the marginal means along its axis are computed
        (averaging over all other parameters) and the effect size is
        ``(max - min)`` of those marginal means, normalized by the global
        range (max - min) of all results. Returns 0.0 if the global range
        is zero.
        """
        names = list(self.params)
        global_range = float(np.ptp(self.results))
        sens: dict[str, float] = {}
        for i, name in enumerate(names):
            axes = tuple(j for j in range(self.results.ndim) if j != i)
            marginal = self.results.mean(axis=axes) if axes else self.results
            effect = float(np.ptp(marginal))
            sens[name] = effect / global_range if global_range > 0 else 0.0
        return sens

    def best(self, maximize: bool = True) -> dict:
        """Return the configuration achieving the best objective value.

        Args:
            maximize: If True, return the argmax configuration; otherwise
                the argmin configuration.

        Returns:
            Dict with swept parameter values plus ``"value"``.
        """
        flat = int(np.argmax(self.results) if maximize else np.argmin(self.results))
        idx = np.unravel_index(flat, self.results.shape)
        config = {name: float(vals[idx[i]]) for i, (name, vals) in enumerate(self.params.items())}
        config["value"] = float(self.results[idx])
        return config


def parameter_sweep(
    func: Callable[..., float],
    param_ranges: dict[str, tuple[float, float, int]],
    fixed: dict | None = None,
) -> SweepResult:
    """Evaluate ``func`` over a full grid of the parameter ranges.

    Args:
        func: Callable invoked as ``func(**kwargs)`` returning a float.
        param_ranges: Mapping of parameter name to ``(lo, hi, n_points)``;
            ``n_points`` evenly spaced values are used per parameter.
        fixed: Extra keyword arguments held constant during the sweep.

    Returns:
        A :class:`SweepResult` whose ``results`` array has one axis per
        swept parameter, in the order of ``param_ranges``.
    """
    fixed = dict(fixed or {})
    names = list(param_ranges)
    grids = [np.linspace(lo, hi, n) for lo, hi, n in (param_ranges[k] for k in names)]
    shape = tuple(len(g) for g in grids)
    results = np.empty(shape, dtype=float)
    for idx in itertools.product(*(range(len(g)) for g in grids)):
        kwargs = dict(fixed)
        kwargs.update({name: float(grids[i][idx[i]]) for i, name in enumerate(names)})
        results[idx] = func(**kwargs)
    return SweepResult(results=results, params=dict(zip(names, grids)), fixed=fixed)


def propose_experiments(objective_desc: str, factors: list[str], levels: int = 2) -> list[dict]:
    """Generate a full-factorial design of experiments plan.

    Args:
        objective_desc: Free-text description of the objective (stored on
            each run as ``"objective"``).
        factors: Names of the experimental factors.
        levels: Number of evenly spaced coded levels per factor. For
            ``levels == 2`` the coded levels are ``[-1, 1]``; for
            ``levels == 3`` they are ``[-1, 0, 1]``, etc.

    Returns:
        List of dicts, one per run, mapping each factor to its coded level,
        plus ``"run"`` (1-based run number) and ``"objective"`` keys.
    """
    coded = list(np.linspace(-1.0, 1.0, levels))
    plan: list[dict] = []
    for run_no, combo in enumerate(itertools.product(coded, repeat=len(factors)), start=1):
        run = {name: float(level) for name, level in zip(factors, combo)}
        run["run"] = run_no
        run["objective"] = objective_desc
        plan.append(run)
    return plan
