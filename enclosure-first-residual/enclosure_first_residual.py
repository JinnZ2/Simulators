#!/usr/bin/env python3
"""
enclosure_first_residual -- enter enclosure terms FIRST, measure residual,
and only then treat the residual as a trait candidate.

    enclosure_first_residual.py demo                 the seven fixtures
    enclosure_first_residual.py run PANEL.json       one panel
    enclosure_first_residual.py run PANEL.json --json --emit-branch-set F.json
    enclosure_first_residual.py --selftest

Work order K, delivered verbatim in WORK_ORDER.md. Findings in CLAIM_TABLE.md.

WHAT IT DOES. Given person-windows (person_id, t0, t1) each carrying the
four enclosure terms and one or more graded behavior terms, it runs:

    0. schema gate      a behavior term with no operationalization string
                        is BLOCKED, not estimated
    1. envelope         a within-person change the person CHOSE is out of
                        envelope; only exogenous changes enter the within arm
    2. NULL FIRST       enclosure terms shuffled within the population,
                        refit, null residual band printed BEFORE any real fit
    3. between arm      behavior ~ enclosure across person-windows
    4. within arm       delta behavior ~ delta enclosure, same person,
                        |delta effective_exits| >= threshold  (discriminator)
    5. compare          the order's table, section PIPELINE step 4

WHAT IT DOES NOT DO. It does not exclude trait. Trait is demoted from
assumption to survivor of a control, and a trait result is a RESULT with
the same standing as no result. It does not use the human label set
(rigidity, resistance to change, closed-minded); those are closed nodes and
a panel carrying them is BLOCKED at the schema gate.

DEPENDENCIES. method-layer (F: branch_set, G: preference_free_rank) is a
declared external dependency, located via METHOD_LAYER_PATH or a sibling
checkout. When it is present the return classes ARE G's enum and the branch
set round-trips through F's loader. When it is absent the same values are
mirrored locally and the record says so; nothing is estimated differently.

RESIDUAL, stated once because both arms inherit it:

    residual = SSE / SST     fraction of the arm's own behavior variance
                             left after its enclosure regressors

so 1.0 is "enclosure explains nothing here" and 0.0 is "everything".

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import argparse
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# declared choices. Every number that could move a result is here, printed
# with every run, and is an argument.
# ---------------------------------------------------------------------------

# [CHOICE 1] the within arm admits a pair only when effective_exits moved by
# at least this much. The order says "threshold" and leaves the value open.
DELTA_THRESHOLD = 1

# [CHOICE 2] draws for the permutation null and for the bootstrap CIs.
NULL_DRAWS = 300
BOOT_DRAWS = 300

# [CHOICE 3] the compare step. ratio = residual_within / residual_between.
#   ratio <= DOMINANT_RATIO            "<<"  enclosure account
#   DOMINANT_RATIO < ratio <= CONFOUND  "~"   trait candidate survives
#   ratio > CONFOUND_RATIO             ">"   confound, selection into windows
DOMINANT_RATIO = 0.5
CONFOUND_RATIO = 1.25

# [CHOICE 4] the null band is the central 95% of the null residual draws.
# The observed residual is "inside" when it is >= the band's lower edge:
# a real fit lowers residual, so only the low side is evidence.
NULL_LOWER_Q = 0.025
NULL_UPPER_Q = 0.975

# [CHOICE 5] fewest within-person pairs the discriminator will fit. One
# regressor plus an intercept leaves no residual under three.
MIN_WITHIN_PAIRS = 3

# [CHOICE 6] forced by fixtures F1 and F3 (CLAIM_TABLE EFR_003, EFR_004):
# the step-4 table's cells are ordered backwards on the ratio axis, so the
# default return is a corrected reading of the same two arms -- within arm
# against its own null (does behavior move with enclosure?), then the
# person-stable share of the between residual against its null (is anything
# left that sits with the person?). --table-literal returns the order's
# table exactly as written; the table cell is printed either way.
CORRECTED_READING = True

GRADED_TERMS = (
    "latency_to_approach_novel",
    "test_phase_present",
    "perseveration_rate",
    "arousal_clearance_time",
)

# The closed nodes. Named here only so the schema gate can refuse them.
CLOSED_LABELS = (
    "rigidity", "resistance_to_change", "closed_minded", "closed-minded",
    "openness", "flexibility", "stubbornness",
)

ORIGIN_PATTERN = "behavior attributed to individual trait"

CHOICES = {
    "DELTA_THRESHOLD": DELTA_THRESHOLD,
    "NULL_DRAWS": NULL_DRAWS,
    "BOOT_DRAWS": BOOT_DRAWS,
    "DOMINANT_RATIO": DOMINANT_RATIO,
    "CONFOUND_RATIO": CONFOUND_RATIO,
    "NULL_BAND": [NULL_LOWER_Q, NULL_UPPER_Q],
    "MIN_WITHIN_PAIRS": MIN_WITHIN_PAIRS,
    "CORRECTED_READING": CORRECTED_READING,
}

# ---------------------------------------------------------------------------
# method-layer (F, G). Located, never vendored.
# ---------------------------------------------------------------------------


def _find_method_layer():
    candidates = []
    env = os.environ.get("METHOD_LAYER_PATH")
    if env == "none":            # explicit: run as if the dependency were absent
        return None
    if env:
        candidates.append(env)
    up1 = os.path.dirname(HERE)
    up2 = os.path.dirname(up1)
    for base in (up1, up2, os.path.dirname(up2)):
        candidates.append(os.path.join(base, "method-layer"))
        candidates.append(os.path.join(base, "jinnz2", "method-layer"))
    for c in candidates:
        if os.path.isfile(os.path.join(c, "branch_set.py")) and \
           os.path.isfile(os.path.join(c, "preference_free_rank.py")):
            return c
    return None


METHOD_LAYER_PATH = _find_method_layer()
if METHOD_LAYER_PATH and METHOD_LAYER_PATH not in sys.path:
    sys.path.insert(0, METHOD_LAYER_PATH)
try:
    import branch_set as F                     # noqa: E402
    import preference_free_rank as G           # noqa: E402
    METHOD_LAYER = "present"
except Exception:                              # pragma: no cover - CI path
    F = None
    G = None
    METHOD_LAYER = "absent"


class ReturnClass(object):
    """Mirror of G.ReturnClass values. Checked equal to G's when G is present
    (selftest); used alone when it is not."""
    SCORED = "SCORED"
    UNKNOWN_MEASURABLE = "UNKNOWN_measurable"
    BLOCKED = "BLOCKED"
    OUT_OF_ENVELOPE = "OUT_OF_ENVELOPE"
    VARIABLE_UNIDENT = "VARIABLE_UNIDENT"


# The order's return type, section RETURN TYPE. Peer classes: a scored
# return is not privileged over an unscored one.
KIND_ENCLOSURE_DOMINANT = "ENCLOSURE_DOMINANT"
KIND_TRAIT_RESIDUAL = "TRAIT_RESIDUAL"
KIND_UNKNOWN = "UNKNOWN_measurable"
KIND_BLOCKED = "BLOCKED"
KIND_OUT_OF_ENVELOPE = "OUT_OF_ENVELOPE"
KIND_CONFOUND = "CONFOUND"   # carried on G's VARIABLE_UNIDENT, see below

BLOCK_NO_WITHIN = "no_within_person_windows"
BLOCK_UNOPERATIONALIZED = "unoperationalized_term"


def make_return(kind, fraction=None, ci=None, reason=None, blocker=None):
    """Build the typed return. When G is present the object is a real
    G.CriterionResult, so SCORED-without-value or BLOCKED-without-blocker
    fail at construction rather than in a reader's hands."""
    if kind in (KIND_ENCLOSURE_DOMINANT, KIND_TRAIT_RESIDUAL):
        rc, value, note, blk = ReturnClass.SCORED, fraction, kind, None
    elif kind == KIND_UNKNOWN:
        rc, value, note, blk = ReturnClass.UNKNOWN_MEASURABLE, None, reason, None
    elif kind == KIND_BLOCKED:
        rc, value, note, blk = ReturnClass.BLOCKED, None, reason, blocker
    elif kind == KIND_OUT_OF_ENVELOPE:
        rc, value, note, blk = ReturnClass.OUT_OF_ENVELOPE, None, reason, None
    elif kind == KIND_CONFOUND:
        # The order's step 4 third row ("confound, likely selection into
        # windows; report and stop") has no entry in its RETURN TYPE list.
        # G's VARIABLE_UNIDENT is the peer class whose meaning matches: the
        # variable doing the work cannot be identified from this design.
        rc, value, note, blk = ReturnClass.VARIABLE_UNIDENT, None, reason, None
    else:
        raise ValueError("unknown return kind %r" % kind)
    # the mirror enforces G's contract even when G is absent
    if rc == ReturnClass.SCORED:
        if value is None or not math.isfinite(float(value)):
            raise ValueError("%s requires a finite fraction" % kind)
    elif value is not None:
        raise ValueError("%s cannot carry a fraction" % kind)
    if rc == ReturnClass.BLOCKED and not (isinstance(blk, str) and blk.strip()):
        raise ValueError("BLOCKED requires a named blocker")
    out = {
        "kind": kind,
        "return_class": rc,
        "fraction": None if value is None else round(value, 4),
        "ci": None if ci is None else [round(ci[0], 4), round(ci[1], 4)],
        "blocker": blk,
        "note": note,
    }
    if G is not None:
        typed = G.CriterionResult(G.ReturnClass(rc), value=value, blocker=blk, note=note)
        out["envelope_status"] = typed.envelope_status.value
    else:
        out["envelope_status"] = ("out_of_envelope" if rc == ReturnClass.OUT_OF_ENVELOPE
                                  else "in_envelope")
    return out


def label(ret):
    if ret["kind"] in (KIND_ENCLOSURE_DOMINANT, KIND_TRAIT_RESIDUAL):
        return "%s(fraction=%.3f, CI=[%.3f, %.3f])" % (
            ret["kind"], ret["fraction"], ret["ci"][0], ret["ci"][1])
    if ret["kind"] == KIND_BLOCKED:
        return "BLOCKED(%s)" % ret["blocker"]
    if ret["kind"] == KIND_CONFOUND:
        return "VARIABLE_UNIDENT(confound: %s)" % ret["note"]
    if ret["note"]:
        return "%s(%s)" % (ret["kind"], ret["note"])
    return ret["kind"]


# ---------------------------------------------------------------------------
# panel schema
# ---------------------------------------------------------------------------


class SchemaError(ValueError):
    pass


def effective_exits(enc):
    """count(reachability == 1 AND exit_cost <= 1.0). The term that carries
    the hypothesis; option_set_size is the nominal count and overstates."""
    return sum(1 for r, c in zip(enc["reachability"], enc["exit_cost"])
               if int(r) == 1 and float(c) <= 1.0)


def enclosure_features(enc):
    n = int(enc["option_set_size"])
    for key in ("exit_cost", "reachability", "reversibility"):
        if len(enc[key]) != n:
            raise SchemaError("%s has %d entries, option_set_size is %d"
                              % (key, len(enc[key]), n))
    for c in enc["exit_cost"]:
        if not (isinstance(c, (int, float)) and math.isfinite(c) and c >= 0):
            raise SchemaError("exit_cost must be finite and >= 0 (fraction of resources AVAILABLE)")
    for key in ("reachability", "reversibility"):
        for v in enc[key]:
            if int(v) not in (0, 1):
                raise SchemaError("%s entries must be 0/1" % key)
    return {
        "option_set_size": n,
        "effective_exits": effective_exits(enc),
        "reversible_count": sum(int(v) for v in enc["reversibility"]),
        "mean_exit_cost": (sum(float(c) for c in enc["exit_cost"]) / n) if n else 0.0,
    }


def load_panel(obj):
    """Validate and normalise a panel dict. Raises SchemaError; the caller
    turns an unoperationalized term into BLOCKED rather than an exception."""
    if not isinstance(obj, dict) or "windows" not in obj:
        raise SchemaError("panel must be an object with a 'windows' list")
    ops = obj.get("operationalizations") or {}
    windows = []
    terms = set()
    for i, w in enumerate(obj["windows"]):
        for key in ("person_id", "t0", "t1", "enclosure", "behavior"):
            if key not in w:
                raise SchemaError("window %d missing %r" % (i, key))
        origin = w.get("change_origin", "unknown")
        if origin not in ("baseline", "exogenous", "chosen", "unknown"):
            raise SchemaError("window %d change_origin must be baseline|exogenous|chosen|unknown" % i)
        feats = enclosure_features(w["enclosure"])
        beh = {}
        for term, val in w["behavior"].items():
            if val is None:
                continue
            if not (isinstance(val, (int, float)) and math.isfinite(val)):
                raise SchemaError("window %d behavior %r must be a finite number" % (i, term))
            beh[term] = float(val)
            terms.add(term)
        windows.append({
            "person_id": str(w["person_id"]), "t0": w["t0"], "t1": w["t1"],
            "change_origin": origin, "features": feats, "behavior": beh,
        })
    windows.sort(key=lambda w: (w["person_id"], str(w["t0"])))
    return {"population": obj.get("population", "unnamed"),
            "operationalizations": ops, "windows": windows,
            "terms": sorted(terms)}


def schema_gate(panel):
    """Return {term: block_reason} for terms that may not be estimated."""
    blocked = {}
    for term in panel["terms"]:
        if term in CLOSED_LABELS or term.replace("-", "_") in CLOSED_LABELS:
            blocked[term] = "closed label from the human set; not a graded form"
        elif term not in GRADED_TERMS:
            blocked[term] = "not one of the graded forms %s" % (GRADED_TERMS,)
        else:
            op = panel["operationalizations"].get(term)
            if not isinstance(op, str) or not op.strip():
                blocked[term] = "no operationalization string"
    return blocked


# ---------------------------------------------------------------------------
# least squares, small and exact
# ---------------------------------------------------------------------------


def _solve(A, b):
    """Gaussian elimination with partial pivoting. Returns None if singular."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col:
                f = M[r][col] / M[col][col]
                if f:
                    for c in range(col, n + 1):
                        M[r][c] -= f * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def ols_residual_fraction(X, y):
    """Fit y ~ 1 + X by least squares. Returns (SSE/SST, coefs, dropped)
    where dropped lists regressor indices removed for being constant or
    collinear. SST == 0 returns (None, ...)."""
    n = len(y)
    if n == 0:
        return None, [], []
    ybar = sum(y) / n
    sst = sum((v - ybar) ** 2 for v in y)
    if sst <= 0:
        return None, [], []
    p = len(X[0]) if X else 0
    keep = [j for j in range(p) if len(set(round(row[j], 12) for row in X)) > 1]
    dropped = [j for j in range(p) if j not in keep]
    cols = [[1.0] + [row[j] for j in keep] for row in X]
    k = len(keep) + 1
    while True:
        XtX = [[sum(r[a] * r[b] for r in cols) for b in range(k)] for a in range(k)]
        Xty = [sum(r[a] * y[i] for i, r in enumerate(cols)) for a in range(k)]
        beta = _solve(XtX, Xty)
        if beta is not None or k == 1:
            break
        dropped.append(keep.pop())          # collinear: drop the last one
        cols = [c[:-1] for c in cols]
        k -= 1
    if beta is None:
        beta = [ybar]
    sse = sum((y[i] - sum(bj * r[j] for j, bj in enumerate(beta))) ** 2
              for i, r in enumerate(cols))
    return sse / sst, beta, dropped


def percentile(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    lo = int(math.floor(k))
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def band(vals, lo_q=0.025, hi_q=0.975):
    s = sorted(v for v in vals if v is not None)
    if not s:
        return None
    return {"mean": sum(s) / len(s), "lo": percentile(s, lo_q),
            "hi": percentile(s, hi_q), "n": len(s)}


# ---------------------------------------------------------------------------
# the arms
# ---------------------------------------------------------------------------

FEATURE_ORDER = ("effective_exits", "reversible_count")   # decision regressors
NOMINAL_ORDER = ("option_set_size",)                       # comparison only


def _xy(windows, term, order):
    X, y, who = [], [], []
    for w in windows:
        if term in w["behavior"]:
            X.append([float(w["features"][f]) for f in order])
            y.append(w["behavior"][term])
            who.append(w["person_id"])
    return X, y, who


def between_arm(windows, term, rng):
    X, y, who = _xy(windows, term, FEATURE_ORDER)
    Xn, _, _ = _xy(windows, term, NOMINAL_ORDER)
    n = len(y)
    res, beta, dropped = ols_residual_fraction(X, y)
    res_nom, _, _ = ols_residual_fraction(Xn, y)
    boots = []
    for _ in range(BOOT_DRAWS):
        idx = [rng.randrange(n) for _ in range(n)]
        r, _, _ = ols_residual_fraction([X[i] for i in idx], [y[i] for i in idx])
        boots.append(r)
    return {"n_windows": n, "residual": res, "ci": band(boots),
            "residual_nominal_only": res_nom, "coefs": beta,
            "dropped_regressors": [FEATURE_ORDER[j] for j in dropped],
            "_X": X, "_y": y, "_who": who}


def null_between(windows, term, rng):
    """NULL FIRST. Shuffle the enclosure feature vectors across windows within
    the population, refit, keep the residual. Behavior stays put."""
    X, y, _ = _xy(windows, term, FEATURE_ORDER)
    draws = []
    for _ in range(NULL_DRAWS):
        Xs = X[:]
        rng.shuffle(Xs)
        r, _, _ = ols_residual_fraction(Xs, y)
        draws.append(r)
    return band(draws, NULL_LOWER_Q, NULL_UPPER_Q)


def within_pairs(windows, term):
    """Consecutive same-person window pairs. Each pair carries the LATER
    window's change_origin, since that is the change the pair straddles."""
    by_person = {}
    for w in windows:
        by_person.setdefault(w["person_id"], []).append(w)
    pairs = []
    single = []
    for pid, ws in by_person.items():
        ws = [w for w in ws if term in w["behavior"]]
        if len(ws) < 2:
            if ws:
                single.append(pid)
            continue
        for a, b in zip(ws, ws[1:]):
            pairs.append({
                "person_id": pid,
                "origin": b["change_origin"],
                "d_effective_exits": b["features"]["effective_exits"] - a["features"]["effective_exits"],
                "dX": [float(b["features"][f] - a["features"][f]) for f in FEATURE_ORDER],
                "dy": b["behavior"][term] - a["behavior"][term],
            })
    return pairs, sorted(single)


def within_arm(pairs, rng):
    X = [p["dX"] for p in pairs]
    y = [p["dy"] for p in pairs]
    n = len(y)
    res, beta, dropped = ols_residual_fraction(X, y)
    boots = []
    for _ in range(BOOT_DRAWS):
        idx = [rng.randrange(n) for _ in range(n)]
        r, _, _ = ols_residual_fraction([X[i] for i in idx], [y[i] for i in idx])
        boots.append(r)
    nulls = []
    for _ in range(NULL_DRAWS):
        Xs = X[:]
        rng.shuffle(Xs)
        r, _, _ = ols_residual_fraction(Xs, y)
        nulls.append(r)
    return {"n_pairs": n, "residual": res, "ci": band(boots),
            "null": band(nulls, NULL_LOWER_Q, NULL_UPPER_Q), "coefs": beta,
            "dropped_regressors": [FEATURE_ORDER[j] for j in dropped]}


def person_stable_component(between, rng):
    """[CHOICE 6] Fraction of the between-arm residual variance that sits
    between persons (ANOVA-style intraclass share), with a permutation null
    from shuffling person labels. A residual with no person-stable share
    has not survived anything and is not a trait candidate."""
    X, y, who = between["_X"], between["_y"], between["_who"]
    _, beta, dropped = ols_residual_fraction(X, y)
    keep = [j for j in range(len(FEATURE_ORDER)) if FEATURE_ORDER[j] not in between["dropped_regressors"]]
    resid = []
    for i, row in enumerate(X):
        pred = beta[0] + sum(beta[k + 1] * row[j] for k, j in enumerate(keep))
        resid.append(y[i] - pred)

    def icc(labels):
        groups = {}
        for r, p in zip(resid, labels):
            groups.setdefault(p, []).append(r)
        multi = {p: g for p, g in groups.items() if len(g) >= 2}
        if len(multi) < 2:
            return None
        grand = sum(sum(g) for g in multi.values()) / sum(len(g) for g in multi.values())
        ss_between = sum(len(g) * (sum(g) / len(g) - grand) ** 2 for g in multi.values())
        ss_total = sum((r - grand) ** 2 for g in multi.values() for r in g)
        return None if ss_total <= 0 else ss_between / ss_total

    observed = icc(who)
    if observed is None:
        return {"share": None, "null": None, "above_null": None,
                "note": "fewer than two persons with two or more windows"}
    nulls = []
    for _ in range(NULL_DRAWS):
        labels = who[:]
        rng.shuffle(labels)
        nulls.append(icc(labels))
    nb = band(nulls, NULL_LOWER_Q, NULL_UPPER_Q)
    return {"share": observed, "null": nb,
            "above_null": bool(nb and observed > nb["hi"]), "note": None}


# ---------------------------------------------------------------------------
# the pipeline, one behavior term
# ---------------------------------------------------------------------------


def run_term(panel, term, seed=0, table_literal=False, out=None):
    out = out or sys.stdout
    rng = random.Random(seed)
    P = lambda s="": print(s, file=out)  # noqa: E731
    rec = {"term": term, "operationalization": panel["operationalizations"].get(term),
           "seed": seed, "choices": dict(CHOICES, CORRECTED_READING=not table_literal)}
    windows = [w for w in panel["windows"] if term in w["behavior"]]
    P("== %s" % term)
    P("   operationalization: %s" % rec["operationalization"])

    # 1. envelope, on the within pairs
    pairs_all, single = within_pairs(windows, term)
    exo = [p for p in pairs_all if p["origin"] == "exogenous"]
    chosen = [p for p in pairs_all if p["origin"] == "chosen"]
    unknown = [p for p in pairs_all if p["origin"] in ("unknown", "baseline")]
    rec["envelope"] = {"pairs_total": len(pairs_all), "exogenous": len(exo),
                       "chosen": len(chosen), "unknown_origin": len(unknown),
                       "single_window_persons": single}
    P("   envelope: %d within pairs, %d exogenous, %d chosen (excluded), %d unknown origin (excluded)"
      % (len(pairs_all), len(exo), len(chosen), len(unknown)))
    if single:
        P("   flagged: %d single-window person(s) go to the between arm only: %s"
          % (len(single), ", ".join(single[:8]) + (" ..." if len(single) > 8 else "")))

    # 2. NULL FIRST -- printed before any real fit
    null_b = null_between(windows, term, rng)
    rec["null_between"] = null_b
    if null_b is None:
        rec["return"] = make_return(KIND_UNKNOWN, reason="behavior has no variance; nothing to fit")
        P("   NULL: not computable (no behavior variance)")
        P("   -> %s" % label(rec["return"]))
        return rec
    P("   NULL FIRST (enclosure shuffled within population, %d draws):" % NULL_DRAWS)
    P("      null residual mean %.4f   band [%.4f, %.4f]" % (null_b["mean"], null_b["lo"], null_b["hi"]))

    # 3. between arm
    bt = between_arm(windows, term, rng)
    rec["between"] = {k: v for k, v in bt.items() if not k.startswith("_")}
    P("   between arm  n=%d  residual %.4f  CI [%.4f, %.4f]   (nominal option_set_size only: %.4f)"
      % (bt["n_windows"], bt["residual"], bt["ci"]["lo"], bt["ci"]["hi"], bt["residual_nominal_only"]))
    if bt["dropped_regressors"]:
        P("   dropped constant/collinear regressor(s): %s" % ", ".join(bt["dropped_regressors"]))
    inside = bt["residual"] >= null_b["lo"]
    rec["null_gate"] = {"observed": bt["residual"], "inside_null_band": inside}
    if inside:
        rec["return"] = make_return(
            KIND_UNKNOWN,
            reason="observed between residual %.4f inside null band [%.4f, %.4f]; enclosure terms have no traction here, so no residual is a trait candidate"
            % (bt["residual"], null_b["lo"], null_b["hi"]))
        P("   null gate: observed residual is INSIDE the null band")
        P("   -> %s" % label(rec["return"]))
        return rec
    P("   null gate: observed residual is below the null band; proceeding")

    # 4. within arm (discriminator)
    admitted = [p for p in exo if abs(p["d_effective_exits"]) >= DELTA_THRESHOLD]
    rec["within_admitted"] = len(admitted)
    if not pairs_all or (not exo and chosen):
        if not pairs_all:
            rec["return"] = make_return(KIND_BLOCKED, blocker=BLOCK_NO_WITHIN,
                                        reason="no person has two windows for this term")
        else:
            rec["return"] = make_return(
                KIND_OUT_OF_ENVELOPE,
                reason="every within-person enclosure change was chosen by the person; reverse causation unresolvable")
        P("   -> %s" % label(rec["return"]))
        return rec
    if len(admitted) < MIN_WITHIN_PAIRS:
        rec["return"] = make_return(
            KIND_BLOCKED, blocker=BLOCK_NO_WITHIN,
            reason="%d exogenous pair(s) with |delta effective_exits| >= %d; need %d"
            % (len(admitted), DELTA_THRESHOLD, MIN_WITHIN_PAIRS))
        P("   within arm: %d admitted pair(s), fewer than %d" % (len(admitted), MIN_WITHIN_PAIRS))
        P("   -> %s" % label(rec["return"]))
        return rec
    wt = within_arm(admitted, rng)
    rec["within"] = wt
    P("   within arm   n=%d pairs (|delta effective_exits| >= %d, exogenous)  residual %.4f  CI [%.4f, %.4f]   null band [%.4f, %.4f]"
      % (wt["n_pairs"], DELTA_THRESHOLD, wt["residual"], wt["ci"]["lo"], wt["ci"]["hi"],
         wt["null"]["lo"], wt["null"]["hi"]))

    # 5. compare -- the order's table, printed as a row every run
    ratio = wt["residual"] / bt["residual"] if bt["residual"] > 0 else float("inf")
    rng2 = random.Random(seed + 1)
    Xb, yb = bt["_X"], bt["_y"]
    Xw = [p["dX"] for p in admitted]
    yw = [p["dy"] for p in admitted]
    ratios = []
    for _ in range(BOOT_DRAWS):
        ib = [rng2.randrange(len(yb)) for _ in yb]
        iw = [rng2.randrange(len(yw)) for _ in yw]
        rb, _, _ = ols_residual_fraction([Xb[i] for i in ib], [yb[i] for i in ib])
        rw, _, _ = ols_residual_fraction([Xw[i] for i in iw], [yw[i] for i in iw])
        if rb and rw is not None and rb > 0:
            ratios.append(rw / rb)
    rband = band(ratios)
    if rband["lo"] <= DOMINANT_RATIO and rband["hi"] > CONFOUND_RATIO:
        cell = "straddle"
    elif ratio <= DOMINANT_RATIO:
        cell = "<<"
    elif ratio > CONFOUND_RATIO:
        cell = ">"
    else:
        cell = "~"
    rec["compare"] = {"ratio": ratio, "ratio_ci": rband, "table_cell": cell}
    P("   compare      ratio within/between %.4f  CI [%.4f, %.4f]   table cell: %s"
      % (ratio, rband["lo"], rband["hi"], cell))

    ps = person_stable_component(bt, random.Random(seed + 2))
    rec["person_stable"] = ps
    if ps["share"] is not None:
        P("   person-stable share of between residual %.3f   null band [%.3f, %.3f]   %s"
          % (ps["share"], ps["null"]["lo"], ps["null"]["hi"], "ABOVE" if ps["above_null"] else "not above"))

    if table_literal:
        # The order's step 4, verbatim. See CLAIM_TABLE EFR_003/EFR_004 for
        # where the fixtures land under it.
        if cell == "straddle":
            rec["return"] = make_return(
                KIND_UNKNOWN,
                reason="ratio CI [%.3f, %.3f] spans both decision boundaries (%.2f, %.2f); more windows"
                % (rband["lo"], rband["hi"], DOMINANT_RATIO, CONFOUND_RATIO))
        elif cell == "<<":
            rec["return"] = make_return(KIND_ENCLOSURE_DOMINANT, fraction=1.0 - wt["residual"],
                                        ci=(1.0 - wt["ci"]["hi"], 1.0 - wt["ci"]["lo"]))
        elif cell == ">":
            rec["return"] = make_return(
                KIND_CONFOUND,
                reason="residual_within %.3f > residual_between %.3f (table, literal)"
                % (wt["residual"], bt["residual"]))
        else:
            rec["return"] = make_return(KIND_TRAIT_RESIDUAL, fraction=bt["residual"],
                                        ci=(bt["ci"]["lo"], bt["ci"]["hi"]))
        P("   -> %s" % label(rec["return"]))
        return rec

    # Corrected reading (default). Same ingredients, read in the direction
    # the variance algebra allows. [CHOICE 6]
    #   a. does behavior MOVE with enclosure within person? within residual
    #      against its own permutation null.
    #   b. if it does, is anything person-stable left over? person-stable
    #      share of the between residual against its permutation null.
    tracks = wt["residual"] < wt["null"]["lo"]
    weak = tracks and wt["ci"]["hi"] >= wt["null"]["lo"]
    rec["corrected"] = {"within_tracks": tracks, "within_weak": weak}
    if weak:
        rec["return"] = make_return(
            KIND_UNKNOWN,
            reason="within residual %.3f is below its null band [%.3f, %.3f] but its CI reaches back into it; more exogenous pairs"
            % (wt["residual"], wt["null"]["lo"], wt["null"]["hi"]))
    elif not tracks:
        rec["return"] = make_return(
            KIND_CONFOUND,
            reason="between arm passed the null gate but within-person delta enclosure does not move behavior (residual %.3f, null band [%.3f, %.3f]); selection into windows likely"
            % (wt["residual"], wt["null"]["lo"], wt["null"]["hi"]))
    elif ps["share"] is None:
        rec["return"] = make_return(KIND_UNKNOWN, reason="trait check not computable: " + ps["note"])
    elif ps["above_null"]:
        tf = trait_fraction_ci(bt, random.Random(seed + 3))
        rec["trait_fraction"] = tf
        rec["return"] = make_return(KIND_TRAIT_RESIDUAL, fraction=tf["point"], ci=(tf["ci"]["lo"], tf["ci"]["hi"]),
                                    )
        rec["return"]["note"] = ("person-stable residual after enclosure; enclosure also moves behavior "
                                 "within person (fraction %.3f)" % (1.0 - wt["residual"]))
    else:
        rec["return"] = make_return(KIND_ENCLOSURE_DOMINANT, fraction=1.0 - wt["residual"],
                                    ci=(1.0 - wt["ci"]["hi"], 1.0 - wt["ci"]["lo"]))
    P("   -> %s" % label(rec["return"]))
    return rec


def trait_fraction_ci(between, rng):
    """TRAIT_RESIDUAL fraction = (person-stable share) x (between residual):
    the share of between-arm behavior variance that is left after enclosure
    AND sits stably with the person. Cluster bootstrap over persons."""
    X, y, who = between["_X"], between["_y"], between["_who"]
    persons = sorted(set(who))
    rows = {}
    for i, p in enumerate(who):
        rows.setdefault(p, []).append(i)

    def frac(Xs, ys, whos):
        r, beta, dropped = ols_residual_fraction(Xs, ys)
        if r is None:
            return None
        keep = [j for j in range(len(FEATURE_ORDER)) if j not in dropped]
        resid = [ys[i] - (beta[0] + sum(beta[k + 1] * Xs[i][j] for k, j in enumerate(keep)))
                 for i in range(len(ys))]
        groups = {}
        for rr, p in zip(resid, whos):
            groups.setdefault(p, []).append(rr)
        multi = {p: g for p, g in groups.items() if len(g) >= 2}
        if len(multi) < 2:
            return None
        grand = sum(sum(g) for g in multi.values()) / sum(len(g) for g in multi.values())
        ssb = sum(len(g) * (sum(g) / len(g) - grand) ** 2 for g in multi.values())
        sst = sum((v - grand) ** 2 for g in multi.values() for v in g)
        return None if sst <= 0 else (ssb / sst) * r

    point = frac(X, y, who)
    draws = []
    for _ in range(BOOT_DRAWS):
        Xs, ys, ws = [], [], []
        for k in range(len(persons)):
            p = persons[rng.randrange(len(persons))]
            for i in rows[p]:
                Xs.append(X[i]); ys.append(y[i]); ws.append("%s#%d" % (p, k))
        draws.append(frac(Xs, ys, ws))
    return {"point": point, "ci": band(draws)}


def run_panel(panel, seed=0, table_literal=False, out=None):
    out = out or sys.stdout
    P = lambda s="": print(s, file=out)  # noqa: E731
    P("enclosure_first_residual  population=%s  windows=%d  persons=%d  method-layer=%s"
      % (panel["population"], len(panel["windows"]),
         len(set(w["person_id"] for w in panel["windows"])), METHOD_LAYER))
    P("choices: %s" % json.dumps(dict(CHOICES, CORRECTED_READING=not table_literal), sort_keys=True))
    blocked = schema_gate(panel)
    results = {}
    for term in panel["terms"]:
        if term in blocked:
            ret = make_return(KIND_BLOCKED, blocker=BLOCK_UNOPERATIONALIZED, reason=blocked[term])
            results[term] = {"term": term, "return": ret, "schema": blocked[term]}
            P("== %s" % term)
            P("   schema gate: %s" % blocked[term])
            P("   -> %s" % label(ret))
            continue
        results[term] = run_term(panel, term, seed=seed, table_literal=table_literal, out=out)
    return {"population": panel["population"], "method_layer": METHOD_LAYER,
            "method_layer_path": METHOD_LAYER_PATH, "results": results}


# ---------------------------------------------------------------------------
# branch set (emit to F)
# ---------------------------------------------------------------------------


def branch_set_dict(run=None):
    """The order's BRANCH SET, schema 1.0. A run's returns update statuses:
    ENCLOSURE_DOMINANT eliminates trait_plain for that term; nothing else is
    eliminated by this instrument alone."""
    common = dict(origin_pattern=ORIGIN_PATTERN,
                  discriminator="within-person delta effective_exits (exogenous change)",
                  cost=1.0, status="open", eliminated_by=None,
                  suppression_cause="prior", access_kind=None,
                  predicts_elsewhere=[{
                      "pattern": "captive-vs-released behavior tracks the option set, same discriminator",
                      "domain": "animal behavior",
                      "already_in_record": "unknown",
                      "record_state": "instrument_exists_unrun"}],
                  instrument_history=[])
    branches = [
        dict(common, id="enclosure_constraint",
             generator="behavior is a function of effective exits; it moves when they move",
             predicted_divergence="residual_within << residual_between"),
        dict(common, id="trait_plain",
             generator="behavior is a stable property of the person",
             predicted_divergence="residual_within ~ residual_between with a person-stable residual share"),
        dict(common, id="selection_into_enclosure",
             generator="persons are sorted into enclosures by the behavior; association is not causal",
             predicted_divergence="residual_within > residual_between"),
        dict(common, id="measurement_artifact_of_label_set",
             generator="the human label set manufactures the trait; graded forms do not show it",
             predicted_divergence="effect present under closed labels, absent under graded forms"),
    ]
    if run:
        for term, rec in run["results"].items():
            k = rec["return"]["kind"]
            if k == KIND_ENCLOSURE_DOMINANT:
                for b in branches:
                    if b["id"] == "trait_plain" and b["status"] == "open":
                        b["status"] = "eliminated"
                        b["eliminated_by"] = "K run on %s / %s: %s" % (run["population"], term, label(rec["return"]))
            elif k == KIND_TRAIT_RESIDUAL:
                for b in branches:
                    if b["id"] == "trait_plain" and b["status"] == "open":
                        b["status"] = "survived"
    return {"schema_version": "1.0", "branches": branches}


def emit_branch_set(path, run=None):
    d = branch_set_dict(run)
    if F is not None:
        bs = F.BranchSet.from_dict(d)          # validates against F
        text = bs.serialize()
        assert F.BranchSet.load(text) == bs
    else:
        text = json.dumps(d, indent=2, sort_keys=True)
    with open(path, "w") as fh:
        fh.write(text + "\n")
    return d


# ---------------------------------------------------------------------------
# fixtures: explicit generative models, seeded, written as panels
# ---------------------------------------------------------------------------

OPS = {
    "latency_to_approach_novel":
        "seconds from onset of a novel stimulus to first approach within one body length; ceiling at trial end",
    "perseveration_rate":
        "fraction of trials after a rule change on which the previously rewarded response is repeated",
}


def _enclosure(rng, eff, size=None):
    """Build enclosure terms with a given effective_exits count."""
    size = size if size is not None else max(eff + rng.randint(0, 3), 1)
    eff = min(eff, size)
    reach = [1] * eff + [rng.randint(0, 1) for _ in range(size - eff)]
    cost = [round(rng.uniform(0.05, 0.9), 3) for _ in range(eff)] + \
           [round(rng.uniform(1.05, 2.5), 3) if reach[i] else round(rng.uniform(0.1, 2.0), 3)
            for i in range(eff, size)]
    rev = [rng.randint(0, 1) for _ in range(size)]
    return {"option_set_size": size, "exit_cost": cost, "reachability": reach, "reversibility": rev}


def make_fixture(name, seed=0, persons=40, windows=2, trait_sd=0.0, slope=-1.0,
                 noise_sd=1.0, selection=0.0, origin="exogenous", min_delta=1,
                 ops=None, term="latency_to_approach_novel"):
    """behavior = 10 + slope * effective_exits + trait_p + noise.
    selection: correlation between trait and the person's mean exits
    (persons with high trait land in low-exit windows) with within-person
    change unrelated to behavior when slope == 0."""
    rng = random.Random(seed)
    ws = []
    for p in range(persons):
        trait = rng.gauss(0, trait_sd) if trait_sd > 0 else 0.0
        base = rng.randint(1, 5)
        if selection:
            base = max(0, min(6, int(round(3 - selection * trait))))
        effs = [base]
        for _ in range(windows - 1):
            d = rng.choice([-2, -1, 1, 2]) if min_delta else rng.choice([-2, -1, 0, 1, 2])
            effs.append(max(0, min(6, effs[-1] + d)))
        for k, eff in enumerate(effs):
            y = 10.0 + slope * eff + trait + rng.gauss(0, noise_sd)
            ws.append({"person_id": "p%02d" % p, "t0": "2024-%02d" % (k * 3 + 1), "t1": "2024-%02d" % (k * 3 + 3),
                       "change_origin": "baseline" if k == 0 else origin,
                       "enclosure": _enclosure(rng, eff), "behavior": {term: round(y, 3)}})
    return {"population": name, "operationalizations": OPS if ops is None else ops, "windows": ws}


FIXTURES = [
    ("F1_enclosure_only", dict(seed=1, trait_sd=0.0, slope=-1.0)),
    ("F2_trait_only", dict(seed=2, trait_sd=2.0, slope=0.0)),
    ("F3_trait_plus_enclosure", dict(seed=3, trait_sd=2.0, slope=-1.0)),
    ("F4_selection_into_windows", dict(seed=4, trait_sd=2.0, slope=0.0, selection=1.2)),
    ("F5_chosen_change", dict(seed=5, trait_sd=0.0, slope=-1.0, origin="chosen")),
    ("F6_unoperationalized", dict(seed=6, trait_sd=0.0, slope=-1.0, ops={})),
    ("F7_single_windows", dict(seed=7, trait_sd=0.0, slope=-1.0, windows=1)),
]


def demo(out=None, table_literal=False):
    out = out or sys.stdout
    runs = {}
    for name, kw in FIXTURES:
        panel = load_panel(make_fixture(name, **kw))
        runs[name] = run_panel(panel, seed=kw["seed"], table_literal=table_literal, out=out)
        print("", file=out)
    print("summary", file=out)
    for name, run in runs.items():
        for term, rec in run["results"].items():
            print("  %-28s %s" % (name, label(rec["return"])), file=out)
    return runs


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------


def selftest():
    import io
    fails = []

    def check(cond, msg):
        if not cond:
            fails.append(msg)

    # mirror equals G
    if G is not None:
        for name in ("SCORED", "UNKNOWN_MEASURABLE", "BLOCKED", "OUT_OF_ENVELOPE", "VARIABLE_UNIDENT"):
            check(getattr(G.ReturnClass, name).value == getattr(ReturnClass, name),
                  "mirror differs from G on %s" % name)
        # a scored return without a fraction must fail at construction
        try:
            G.CriterionResult(G.ReturnClass.SCORED, value=None)
            check(False, "G accepted SCORED without a value")
        except ValueError:
            pass
    # effective_exits
    enc = {"option_set_size": 4, "exit_cost": [0.2, 1.0, 1.5, 0.3],
           "reachability": [1, 1, 1, 0], "reversibility": [1, 0, 0, 1]}
    check(effective_exits(enc) == 2, "effective_exits counts reachable AND cost<=1.0")
    # OLS exact on a line
    r, beta, _ = ols_residual_fraction([[1.0], [2.0], [3.0]], [2.0, 4.0, 6.0])
    check(abs(r) < 1e-12 and abs(beta[1] - 2.0) < 1e-9, "OLS misses an exact line")
    # constant regressor dropped, not crashed
    r, beta, dropped = ols_residual_fraction([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]], [1.0, 2.0, 3.1])
    check(dropped == [1], "constant regressor not dropped")
    # fixtures land where CLAIM_TABLE says
    buf = io.StringIO()
    runs = demo(out=buf)
    kinds = {name: next(iter(run["results"].values()))["return"]["kind"] for name, run in runs.items()}
    expect = {
        "F1_enclosure_only": (KIND_ENCLOSURE_DOMINANT,),
        "F2_trait_only": (KIND_UNKNOWN,),
        "F3_trait_plus_enclosure": (KIND_TRAIT_RESIDUAL,),
        "F4_selection_into_windows": (KIND_CONFOUND,),
        "F5_chosen_change": (KIND_OUT_OF_ENVELOPE,),
        "F6_unoperationalized": (KIND_BLOCKED,),
        "F7_single_windows": (KIND_BLOCKED,),
    }
    for name, ok in expect.items():
        check(kinds[name] in ok, "%s landed in %s, expected one of %s" % (name, kinds[name], ok))
    text = buf.getvalue()
    # NULL FIRST is printed before the between fit, every term that gets there
    for block in text.split("== ")[1:]:
        if "   between arm  n=" in block:
            check(block.index("NULL FIRST") < block.index("   between arm  n="), "between fit printed before null")
    # F6 blocked with the named blocker, F7 with the other
    check(runs["F6_unoperationalized"]["results"]["latency_to_approach_novel"]["return"]["blocker"] == BLOCK_UNOPERATIONALIZED,
          "F6 blocker name")
    check(runs["F7_single_windows"]["results"]["latency_to_approach_novel"]["return"]["blocker"] == BLOCK_NO_WITHIN,
          "F7 blocker name")
    # closed labels are refused at the schema gate
    p = load_panel({"population": "x", "operationalizations": {"rigidity": "score"},
                    "windows": [{"person_id": "a", "t0": 1, "t1": 2, "change_origin": "baseline",
                                 "enclosure": enc, "behavior": {"rigidity": 3}}]})
    check("rigidity" in schema_gate(p), "closed label not refused")
    # branch set: four branches, round-trips through F when present
    d = branch_set_dict(runs["F1_enclosure_only"])
    check([b["id"] for b in d["branches"]] == ["enclosure_constraint", "trait_plain",
                                                "selection_into_enclosure", "measurement_artifact_of_label_set"],
          "branch ids")
    if F is not None:
        bs = F.BranchSet.from_dict(d)
        check(F.BranchSet.load(bs.serialize()) == bs, "branch set does not round-trip through F")
    # table-literal mode returns TRAIT_RESIDUAL on F1 (the finding EFR_003 records)
    buf2 = io.StringIO()
    p1 = load_panel(make_fixture("F1", **dict(FIXTURES[0][1])))
    lit = run_panel(p1, seed=1, table_literal=True, out=buf2)
    gated = run_panel(p1, seed=1, table_literal=False, out=io.StringIO())
    lk = lit["results"]["latency_to_approach_novel"]["return"]["kind"]
    gk = gated["results"]["latency_to_approach_novel"]["return"]["kind"]
    # EFR_003: under the literal table an enclosure-only panel lands in the
    # confound cell; the corrected reading returns the enclosure account.
    check(lk == KIND_CONFOUND, "F1 literal landed in %s, EFR_003 records the confound cell" % lk)
    check(gk == KIND_ENCLOSURE_DOMINANT, "F1 corrected landed in %s" % gk)
    print("selftest: %s (%d checks failed)  method-layer=%s"
          % ("PASS" if not fails else "FAIL", len(fails), METHOD_LAYER))
    for f in fails:
        print("  - " + f)
    return 0 if not fails else 1


# ---------------------------------------------------------------------------
# cli
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", nargs="?", choices=("demo", "run"))
    ap.add_argument("panel", nargs="?")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--json", action="store_true", help="print the record as JSON after the text")
    ap.add_argument("--emit-branch-set", metavar="PATH", help="write the F branch set, statuses updated by the run")
    ap.add_argument("--table-literal", action="store_true",
                    help="return the order's step-4 table exactly as written (no corrected reading)")
    ap.add_argument("--selftest", action="store_true")
    a, _ = ap.parse_known_args(argv)
    if a.selftest:
        return selftest()
    if a.command == "demo":
        runs = demo(table_literal=a.table_literal)
        if a.emit_branch_set:
            emit_branch_set(a.emit_branch_set, runs["F1_enclosure_only"])
        return 0
    if a.command == "run":
        if not a.panel:
            ap.error("run needs a panel JSON path")
        with open(a.panel) as fh:
            raw = json.load(fh)
        try:
            panel = load_panel(raw)
        except SchemaError as e:
            print("schema error: %s" % e)
            return 2
        run = run_panel(panel, seed=a.seed, table_literal=a.table_literal)
        if a.json:
            print(json.dumps(run, indent=2, sort_keys=True, default=str))
        if a.emit_branch_set:
            emit_branch_set(a.emit_branch_set, run)
            print("branch set -> %s" % a.emit_branch_set)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
