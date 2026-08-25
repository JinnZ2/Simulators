#!/usr/bin/env python3
"""
residual -- read a miss history and name the folded term.

    residual.py demo                 the four fixtures, run
    residual.py --selftest
    residual.py run FILE.json [--coupling X | --claim ID]

Companion to the fold detector, which finds unbound numbers, and to the
claim record, which defines a bound one. This one reads the residuals a
claim left behind and reports which variable they lean WITH.

WHAT IT DOES NOT DO. It does not rule that a lean was an error. A lean
is a structural fact about a residual series and the tool reports it;
whether it should have been there is the operator's reading. The
vocabulary is enforced, not remembered -- see naming.py.

SIGN CONVENTION, stated because everything downstream inherits it:

    residual = actual - predicted

so overprediction is a NEGATIVE residual. A tool that left this implicit
would have half its readings inverted for half its readers.

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import json
import math
import os
import sys

import naming

# S3: the coupling comes from the claim record. Imported rather than
# reimplemented, so the number the discriminator responds to is the same
# object the clock derives its shelf life from.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "claim-record"))
try:
    import record as claim_record
except ImportError:                                   # pragma: no cover
    claim_record = None

HERE = os.path.dirname(os.path.abspath(__file__))

# [CHOICE 1] a slope counts as a lean when it clears this many standard
# errors. The G-RES shape: a feature against the instrument's own noise,
# with the margin named rather than assumed.
MARGIN = 2.0

# [CHOICE 2] the boundary between strong and weak coupling for the S3
# 2x2. Stipulated: nothing establishes it, it is printed with every run,
# and it is an argument.
COUPLING_STRONG = 0.10

# [CHOICE 4] two axes this correlated cannot be told apart by a ranked
# list of slopes against them. Naming one would be picking, so the report
# names the group. Set high on purpose: the claim is indistinguishability,
# not mere association.
COLLINEAR_AT = 0.99

# [CHOICE 3] windows for the S4 rate check. Four is the fewest that
# gives a regression of lean-on-time more than two points to sit on.
RATE_WINDOWS = 4

# S1 / S5 field 8. S5 names the values `raw | corrected | unknown`; S6
# replaces the state vocabulary with adjusted / unadjusted. S6 governs,
# and the two S5 spellings are accepted as aliases so a series written
# to the letter of S5 still loads.
UNADJUSTED, ADJUSTED, UNKNOWN = "unadjusted", "adjusted", "unknown"
STATUS_ALIASES = {"raw": UNADJUSTED, "corrected": ADJUSTED,
                  "unadjusted": UNADJUSTED, "adjusted": ADJUSTED,
                  "unknown": UNKNOWN}

REFUSED = "REFUSED"
UNINTERPRETABLE = "UNINTERPRETABLE"
RECOVER = "RECOVER"
LOG_AND_LEAVE = "LOG_AND_LEAVE"
CHECK_S2A = "CHECK_S2A"
NO_ACTION = "NO_ACTION"

STABLE, GROWING, RATE_NOT_COMPUTABLE = "STABLE", "GROWING", "NOT_COMPUTABLE"


# ---------------------------------------------------------------- stats

def _mean(xs):
    return sum(xs) / float(len(xs))


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def slope(xs, ys):
    """OLS slope, its standard error, and the standardized slope.

    The standardized slope is the one that RANKS. Raw slopes against
    predictors with different units are not on one scale, and sorting
    them would be a comparison across unlike objects -- G-DIM, in the
    one place a ranked list makes it easy to miss.
    """
    n = len(xs)
    if n < 3 or len(ys) != n:
        return {"state": "TOO_FEW", "slope": None, "se": None,
                "standardized": None, "lean": None}
    mx, my = _mean(xs), _mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx <= 0:
        return {"state": "NO_VARIATION", "slope": None, "se": None,
                "standardized": None, "lean": None}
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    sse = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    se = math.sqrt(sse / (n - 2) / sxx) if sse > 0 else 0.0
    sdy = _sd(ys)
    std = (b * _sd(xs) / sdy) if sdy > 0 else None
    lean = (se == 0.0 and b != 0.0) or (se > 0 and abs(b) > MARGIN * se)
    return {"state": "OK", "slope": b, "se": se, "standardized": std,
            "lean": bool(lean), "n": n}


def correlation(xs, ys):
    """|r| between two axes. Used to find axes that cannot be separated."""
    r = slope(xs, ys)
    return None if r["standardized"] is None else abs(r["standardized"])


def collinear_group(series, rows, top):
    """Axes indistinguishable from the top-ranked one.

    A ranked list of slopes cannot separate two axes that move together:
    the residual leans with both by the same amount, and naming one is
    picking. S2 asks for the term to be NAMED rather than inferred, and
    naming the wrong one of a collinear pair is a worse failure than
    naming the pair.
    """
    axes = {"predicted magnitude": series.predicted,
            "time index": series.time_index}
    axes.update(series.predictors)
    base = axes.get(top)
    if base is None:
        return [top]
    out = [top]
    for r in rows:
        name = r["against"]
        if name == top or name not in axes:
            continue
        c = correlation(base, axes[name])
        if c is not None and c >= COLLINEAR_AT:
            out.append(name)
    return out


def pooled_sign(res):
    """One row, never the verdict. S2 says so and the fixtures show why."""
    n = len(res)
    nz = [r for r in res if r != 0.0]
    if len(nz) < 3:
        return {"state": "TOO_FEW", "fraction_positive": None, "lean": None}
    p = sum(1 for r in nz if r > 0) / float(len(nz))
    se = math.sqrt(0.25 / len(nz))
    return {"state": "OK", "fraction_positive": p, "se": se,
            "lean": abs(p - 0.5) > MARGIN * se, "n": len(nz)}


# ---------------------------------------------------------------- S1

class Series(object):
    __slots__ = ("name", "predicted", "actual", "predictors", "time_index",
                 "correction_status", "correction_method", "correction_depth")

    def __init__(self, name, predicted, actual, predictors=None,
                 time_index=None, correction_status=UNKNOWN,
                 correction_method=None, correction_depth=None):
        self.name = name
        self.predicted = [float(x) for x in predicted]
        self.actual = [float(x) for x in actual]
        self.predictors = {k: [float(x) for x in v]
                           for k, v in (predictors or {}).items()}
        self.time_index = ([float(t) for t in time_index]
                           if time_index is not None
                           else list(range(len(self.predicted))))
        self.correction_status = STATUS_ALIASES.get(
            str(correction_status).lower(), str(correction_status))
        self.correction_method = correction_method
        self.correction_depth = correction_depth

    @property
    def residual(self):
        return [a - p for a, p in zip(self.actual, self.predicted)]


def admit(series):
    """S1. An adjusted series is refused with a reason, not scored."""
    if series.correction_status == ADJUSTED:
        return (False,
                "the series is flagged %s. S1 admits unadjusted residuals "
                "only, because a slope measured after something was "
                "subtracted is a property of what was subtracted as much "
                "as of the claim. What was subtracted: %s"
                % (ADJUSTED, series.correction_method or "not recorded"))
    if series.correction_status not in (UNADJUSTED, UNKNOWN):
        return (False, "correction_status %r is not one of %s"
                % (series.correction_status,
                   ", ".join((UNADJUSTED, ADJUSTED, UNKNOWN))))
    return True, None


# ---------------------------------------------------------------- S2

def conditional_lean(series):
    """S2. Slopes against magnitude, each predictor, and time."""
    res = series.residual
    rows = [{"row": "S2a", "against": "predicted magnitude", "kind": "magnitude",
             **slope(series.predicted, res)}]
    for k in sorted(series.predictors):
        rows.append({"row": "S2b", "against": k, "kind": "predictor",
                     **slope(series.predictors[k], res)})
    rows.append({"row": "S2c", "against": "time index", "kind": "time",
                 **slope(series.time_index, res)})
    ps = pooled_sign(res)
    ps.update({"row": "pooled", "against": "sign only", "kind": "pooled",
               "slope": None, "standardized": None})
    ranked = sorted([r for r in rows if r.get("standardized") is not None],
                    key=lambda r: -abs(r["standardized"]))
    leaning = [r for r in ranked if r.get("lean")]
    cand = leaning[0]["against"] if leaning else None
    group = collinear_group(series, leaning, cand) if cand else []
    return {"rows": rows + [ps], "ranked": ranked, "pooled": ps,
            "candidate": cand,
            "candidate_row": leaning[0]["row"] if leaning else None,
            "candidate_group": group,
            "separable": len(group) == 1,
            "any_conditional_lean": bool(leaning),
            "any_lean": bool(leaning) or bool(ps.get("lean"))}


# ---------------------------------------------------------------- S4

def rate_check(series, windows=RATE_WINDOWS):
    """S4. Is the lean stable or growing.

    Lean magnitude per window is the S2(a) slope inside that window,
    regressed on window index. A growing lean is a DIFFERENT finding
    from a stable one and the report keeps them apart.
    """
    res = series.residual
    n = len(res)
    if n < windows * 3:
        return {"state": RATE_NOT_COMPUTABLE, "why":
                "%d points over %d windows leaves fewer than 3 per window"
                % (n, windows), "per_window": []}
    size = n // windows
    mags, per = [], []
    for w in range(windows):
        lo = w * size
        hi = n if w == windows - 1 else (w + 1) * size
        s = slope(series.predicted[lo:hi], res[lo:hi])
        per.append({"window": w, "n": hi - lo, "slope": s["slope"],
                    "state": s["state"]})
        if s["slope"] is None:
            return {"state": RATE_NOT_COMPUTABLE,
                    "why": "window %d: %s" % (w, s["state"]),
                    "per_window": per}
        mags.append(abs(s["slope"]))
    trend = slope(list(range(windows)), mags)
    if trend["state"] != "OK":
        return {"state": RATE_NOT_COMPUTABLE, "why": trend["state"],
                "per_window": per}
    return {"state": GROWING if trend["lean"] else STABLE,
            "trend_slope": trend["slope"], "trend_se": trend["se"],
            "per_window": per,
            "reads": ("the lean grows with the time index: by S4 the "
                      "background moved past the rate ceiling and the claim "
                      "has left its stated domain of validity. A different "
                      "repair from a missing term.")
            if trend["lean"] else
                     ("the lean does not grow with the time index: by S4 a "
                      "missing term, with the claim still inside its "
                      "domain.")}


# ---------------------------------------------------------------- S3

def respond(lean_present, coupling, strong_at=COUPLING_STRONG):
    """S3. Only one cell is a work order."""
    if coupling is None:
        return {"cell": "COUPLING_UNKNOWN", "strong": None,
                "reads": "S3 needs a coupling. Take it from the claim "
                         "record's clock, or perturb the constant and "
                         "measure the movement; dependent count is the "
                         "fallback and is named as one when used."}
    strong = abs(coupling) >= strong_at
    if lean_present and strong:
        return {"cell": RECOVER, "strong": True,
                "reads": "lean present and coupling strong. The term is "
                         "named below; S3 requires that it be named rather "
                         "than inferred from the lean existing."}
    if lean_present:
        return {"cell": LOG_AND_LEAVE, "strong": False,
                "reads": "lean present and coupling weak. Recorded; no "
                         "recovery order."}
    if strong:
        return {"cell": CHECK_S2A, "strong": True,
                "reads": "no lean and coupling strong. S3 sends this back "
                         "to S2(a) before the absence is accepted: a "
                         "magnitude-conditional lean is what a pooled test "
                         "misses, and strong coupling is where it costs."}
    return {"cell": NO_ACTION, "strong": False,
            "reads": "no lean and coupling weak."}


# ---------------------------------------------------------------- run

def analyse(series, coupling=None, coupling_source=None,
            strong_at=COUPLING_STRONG):
    ok, why = admit(series)
    if not ok:
        return {"series": series.name, "verdict": REFUSED, "why": why}
    s2 = conditional_lean(series)
    s4 = rate_check(series)

    # S5 field 8. A symmetric series whose adjustment history is unknown
    # cannot be read: a claim that left no lean and a claim whose lean was
    # removed produce the same artifact. The schema emits this rather
    # than defaulting to clean.
    if series.correction_status == UNKNOWN and not s2["any_lean"]:
        return {"series": series.name, "verdict": UNINTERPRETABLE,
                "s2": s2, "s4": s4, "coupling": coupling,
                "coupling_source": coupling_source,
                "why": "no lean, and the adjustment history is %s. A series "
                       "with no lean and one whose lean was removed are the "
                       "same artifact from here, so this is not a clean "
                       "score. It is an absence of grounds for either "
                       "reading." % UNKNOWN}
    r = respond(s2["any_lean"], coupling, strong_at)
    return {"series": series.name, "verdict": r["cell"], "response": r,
            "s2": s2, "s4": s4, "coupling": coupling,
            "coupling_source": coupling_source}


def coupling_from_claim(cid, records_dir=None):
    """S3's first source. Returns (value, provenance).

    The order's fallback chain is explicit: the claim record first, then
    perturbation, then dependent count -- and the last is named as a
    fallback wherever it is used, because a count is not an elasticity
    and a report that did not say which it had would be comparing two
    quantities in one column.
    """
    if claim_record is None:
        return None, "claim-record is not importable from here"
    reg = claim_record.Registry.load(records_dir)
    rec = reg.records.get(cid)
    if rec is None:
        return None, "%s is not in the claim registry" % cid
    q = ((rec.get("clock") or {}).get("coupling")) or {}
    if q.get("state") == "UNMEASURED":
        return None, ("the claim record states the coupling UNMEASURED: %s"
                      % q.get("why", "no reason recorded"))
    v = q.get("value")
    if not isinstance(v, (int, float)):
        return None, "the claim record carries no coupling value"
    return float(v), ("claim record %s, clock.coupling, basis: %s"
                      % (cid, (q.get("basis") or "")[:80]))


# ---------------------------------------------------------------- render

def table(headers, rows):
    w = [len(h) for h in headers]
    body = [[str(x) for x in r] for r in rows]
    for r in body:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(c))
    fmt = "  ".join("%-" + str(x) + "s" for x in w)
    out = [fmt % tuple(headers), fmt % tuple("-" * x for x in w)]
    for r in body:
        out.append((fmt % tuple(r)).rstrip())
    return "\n".join(out)


def _f(v, spec="%.4g"):
    return "-" if v is None else spec % v


def render(res):
    L = ["series            %s" % res["series"],
         "verdict           %s" % res["verdict"]]
    if res["verdict"] == REFUSED:
        L += ["", res["why"]]
        return "\n".join(L)
    L += ["coupling          %s%s"
          % (_f(res.get("coupling")),
             "  (%s)" % res["coupling_source"]
             if res.get("coupling_source") else ""),
          "margin            %g standard errors" % MARGIN,
          "sign convention   residual = actual - predicted",
          "",
          "S2 -- conditional lean. Ranked by the STANDARDIZED slope, which",
          "is dimensionless; raw slopes against different predictors are",
          "not on one scale and are shown but not sorted on.",
          ""]
    rows = []
    for r in res["s2"]["rows"]:
        rows.append([r["row"], r["against"],
                     _f(r.get("slope")), _f(r.get("se")),
                     _f(r.get("standardized")),
                     "-" if r.get("lean") is None else
                     ("lean" if r["lean"] else "."),
                     r.get("state", "-")])
    L.append(table(["row", "against", "slope", "se", "standardized",
                    "lean", "state"], rows))
    ps = res["s2"]["pooled"]
    L += ["", "pooled sign fraction positive: %s  (one row, not the verdict)"
          % _f(ps.get("fraction_positive"))]
    cand = res["s2"]["candidate"]
    grp = res["s2"].get("candidate_group") or []
    if not cand:
        L += ["", "folded-term candidate: NONE NAMED -- no conditional row "
              "leans"]
    elif len(grp) == 1:
        L += ["", "folded-term candidate: %s, from %s"
              % (cand, res["s2"]["candidate_row"])]
    else:
        L += ["",
              "folded-term candidate: NOT SEPARABLE -- %s"
              % ", ".join(grp),
              "  these axes correlate at %.2f or above with each other, so"
              % COLLINEAR_AT,
              "  the residual leans with all of them by the same amount and",
              "  a ranked list cannot say which. Naming one would be",
              "  picking. Separating them needs a series in which they",
              "  move independently."]
    s4 = res["s4"]
    L += ["", "S4 -- rate check: %s" % s4["state"]]
    if s4.get("reads"):
        L.append("  " + s4["reads"])
    if s4.get("why"):
        L.append("  " + s4["why"])
    if s4.get("per_window"):
        L.append("  per-window S2(a) slope: %s"
                 % ", ".join(_f(w["slope"]) for w in s4["per_window"]))
    if res.get("response"):
        L += ["", "S3 -- %s" % res["response"]["cell"],
              "  " + res["response"]["reads"]]
    if res["verdict"] == UNINTERPRETABLE:
        L += ["", "  " + res["why"]]
    L += ["", "This report states structure. It does not rule that a lean",
          "was an error, and no column here is a judgement."]
    return "\n".join(L)


# ---------------------------------------------------------------- fixtures

def _noise(n, amp, seed):
    """Deterministic small jitter. No RNG state leaks between fixtures."""
    import random
    rng = random.Random(seed)
    return [rng.uniform(-amp, amp) for _ in range(n)]


def fixture(which):
    n = 120
    pred = [1.0 + i * (100.0 / n) for i in range(n)]
    if which == "F1":
        # Overpredict small, underpredict large. Pooled: symmetric.
        eps = _noise(n, 0.3, 11)
        res = [(-4.0 if p < 50.0 else 4.0) + e for p, e in zip(pred, eps)]
        st, meth, depth = UNADJUSTED, None, 0
    elif which == "F2":
        eps = _noise(n, 0.6, 22)
        res = [3.0 + e for e in eps]
        st, meth, depth = UNADJUSTED, None, 0
    elif which == "F3":
        eps = _noise(n, 0.3, 33)
        res = [(-6.0 + 12.0 * (i / float(n - 1))) * (0.2 + 1.6 * i / (n - 1.0))
               + eps[i] for i in range(n)]
        st, meth, depth = UNADJUSTED, None, 0
    elif which == "F4":
        eps = _noise(n, 0.5, 44)
        res = [e for e in eps]
        st, meth, depth = UNKNOWN, None, None
    else:
        raise ValueError(which)
    actual = [p + r for p, r in zip(pred, res)]
    return Series(which, pred, actual,
                  predictors={"unrelated": [math.sin(i / 7.0)
                                            for i in range(n)]},
                  correction_status=st, correction_method=meth,
                  correction_depth=depth)


FIXTURE_COUPLING = {"F1": 0.8, "F2": 0.01, "F3": 0.7, "F4": 0.5}


def demo():
    out = []
    for f in ("F1", "F2", "F3", "F4"):
        s = fixture(f)
        out.append(render(analyse(s, FIXTURE_COUPLING[f],
                                  "fixture, stipulated")))
        out.append("=" * 68)
    return "\n".join(out)


# ---------------------------------------------------------------- selftest

def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("residual selftest")

    # Known answers for the slope, from the algebra.
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    ck("slope of an exact line", round(slope(xs, [2 * x + 1 for x in xs])
                                       ["slope"], 9), 2.0)
    ck("a flat series has slope zero",
       round(slope(xs, [7.0] * 5)["slope"], 9), 0.0)
    ck("a predictor with no variation is a state, not a zero",
       slope([3.0] * 5, [1.0, 2.0, 3.0, 4.0, 5.0])["state"], "NO_VARIATION")
    ck("too few points is a state, not a zero",
       slope([1.0, 2.0], [1.0, 2.0])["state"], "TOO_FEW")
    ck("the standardized slope is dimensionless and scale-free",
       round(slope([x * 1000 for x in xs],
                   [2 * x + 1 for x in xs])["standardized"], 9),
       round(slope(xs, [2 * x + 1 for x in xs])["standardized"], 9))

    # F1: the counterexample S2 exists for.
    r1 = analyse(fixture("F1"), FIXTURE_COUPLING["F1"], "stipulated")
    ck("F1 pooled sign returns no lean", r1["s2"]["pooled"]["lean"], False)
    s2a = [r for r in r1["s2"]["rows"] if r["row"] == "S2a"][0]
    ck("F1 S2(a) fires", s2a["lean"], True)
    ck("F1 top-ranked axis is predicted magnitude",
       r1["s2"]["candidate"], "predicted magnitude")
    # In F1 the predicted values rise with the time index, which is the
    # common real shape. The two axes are then indistinguishable and the
    # report says so instead of picking one.
    ck("F1 names the collinear group rather than one of it",
       (r1["s2"]["separable"], sorted(r1["s2"]["candidate_group"])),
       (False, ["predicted magnitude", "time index"]))
    ck("F1 verdict is a work order", r1["verdict"], RECOVER)

    # F2: one-directional lean, weak coupling.
    r2 = analyse(fixture("F2"), FIXTURE_COUPLING["F2"], "stipulated")
    ck("F2 pooled sign fires", r2["s2"]["pooled"]["lean"], True)
    ck("F2 has no conditional lean", r2["s2"]["any_conditional_lean"], False)
    ck("F2 verdict is log and leave", r2["verdict"], LOG_AND_LEAVE)
    ck("F2 names no term, because no conditional row leans",
       r2["s2"]["candidate"], None)

    # F3: growing lean, and it must be a DIFFERENT output.
    r3 = analyse(fixture("F3"), FIXTURE_COUPLING["F3"], "stipulated")
    ck("F3 rate check reports growing", r3["s4"]["state"], GROWING)
    ck("F1 rate check does not", r1["s4"]["state"], STABLE)
    ck("F2 rate check does not", r2["s4"]["state"], STABLE)
    ck("F3 output is distinct from F1 and F2",
       len({render(r1), render(r2), render(r3)}), 3)

    # F4: the instrument's own record.
    r4 = analyse(fixture("F4"), FIXTURE_COUPLING["F4"], "stipulated")
    ck("F4 emits uninterpretable", r4["verdict"], UNINTERPRETABLE)
    ck("F4 is not scored as a clean series",
       r4["verdict"] in (NO_ACTION, CHECK_S2A), False)
    # And the same series with the history known reads differently.
    known = fixture("F4")
    known.correction_status = UNADJUSTED
    ck("the same series with a known history is readable",
       analyse(known, 0.5, "stipulated")["verdict"] in
       (NO_ACTION, CHECK_S2A), True)
    ck("an adjusted series is refused, not scored",
       analyse(Series("x", [1, 2, 3], [1, 2, 3],
                      correction_status="adjusted"))["verdict"], REFUSED)
    ck("and S5's own spelling loads as the same state",
       Series("x", [1], [1], correction_status="corrected"
              ).correction_status, ADJUSTED)

    # S3, all four cells.
    ck("2x2: lean + strong", respond(True, 0.9)["cell"], RECOVER)
    ck("2x2: lean + weak", respond(True, 0.01)["cell"], LOG_AND_LEAVE)
    ck("2x2: no lean + strong", respond(False, 0.9)["cell"], CHECK_S2A)
    ck("2x2: no lean + weak", respond(False, 0.01)["cell"], NO_ACTION)
    ck("a missing coupling is a state, not weak",
       respond(True, None)["cell"], "COUPLING_UNKNOWN")

    # S3's first source: the claim record, imported not reimplemented.
    v, src = coupling_from_claim("UNF_GRID_IRAQ")
    ck("the coupling is read from the claim record",
       (round(v, 4) if v is not None else None), 0.8815)
    ck("and its provenance travels with it", "clau" in src or "claim" in src,
       True)
    v2, why2 = coupling_from_claim("UNF_PALESTINE")
    ck("a record with a coupling gives one", v2 is not None, True)
    v3, why3 = coupling_from_claim("NO_SUCH_CLAIM")
    ck("an unknown claim is a state with a reason, not a zero",
       (v3, "not in the claim registry" in why3), (None, True))

    # S6, over everything this module emits.
    out = demo()
    ck("the emitted report carries no screened form",
       naming.check(out)[0], True)
    ck("and the screen would fire if it drifted",
       naming.check(out + "\napply a %s %sion" % ("b" + "ias", "correct"))[0],
       False)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  residual.py demo
  residual.py run FILE.json [--coupling X | --claim CLAIM_ID]
  residual.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) > 1 and argv[1] == "demo":
        out = demo()
        print(out)
        return 0 if naming.check(out)[0] else 1
    if len(argv) > 2 and argv[1] == "run":
        d = json.load(open(argv[2]))
        s = Series(d.get("name", argv[2]), d["predicted"], d["actual"],
                   d.get("predictors"), d.get("time_index"),
                   d.get("correction_status", UNKNOWN),
                   d.get("correction_method"), d.get("correction_depth"))
        c, src = None, None
        if "--coupling" in argv:
            c = float(argv[argv.index("--coupling") + 1])
            src = "given on the command line"
        elif "--claim" in argv:
            c, src = coupling_from_claim(argv[argv.index("--claim") + 1])
        out = render(analyse(s, c, src))
        print(out)
        return 0 if naming.check(out)[0] else 1
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
