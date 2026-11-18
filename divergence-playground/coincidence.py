#!/usr/bin/env python3
"""
coincidence.py -- test whether N "hits" are actually independent.  stdlib, CC0.

Six generators, each a separate check, plus none_of_above.  C1-C3, C5 and C6
are spurious-explanation filters: each names a way a "convergence" can be an
artifact.  C4 is the real-common-cause claim.  none_of_above is DERIVED: it is
supported only when C1-C6 are ALL ruled out, and when it is, it opens its own
branch -- an unexplained convergence to investigate, never a finding certified
from here.

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
        Survives C1-C3 (and C5, C6).  The only kind worth having.
        TEST: state an out-of-sample PREDICTION that follows from the
        common cause.  Log it as prediction_of_record.  A real common
        cause constrains something you haven't measured yet.

    C5  LOCAL NORMAL FORM
        Two systems may match only NEAR a tipping point because both
        reduce to the same simple (normal) form there -- a shared normal
        form, not a shared mechanism.
        TEST: move away from the transition and re-measure.  A true match
        persists; a normal-form match diverges.  Supply match NEAR and FAR
        and a pre-declared persistence tolerance.
        CASE: grid vs ODE fire model near a drought threshold.

    C6  NUMERICAL ARTIFACT
        The match or smoothness may be produced by the numerics -- solver,
        step size, or rounding -- not the physics.  A physical effect is
        stable across solver/step/precision and does NOT grow as the step
        shrinks; roundoff GROWS as dt shrinks (more steps, more accumulated
        error) and an exact-binary step (e.g. 1/64) removes it.
        TEST: change solver, halve/double the step, raise precision, use an
        exact-binary step.  Supply the metric under those changes.
        CASE: run 10 -- deposition counter roundoff (residual grew as dt
        shrank; 1/64 exact).

    none_of_above  DERIVED
        Supported only when C1-C6 are ALL ruled out.  Refuses to infer a
        missing verdict.  When supported, it OPENS ITS OWN BRANCH: the
        convergence is unexplained by any known coincidence class and is
        a thing to investigate, not to certify.

All are STRUCTURED ELICITATION -- the tool cannot infer the maps, the trial
counts, the tolerances, the off-transition match, or the numeric sensitivity.
It refuses to certify a coincidence claim without them.
"""

import json
import random
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


# --- C5 -----------------------------------------------------------------

@dataclass
class C5Test:
    """Do two systems match only because both reduce to the same local normal
    form near a transition?

    A true shared mechanism matches NEAR and FAR from the transition.  A
    normal-form coincidence matches near the tipping point and diverges away
    from it.  Supply a match score (higher = closer) near and far, and a
    pre-declared persistence tolerance: how much the match may drop away from
    the transition before it counts as 'only near'.
    """
    system_a: str
    system_b: str
    match_near: float            # agreement near the transition (higher = closer)
    match_far: float             # agreement away from the transition
    persistence_tol: float       # pre-declared max allowed drop for a true match
    transition: str = ""         # what the tipping point is

    def run(self) -> dict:
        degradation = self.match_near - self.match_far
        explained = degradation > self.persistence_tol
        return {
            "generator": "C5_local_normal_form",
            "system_a": self.system_a, "system_b": self.system_b,
            "transition": self.transition,
            "match_near": self.match_near, "match_far": self.match_far,
            "degradation": degradation,
            "persistence_tol": self.persistence_tol,
            "explained_by_normal_form": explained,
            "persists_away_from_transition": not explained,
            "note": ("A match that holds only near the transition is a shared "
                     "normal form, not a shared mechanism.  Move away and "
                     "re-measure; a true match persists."),
        }


# --- C6 -----------------------------------------------------------------

@dataclass
class C6Test:
    """Is the match/smoothness produced by the numerics (solver, step, rounding)?

    Supply the metric under changed numerics.  A physical effect is stable
    across solver/step/precision and does NOT grow as the step shrinks.  A
    numerical artifact moves when the numerics move; roundoff GROWS as dt
    shrinks; an exact-binary step (e.g. 1/64) removes it.

    Provide at least one of:
      refinement    [(dt, value), ...]  -- the roundoff / non-convergence test
      by_config     {label: value}      -- spread across solver / precision
      exact_binary  (dt, value)         -- the effect at an exact-binary step
    """
    metric_name: str
    stability_tol: float                                   # pre-declared, absolute
    refinement: List[tuple] = field(default_factory=list)  # [(dt, value), ...]
    by_config: dict = field(default_factory=dict)          # {label: value}
    exact_binary: Optional[tuple] = None                   # (dt, value)

    def run(self) -> dict:
        flags: List[str] = []
        out = {
            "generator": "C6_numerical_artifact",
            "metric_name": self.metric_name,
            "stability_tol": self.stability_tol,
        }

        # (a) refinement: does |value| GROW as dt shrinks? (roundoff signature)
        grows = None
        if len(self.refinement) >= 2:
            pts = sorted(self.refinement, key=lambda p: p[0], reverse=True)  # coarse -> fine
            coarse = abs(pts[0][1])
            fine = abs(pts[-1][1])
            grows = (fine - coarse) > self.stability_tol
            out["refinement"] = [{"dt": dt, "value": v} for dt, v in pts]
            out["grows_as_dt_shrinks"] = grows
            if grows:
                flags.append("grows_as_dt_shrinks")

        # (b) spread across solver / precision configs
        spread = None
        if self.by_config:
            vals = list(self.by_config.values())
            spread = max(vals) - min(vals)
            out["config_spread"] = spread
            out["unstable_across_configs"] = spread > self.stability_tol
            if spread > self.stability_tol:
                flags.append("unstable_across_configs")

        # (c) an exact-binary step removes the effect
        if self.exact_binary is not None:
            dt_e, v_e = self.exact_binary
            ref_level = None
            if self.refinement:
                ref_level = max(abs(v) for _, v in self.refinement)
            elif self.by_config:
                ref_level = max(abs(v) for v in self.by_config.values())
            out["exact_binary"] = {"dt": dt_e, "value": v_e}
            if ref_level is not None:
                collapses = abs(v_e) + self.stability_tol < ref_level
                out["effect_collapses_at_exact_step"] = collapses
                if collapses:
                    flags.append("effect_collapses_at_exact_step")

        if grows is None and spread is None and self.exact_binary is None:
            out["status"] = "UNDECIDABLE_NO_NUMERIC_VARIATION"
            out["numerical_artifact"] = None
            out["note"] = ("supply refinement=[(dt,value),...], by_config={label:value}, "
                           "or exact_binary=(dt,value); the tool cannot infer numeric "
                           "sensitivity.")
            return out

        out["flags"] = flags
        out["numerical_artifact"] = len(flags) > 0
        return out


# --- none_of_above ------------------------------------------------------

_COINCIDENCE_CHECKS = ("c1", "c2", "c3", "c4", "c5", "c6")


def none_of_above(ruled_out: dict, branch_id: str = "", note: str = "") -> dict:
    """DERIVED verdict: a convergence survives when C1-C6 are ALL ruled out.

    `ruled_out` must give an explicit bool for each of c1..c6 -- the meaning is
    "this class is ruled out AS THE EXPLANATION" (for c4: no named/supported
    common cause accounts for it).  The tool will not infer a missing verdict:
    a silent False would manufacture a finding, a silent True would hide one.

    When all six are ruled out the convergence is unexplained by any known
    coincidence class and OPENS ITS OWN BRANCH -- it becomes a thing to
    investigate, not a thing certified from here.  The verdict is always tagged
    DERIVED: it follows from the six, it is never observed directly.
    """
    missing = [k for k in _COINCIDENCE_CHECKS if k not in ruled_out]
    if missing:
        raise ValueError(f"none_of_above needs an explicit verdict for: {missing}")
    bad = [k for k in _COINCIDENCE_CHECKS if ruled_out[k] not in (True, False)]
    if bad:
        raise ValueError(f"none_of_above verdicts must be bool (not None) for: {bad}")

    remaining = [k for k in _COINCIDENCE_CHECKS if not ruled_out[k]]
    all_ruled_out = not remaining
    out = {
        "generator": "none_of_above",
        "tag": "DERIVED",
        "ruled_out": {k: ruled_out[k] for k in _COINCIDENCE_CHECKS},
        "checks_not_yet_ruled_out": remaining,
        "opens_branch": all_ruled_out,
    }
    if all_ruled_out:
        out["status"] = "SUPPORTED_OPENS_BRANCH"
        out["branch"] = {
            "branch_id": branch_id or "none_of_above",
            "prompt": ("Unexplained convergence: no structural identity (C1), "
                       "trials factor (C2), elastic target (C3), named common "
                       "cause (C4), local normal form (C5) or numerical artifact "
                       "(C6) accounts for it.  Investigate as a genuine finding; "
                       "do not certify from here."),
            "note": note,
        }
    else:
        out["status"] = "NOT_SUPPORTED"
        out["note"] = ("still explained by: " + ", ".join(remaining) +
                       ".  none_of_above is DERIVED only when all six are ruled out.")
    return out


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


# C5 planted cases: signal fires, null stays silent ----------------------

def _t_c5_normal_form_fires():
    # grid vs ODE fire model: matches at the drought threshold, diverges away.
    t = C5Test(system_a="grid_fire", system_b="ode_fire",
               match_near=0.98, match_far=0.55, persistence_tol=0.10,
               transition="drought threshold")
    r = t.run()
    assert r["explained_by_normal_form"] is True, r
    assert r["persists_away_from_transition"] is False


def _t_c5_true_match_persists_silent():
    # a real shared mechanism: match holds away from the transition.
    t = C5Test(system_a="grid_fire", system_b="ode_fire",
               match_near=0.98, match_far=0.95, persistence_tol=0.10,
               transition="drought threshold")
    r = t.run()
    assert r["explained_by_normal_form"] is False, r
    assert r["persists_away_from_transition"] is True


# C6 planted cases: signal fires, null stays silent ----------------------

def _t_c6_roundoff_fires():
    # run 10 -- deposition counter roundoff: residual grows as dt shrinks,
    # and an exact-binary step (1/64) removes it.
    t = C6Test(metric_name="deposition_residual", stability_tol=0.05,
               refinement=[(0.1, 0.02), (0.05, 0.05), (0.025, 0.11)],
               exact_binary=(1.0 / 64, 0.001))
    r = t.run()
    assert r["grows_as_dt_shrinks"] is True, r
    assert r["effect_collapses_at_exact_step"] is True, r
    assert r["numerical_artifact"] is True


def _t_c6_convergent_effect_silent():
    # a physical effect: residual SHRINKS as dt shrinks (converges), stable.
    t = C6Test(metric_name="deposition_residual", stability_tol=0.05,
               refinement=[(0.1, 0.04), (0.05, 0.02), (0.025, 0.01)])
    r = t.run()
    assert r["grows_as_dt_shrinks"] is False, r
    assert r["numerical_artifact"] is False


def _t_c6_undecidable_without_variation():
    r = C6Test(metric_name="x", stability_tol=0.05).run()
    assert r["numerical_artifact"] is None
    assert r["status"] == "UNDECIDABLE_NO_NUMERIC_VARIATION"


# none_of_above -----------------------------------------------------------

def _t_none_of_above_opens_branch_when_all_ruled_out():
    r = none_of_above({"c1": True, "c2": True, "c3": True,
                       "c4": True, "c5": True, "c6": True},
                      branch_id="FK-X")
    assert r["status"] == "SUPPORTED_OPENS_BRANCH"
    assert r["opens_branch"] is True
    assert r["tag"] == "DERIVED"
    assert r["branch"]["branch_id"] == "FK-X"


def _t_none_of_above_holds_when_one_remains():
    r = none_of_above({"c1": True, "c2": True, "c3": True,
                       "c4": True, "c5": False, "c6": True})
    assert r["status"] == "NOT_SUPPORTED"
    assert r["opens_branch"] is False
    assert r["checks_not_yet_ruled_out"] == ["c5"]


def _t_none_of_above_refuses_to_infer():
    for bad in ({"c1": True}, {k: True for k in _COINCIDENCE_CHECKS[:-1]}):
        try:
            none_of_above(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("none_of_above must refuse a missing verdict")
    nulled = {k: True for k in _COINCIDENCE_CHECKS}
    nulled["c3"] = None
    try:
        none_of_above(nulled)
    except ValueError:
        pass
    else:
        raise AssertionError("none_of_above must refuse a None verdict")


# null-harness discipline (in-folder, stdlib): before trusting C5/C6, show
# each fires on a known-signal class and stays silent on a known-null class.
# Same shape as ../null-harness/null_harness.py bake_off: report FP (null
# fire rate, must be ~0) and TP (signal fire rate, must be ~1).  Seeded.

def _bake_off(gate, null_gen, signal_gen, n=400, seed=0):
    rng = random.Random(seed)
    fp = sum(1 for _ in range(n) if gate(null_gen(rng))) / n
    tp = sum(1 for _ in range(n) if gate(signal_gen(rng))) / n
    return fp, tp


def _t_c5_bake_off_discriminates():
    def gate(d):
        return C5Test("a", "b", d["near"], d["far"], d["tol"]).run()[
            "explained_by_normal_form"]

    def null_gen(rng):                       # true match: persists away
        near = rng.uniform(0.90, 1.00)
        return {"near": near, "far": near - rng.uniform(0.0, 0.03), "tol": 0.10}

    def signal_gen(rng):                     # normal-form: diverges away
        near = rng.uniform(0.90, 1.00)
        return {"near": near, "far": near - rng.uniform(0.30, 0.60), "tol": 0.10}

    fp, tp = _bake_off(gate, null_gen, signal_gen)
    assert fp == 0.0 and tp == 1.0, (fp, tp)   # clean separation (CONSTANT_SILENT null)


def _t_c6_bake_off_discriminates():
    def gate(d):
        return C6Test("m", d["tol"], refinement=d["refine"],
                      exact_binary=d.get("exact")).run()["numerical_artifact"]

    def null_gen(rng):                       # convergent physical effect
        v0 = rng.uniform(0.02, 0.06)
        return {"tol": 0.05,
                "refine": [(0.1, v0), (0.05, v0 / 2), (0.025, v0 / 4)]}

    def signal_gen(rng):                     # roundoff: grows as dt shrinks
        a = rng.uniform(0.02, 0.06)
        return {"tol": 0.05,
                "refine": [(0.1, a), (0.05, 2 * a), (0.025, 4 * a)],
                "exact": (1.0 / 64, 0.0)}

    fp, tp = _bake_off(gate, null_gen, signal_gen)
    assert fp == 0.0 and tp == 1.0, (fp, tp)


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
