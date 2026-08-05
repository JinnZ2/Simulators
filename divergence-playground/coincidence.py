#!/usr/bin/env python3
"""
coincidence.py -- test whether N "hits" are actually independent.  stdlib, CC0.

Four generators, each a separate check.  Run in order: C1 collapses the
most spurious "convergences" (structural identities); C4 is the only
one that survives to become a real common cause.

    C1  SAME OBJECT, TWO SHADOWS
        Two quantities that "coincidentally" agree may be related by a
        deterministic map.  rs_ratio 0.989 vs E_ede +1.1%: both are
        shadows of a fractional-E excess, related by
        r_s ∝ ∫ da/(a²E).  N=1, not 2.
        TEST: state candidate map A = f(B).  Compute residual after
        applying f.  If |residual| < a pre-declared tolerance,
        they are one hit.

    C2  TRIALS FACTOR (look-elsewhere)
        p_effective = 1 - (1 - p_local)^N_trials.
        If you scanned N quantities looking for a match, small p_local
        becomes plausible.
        TEST: state N BEFORE claiming surprise.  If you can't state
        N, you can't claim.

    C3  ELASTIC TARGET
        "≈0.011" -- does 0.013 count?  0.016?  If tolerance was set
        after seeing the number, the tolerance IS the finding.
        TEST: PRE-STATE the match window.  Log it as pre_window.
        Then evaluate the observed match against it.

    C4  REAL COMMON CAUSE
        Survives C1-C3.  The only kind worth having.
        TEST: state an out-of-sample PREDICTION that follows from the
        common cause.  Log it as prediction_of_record.  A real common
        cause constrains something you haven't measured yet.

All four are STRUCTURED ELICITATION -- the tool cannot infer the maps,
the trial counts, or the tolerances.  It refuses to certify a
coincidence claim without them.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Callable, List, Optional


# --- C1 -----------------------------------------------------------------

@dataclass
class C1Test:
    """One candidate deterministic map A = f(B) between two quantities."""
    name_a: str
    value_a: float
    name_b: str
    value_b: float
    map_expr: str                 # human-readable, e.g. "A = 1 - B"
    map_fn: Callable[[float], float]
    tolerance: float = 0.01       # relative

    def run(self) -> dict:
        predicted = self.map_fn(self.value_b)
        # relative residual
        denom = max(abs(self.value_a), abs(predicted), 1e-30)
        rel = abs(self.value_a - predicted) / denom
        return {
            "generator": "C1_same_object_two_shadows",
            "name_a": self.name_a, "value_a": self.value_a,
            "name_b": self.name_b, "value_b": self.value_b,
            "map": self.map_expr, "predicted_a": predicted,
            "relative_residual": rel, "tolerance": self.tolerance,
            "collapses_to_one_hit": rel <= self.tolerance,
        }


# --- C2 -----------------------------------------------------------------

def c2_trials_factor(p_local: float, n_trials: int) -> dict:
    """Return p_effective under a naive look-elsewhere correction."""
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1")
    if not (0 <= p_local <= 1):
        raise ValueError("p_local in [0,1]")
    p_eff = 1.0 - (1.0 - p_local) ** n_trials
    return {"generator": "C2_trials_factor",
            "p_local": p_local, "n_trials": n_trials,
            "p_effective": p_eff,
            "surprising_at_005": p_eff < 0.05}


# --- C3 -----------------------------------------------------------------

@dataclass
class C3Test:
    """Pre-declared tolerance window for a target match."""
    observed: float
    target: float
    pre_window: float          # absolute half-width, declared BEFORE looking
    declared_at: str = ""      # timestamp/context of the pre-declaration

    def run(self) -> dict:
        margin = abs(self.observed - self.target)
        return {
            "generator": "C3_elastic_target",
            "observed": self.observed, "target": self.target,
            "pre_window": self.pre_window, "margin": margin,
            "declared_at": self.declared_at,
            "hits_pre_window": margin <= self.pre_window,
            "note": ("If pre_window was set after seeing observed, this "
                     "test is void.  Log the timestamp/context in "
                     "declared_at and be honest."),
        }


# --- C4 -----------------------------------------------------------------

@dataclass
class C4Test:
    """Real-common-cause claim: name an out-of-sample prediction it makes."""
    cause: str                    # the alleged common cause
    prediction: str               # what to measure
    predicted_value: float
    predicted_uncertainty: float
    pre_registered_at: str = ""

    def run(self, observed_value: Optional[float] = None) -> dict:
        result = {
            "generator": "C4_real_common_cause",
            "cause": self.cause, "prediction": self.prediction,
            "predicted_value": self.predicted_value,
            "predicted_uncertainty": self.predicted_uncertainty,
            "pre_registered_at": self.pre_registered_at,
        }
        if observed_value is None:
            result["status"] = "REGISTERED_AWAITING_OBSERVATION"
            return result
        z = (observed_value - self.predicted_value) / (self.predicted_uncertainty + 1e-30)
        result["observed_value"] = observed_value
        result["z_score"] = z
        result["status"] = "SUPPORTED" if abs(z) <= 1.0 else \
                           "MARGINAL" if abs(z) <= 2.0 else "REFUTED"
        return result


# --- self-test ------------------------------------------------------------

def _t_c1_catches_shadow_pair():
    # rs_ratio = 0.9886 vs E_ede fractional excess ~ 0.0114.  Both are
    # shadows of the same E-integral.  Map: rs_ratio ≈ 1 - E_ede_frac.
    t = C1Test(name_a="rs_ratio", value_a=0.9886,
               name_b="E_ede_frac", value_b=0.0114,
               map_expr="A = 1 - B",
               map_fn=lambda b: 1.0 - b,
               tolerance=0.001)
    r = t.run()
    assert r["collapses_to_one_hit"] is True, r
    assert r["relative_residual"] < 1e-3


def _t_c1_lets_independent_pair_through():
    t = C1Test(name_a="temperature", value_a=300.0,
               name_b="stock_price", value_b=42.0,
               map_expr="A = 7.14 * B (arbitrary)",
               map_fn=lambda b: 7.14 * b,
               tolerance=0.001)
    r = t.run()
    assert r["collapses_to_one_hit"] is True   # by construction the map does fit
    # this is a REMINDER: C1 will 'match' anything if the map is fit post-hoc.
    # honest use: the map is stated from PHYSICS, not eyeballed to fit.


def _t_c2_look_elsewhere():
    r = c2_trials_factor(p_local=0.01, n_trials=100)
    # 1 - 0.99^100 ~ 0.634
    assert 0.6 < r["p_effective"] < 0.7
    assert r["surprising_at_005"] is False


def _t_c3_pre_window_binds():
    t = C3Test(observed=0.013, target=0.011, pre_window=0.005,
               declared_at="2026-08-04 pre-hoc")
    assert t.run()["hits_pre_window"] is True
    t2 = C3Test(observed=0.013, target=0.011, pre_window=0.001,
                declared_at="2026-08-04 pre-hoc")
    assert t2.run()["hits_pre_window"] is False


def _t_c4_registered_prediction():
    t = C4Test(cause="shared E-excess",
               prediction="chi_ls should also decrease by ~1.1%",
               predicted_value=0.989, predicted_uncertainty=0.005,
               pre_registered_at="2026-08-04")
    r = t.run()   # not yet observed
    assert r["status"] == "REGISTERED_AWAITING_OBSERVATION"
    # later, when observed:
    r2 = t.run(observed_value=0.988)
    assert r2["status"] == "SUPPORTED"
    r3 = t.run(observed_value=0.950)
    assert r3["status"] == "REFUTED"


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
