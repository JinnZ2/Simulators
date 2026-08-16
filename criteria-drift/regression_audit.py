"""
regression_audit.py -- the series the regression is run on, and the term it
does not have.

CC0-1.0. Standard library only. Deterministic. Imports the delivered kit;
modifies nothing. Reads the database built by the README's quick start.

Three results, in increasing order of how much of the design they touch:

  1  build_series() plants a y = 0.0 at the head of every model's series and
     pairs it with a real drift value. On the one model with enough data for
     a three-point fit, removing it FLIPS THE SIGN of the slope -- between
     the two opposite readings the README's own decision rule offers.

  2  version_order is built from `to_version`, so the first criteria version
     never appears and any score attached to it is dropped. A model measured
     at the first and last version -- the longest baseline in the dataset --
     contributes nothing.

  3  the regression has no capability term. `reported = a*c + b` is one
     equation in two unknowns, so a slope on drift alone absorbs both. The
     repair is already expressible in the shipped schema and is not asked
     for.

Run `python3 audit.py init` and the README's ingest steps first.
"""

from __future__ import annotations

import os
import sys

import drift
import store
from regress import DriftRegressor, ols_regression

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "drift.db")
ARTIFACT = "CodeBench"
RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def load():
    s = store.DriftStore(DB)
    versions = s.get_criteria_history(ARTIFACT)
    metrics = drift.DriftEngine().compute_history(versions)
    return s, versions, metrics, s.get_score_matrix(ARTIFACT)


def transitions(metrics):
    return {p["to_version"]: (p["from_version"], p["composite_drift"])
            for p in metrics.pairs}


def shipped_series(model_scores, metrics):
    """
    The pre-repair build_series(), reproduced here so the defect and its
    cost stay measurable after the repair. Two things it did: version_order
    from `to_version` only (dropping the first version), and a planted
    y = 0.0 at the head paired with a real drift value.
    """
    order = [p["to_version"] for p in metrics.pairs]
    into = {p["to_version"]: p["composite_drift"] for p in metrics.pairs}
    ordered = [(v, model_scores[v]) for v in order if v in model_scores]
    if len(ordered) < 2:
        return [], []
    x, y = [], []
    for i, (v, sc) in enumerate(ordered):
        x.append(into.get(v, 0.0))
        y.append(0.0 if i == 0 else sc - ordered[i - 1][1])
    return x, y


def honest_series(model_scores, trans):
    """Every transition whose BOTH endpoints have a score. No planted points."""
    x, y = [], []
    for to, (frm, d) in trans.items():
        if frm in model_scores and to in model_scores:
            x.append(d)
            y.append(model_scores[to] - model_scores[frm])
    return x, y


# ---------------------------------------------------------------------------


def check_planted(versions, metrics, matrix) -> None:
    section("1  every series begins with a fabricated point")

    print("  The pre-repair build_series(score_type='delta') set imp = 0.0")
    print("  at i == 0 and paired it with the drift INTO that version -- a")
    print("  real x against a y that was not measured.\n")

    print("  %-12s %-38s %s" % ("model", "y series as built", "planted"))
    print("  " + "-" * 68)
    for m in sorted(matrix):
        x, y = shipped_series(matrix[m], metrics)
        if not y:
            print("  %-12s %-38s %s" % (m, "(empty)", "-"))
            continue
        print("  %-12s %-38s %s"
              % (m, [round(v, 4) for v in y],
                 "1 of %d" % len(y) if y[0] == 0.0 else "no"))

    print()
    print("  It is not padding. For Alpha-1B the head point REPLACES a real")
    print("  measurement:\n")
    a = matrix["Alpha-1B"]
    trans = transitions(metrics)
    frm, d = trans["v2.0"]
    print("      scores      %s -> %.2f, %s -> %.2f"
          % (frm, a[frm], "v2.0", a["v2.0"]))
    print("      real delta  %+.2f" % (a["v2.0"] - a[frm]))
    print("      recorded    %+.2f   at x = %.4f" % (0.0, d))


def check_dropped(versions, metrics, matrix) -> None:
    section("2  the baseline version is not in the series at all")

    reg = DriftRegressor(matrix, metrics)
    print("  all criteria versions   %s" % [v.version_id for v in versions])
    print("  pre-repair order        %s"
          % [p["to_version"] for p in metrics.pairs])
    print("  repaired version_order  %s" % reg.version_order)
    print()
    print("  version_order was [p['to_version'] for p in pairs], so the")
    print("  FIRST version never appeared and any score attached to it was")
    print("  dropped before the series was built.\n")

    print("  %-12s %-30s %-10s %s"
          % ("model", "scores on record", "was", "now"))
    print("  " + "-" * 68)
    for m in sorted(matrix):
        old, _ = shipped_series(matrix[m], metrics)
        new, _ = reg.build_series(m, score_type="delta")
        print("  %-12s %-30s %-10d %d"
              % (m, ",".join(sorted(matrix[m])), len(old), len(new)))

    print()
    print("  Delta-350M holds scores at the FIRST and LAST version -- the")
    print("  longest baseline in the dataset, and the only pair spanning")
    print("  every criteria change. After filtering, one score survives,")
    print("  len(ordered_scores) < 2, and the model returns ([], []).")
    print()
    print("  The two defects push opposite ways on n: the planted head adds")
    print("  a point, the dropped baseline removes one or more. They do not")
    print("  cancel, because they are not the same point.")


def check_repair(versions, metrics, matrix) -> None:
    section("3  what the two defects cost, measured")

    reg = DriftRegressor(matrix, metrics)
    trans = transitions(metrics)

    print("  Corrected series: every transition whose BOTH endpoint scores")
    print("  exist, no planted head, first version included.\n")
    print("  %-12s %-28s %-28s" % ("model", "as shipped", "corrected"))
    print("  " + "-" * 70)
    flips = []
    for m in sorted(matrix):
        x, y = shipped_series(matrix[m], metrics)
        a = ols_regression(x, y)
        cx, cy = reg.build_series(m, score_type="delta")
        b = ols_regression(cx, cy)
        fa = ("n=%d slope=%+.4f" % (a.n, a.slope) if a.n >= 2
              else "n=%d (no fit)" % a.n)
        fb = ("n=%d slope=%+.4f" % (b.n, b.slope) if b.n >= 2
              else "n=%d (below 2)" % b.n)
        if a.n >= 2 and b.n >= 2 and (a.slope > 0) != (b.slope > 0):
            flips.append(m)
        print("  %-12s %-28s %-28s" % (m, fa, fb))

    print()
    if flips:
        print("  SIGN FLIP on %s." % ", ".join(flips))
        print()
        print("  The README's decision rule reads the sign:\n")
        print("      beta1 > 0   criteria inflation explains some gain")
        print("      beta1 < 0   stricter criteria masking real gains\n")
        print("  Alpha-1B is the only model with three real transitions, and")
        print("  the shipped and corrected series put it on opposite sides")
        print("  of that rule. The verdict is set by the fabricated point.")
    print()
    print("  After correction the demo supports one n=3 fit and one n=2.")
    print("  Two models fall below two points. The shipped n column was")
    print("  inflated by the planted head, not by having more data.")
    print()
    print("  REPAIRED, and one more thing the repair made visible: with")
    print("  span pairing, a model scored across a MULTI-version gap is")
    print("  matched against the summed drift over that span rather than")
    print("  dropped. Delta-350M is back in the series.\n")
    total = 0
    for m in sorted(matrix):
        x, _ = reg.build_series(m, score_type="delta")
        total += len(x)
    print("    real observations across all models: %d" % total)
    pooled = reg.regress_pooled()
    d = pooled.to_dict()
    print("    pooled fit  n=%d df=%d slope=%+.4f t=%s p=%s sig=%s"
          % (d["n"], d["df"], d["slope"],
             "n/a" if d["t_slope"] is None else "%.2f" % d["t_slope"],
             "n/a" if d["p_slope"] is None else "%.3f" % d["p_slope"],
             d["significant_at_05"]))
    print()
    print("  composite_drift is a property of the ARTIFACT, so every")
    print("  per-model fit ran against the same x-vector -- four models,")
    print("  four slopes, two signs, from one criteria history. The pooled")
    print("  fit is the one the design's question asks for, and it is the")
    print("  only fit here with degrees of freedom to spare.")


def check_significance(metrics, matrix) -> None:
    section("4  'significant' is in the decision rule and not in the code")

    print("  README.md:\n")
    print("      If the slope is positive and significant, some fraction of")
    print("      'progress' is the ruler stretching.")
    print("      beta1 > 0, significant: Criteria inflation explains ...\n")
    src = open(os.path.join(HERE, "regress.py"), encoding="utf-8").read()
    for term in ("signific", "p_value", "pvalue", "t_stat", "ttest"):
        print("      regress.py contains %-10r  %s"
              % (term, term in src))
    print()
    reg = DriftRegressor(matrix, metrics)
    print("  REPAIRED: t, df, p and significant_at_05 are in to_dict(), and")
    print("  r_squared is null below three points. What the demo produces:\n")
    print("  %-12s %-6s %-11s %-11s %-8s %s"
          % ("model", "n", "slope", "se", "t", "df"))
    print("  " + "-" * 60)
    for m in sorted(matrix):
        r = reg.regress(m)
        if r.n < 2:
            print("  %-12s %-6d %s" % (m, r.n, "(no fit)"))
            continue
        se = r.se_slope
        t = "n/a" if se in (0.0, float("inf")) else "%.2f" % (r.slope / se)
        print("  %-12s %-6d %-11.4f %-11s %-8s %d"
              % (m, r.n, r.slope,
                 "inf" if se == float("inf") else "%.4f" % se, t,
                 max(r.n - 2, 0)))
    print()
    print("  One degree of freedom on the fits that have any. No t is near")
    print("  a conventional threshold, and the interpretation string reports")
    print("  the sign and R-squared without either.")
    print()
    print("  R-squared = 1.000 at n = 2 is arithmetic: two points define a")
    print("  line. `_interpret()` guards it -- 'Insufficient data for")
    print("  reliable inference' -- but `to_dict()` emits `r_squared: 1.0`")
    print("  in the same object, so a consumer reading the FIELD rather than")
    print("  the prose gets a perfect fit. The guard is in the sentence, not")
    print("  in the data.")


def check_identification(metrics, matrix) -> None:
    section("5  the term the regression does not have")

    print("  The research program states the model as:\n")
    print("      reported = b0 + b1*actual_capability_gain")
    print("               + b2*criteria_drift + e\n")
    print("  regress.py runs:\n")
    print("      delta_score = b0 + b1*composite_drift + e\n")
    print("  The capability term is dropped, because it is unobservable.")
    print("  Anything it shares with drift loads onto the reported slope.")
    print()
    print("  And the two are not plausibly independent: a benchmark is")
    print("  revised BECAUSE models saturated it. So drift is downstream of")
    print("  capability, which is the reverse of the direction the slope is")
    print("  read in.")
    print()
    print("  ../anchor-interval/moving_reference.py puts a number on the")
    print("  underlying problem: under `reported = a*c + b`, a capability")
    print("  rising 117%% with a fixed ruler and a capability that never")
    print("  moves under a ruler stretching 117%% produce the same published")
    print("  series to 5.6e-17. One equation, two unknowns, per release.")
    print()
    print("  THE REPAIR IS ALREADY EXPRESSIBLE IN THIS SCHEMA.\n")
    print("      ModelScore keys on (model, artifact, VERSION)")
    print()
    print("  so scoring every model on the FIRST version as well as its")
    print("  contemporary one is a legal ingest today. The divergence")
    print("  between the two series is the criteria term, isolated -- and")
    print("  it identifies capability only up to the fixed version's own")
    print("  unknown gain and offset, so what it buys is a SHARE, not a")
    print("  capability (../anchor-interval/ ANC_006).")
    print()
    print("  Nothing in the CLI asks for it. The example data has one score")
    print("  per model per version and no model scored on a superseded")
    print("  version, which is exactly the design that cannot separate the")
    print("  two terms.")
    print()
    have_old = [m for m, s in matrix.items()
                if len([v for v in s if v != "v3.1-hard"]) > 1]
    print("  models in the demo with scores on more than one non-current")
    print("  version: %d of %d" % (len(have_old), len(matrix)))


def main() -> int:
    if not os.path.exists(DB):
        print("no drift.db -- run the README quick start first")
        return 2
    _s, versions, metrics, matrix = load()

    print()
    print("REGRESSION AUDIT -- criteria_drift_kit")
    print("artifact %s, %d criteria versions, %d models"
          % (ARTIFACT, len(versions), len(matrix)))

    check_planted(versions, metrics, matrix)
    check_dropped(versions, metrics, matrix)
    check_repair(versions, metrics, matrix)
    check_significance(metrics, matrix)
    check_identification(metrics, matrix)

    section("READING")
    print("""
  REPAIRED. Every result below is the pre-repair behaviour, reproduced by
  shipped_series() so the cost stays measurable, against what
  build_series() returns now. tests/test_repairs.py pins each one.

  Two mechanical defects in build_series(). It planted y = 0.0 at the head
  of every series and pairs it with a real drift value -- for Alpha-1B that
  fabricated point REPLACES a measured -0.04 -- and it builds version_order
  from `to_version`, so the first criteria version and every score attached
  to it is dropped before the series exists. Delta-350M holds the longest
  baseline in the dataset, first version to last, and contributes nothing.

  Together they flip a sign. Alpha-1B is the only model with three real
  transitions, and shipped vs corrected put it on opposite sides of the
  README's own decision rule -- criteria inflation against stricter
  criteria masking gains.

  'Significant' appears twice in README.md and zero times in regress.py.
  The fits that exist have one degree of freedom, and R-squared = 1.000 at
  n = 2 is emitted as a field next to an interpretation string that says
  the data is insufficient.

  The structural one is NOT repaired and cannot be by editing a function:
  the capability term is in the stated model and not in the code, because
  it is unobservable, so the drift slope absorbs it. The repair is already
  expressible -- ModelScore keys on version, so scoring every model on the
  first version alongside its contemporary one is a legal ingest today.
  Nothing asks for it, and the example data is built the one way that
  cannot separate the two terms. That stays open as CD_006.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
