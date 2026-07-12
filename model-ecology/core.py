"""
core.py
-------
Plugin substrate. Adding a new mathematical method, observer profile, or
representation requires exactly one new class implementing one interface.
Every component is then evaluated by the same audit pipeline. No plugin is
privileged, including whichever representation is currently fashionable.

CC0. stdlib only. Phone-buildable.

ONTOLOGY NOTICE
---------------
A Model here is not a predictor. It is an ORGANISM with a habitat.
Its fitness is not accuracy. Its fitness is:
    (a) where it works,
    (b) where it degrades,
    (c) where it fails catastrophically,
    (d) what it silently assumes,
    (e) what unique information it contributes even when wrong.

Accuracy is one column. It is not the ledger.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


# --------------------------------------------------------------- declarations

@dataclass
class ModelResult:
    """What a model returns, WITH its epistemic baggage attached. Never bare."""
    prediction: list                 # time series or scalar per timestep
    uncertainty: list                # same shape; None entries allowed
    confidence: float                # 0..1, model's own claim about itself
    assumptions_used: list = field(default_factory=list)
    residuals: list = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


class Model:
    """
    Base plugin. Subclass and implement fit/predict.

    `family` is the load-bearing field. It names inherited mathematical
    assumptions, NOT the method's brand name. Two methods with different names
    and the same ancestry are not independent evidence. See phylogeny.py.
    """
    name: str = "unnamed"
    family: str = "unknown"          # spectral | geometric | probabilistic | ...
    assumptions: list = []
    limitations: list = []

    def fit(self, data: list) -> "Model":
        return self

    def predict(self, data: list) -> ModelResult:
        raise NotImplementedError

    def explain(self) -> dict:
        return {
            "name": self.name,
            "family": self.family,
            "assumptions": list(self.assumptions),
            "limitations": list(self.limitations),
        }


@dataclass
class Observer:
    """
    Not psychology. A computational description of perspective.

    The framework's question is never "is this observer right." It is:
    IF I CHANGE ONLY THE OBSERVER, DOES THE CONCLUSION CHANGE?
    If yes -> observer-sensitive. If no -> observer-invariant.
    Observer-invariance is a property you measure, not a virtue you assume.
    """
    name: str
    simplicity_bias: float = 0.5     # 0 = tolerate complexity, 1 = punish it
    uncertainty_bias: float = 0.5    # 0 = tolerate wide bounds, 1 = punish them
    outlier_weight: float = 0.5      # 0 = discard outliers, 1 = privilege them
    determinism_bias: float = 0.5    # 0 = prefer probabilistic, 1 = deterministic
    explain_vs_predict: float = 0.5  # 0 = pure prediction, 1 = pure explanation

    def score(self, model: Model, result: ModelResult) -> float:
        """
        Rank a model result THROUGH this observer's lens.

        Every term must be MODEL-SPECIFIC and computable WITHOUT ground truth,
        or the observer has nothing to bite on and churn is trivially zero.
        Note the deliberate tension: simplicity_bias PUNISHES declared
        assumptions while explain_vs_predict REWARDS declaring them. An honest
        observer axis must be able to disagree with itself.
        """
        d = result.diagnostics
        complexity = len(model.assumptions) / 10.0
        unc = _mean([u for u in result.uncertainty if u is not None]) or 0.0

        s = result.confidence
        s -= self.simplicity_bias * complexity
        s -= self.uncertainty_bias * unc
        s += self.outlier_weight * d.get("novelty", 0.0)
        s += self.determinism_bias * d.get("smoothness", 0.0)
        s += self.explain_vs_predict * complexity      # transparency reward
        return s


# ------------------------------------------------------------------- registry

class Registry:
    """Plugin registry. One decorator, one interface, same audit for everyone."""

    def __init__(self):
        self.models: dict = {}
        self.observers: dict = {}
        self.representations: dict = {}

    def model(self, cls):
        self.models[cls.name] = cls
        return cls

    def observer(self, obs: Observer):
        self.observers[obs.name] = obs
        return obs

    def representation(self, name: str):
        """A representation transform: list -> list. Manifold is one of these,
        with no special standing."""
        def deco(fn: Callable):
            self.representations[name] = fn
            return fn
        return deco


REGISTRY = Registry()


# --------------------------------------------------------------------- helpers

def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _std(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def pearson(a: list, b: list) -> float:
    """Correlation, stdlib. Returns 0.0 on degenerate input rather than raising."""
    n = min(len(a), len(b))
    if n < 2:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va == 0 or vb == 0:
        return 0.0
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return cov / (va ** 0.5 * vb ** 0.5)
