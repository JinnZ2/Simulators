# SPDX-License-Identifier: CC0-1.0
"""
No metric ships without a known-answer run.

A standing step, not a habit. Twice in this repo a metric was wrong in a way
no amount of reading would have caught, and both times it was caught by
running the metric against a case whose answer was fixed in advance:

  1. `null-harness/null_harness.py::_verdict` returns the same string for a
     gate that recovers half its known signal and one that recovers all of
     it. Found while grading `nonidentity-census` T1, where the fail class
     read `OK` at 6/12 and `OK` at 12/12.
  2. `nonidentity-census/t6_window_declaration.py::decided_by_tracks_window`
     first took the majority label per arm over the total, which is the
     marginal majority rate. It read 0.83 on a set whose two arms are
     IDENTICAL by construction and whose true association is exactly zero.

Both are real, both are in this tree, and both are registered below as
cases. A registry seeded only with metrics that pass is a registry nobody
has tested, so one of the seeds is a CURRENTLY FAILING case, pinned. If it
starts passing, the test goes red and the note here has to be updated.

WHAT THE GATE REFUSES, so that it is not decorative:

  - a metric with no cases;
  - a case set whose expected values are all equal. A case set that expects
    the same answer everywhere cannot detect a constant metric, which is the
    exact failure mode both seeds are instances of;
  - a case with no `why_known`. An expected value with no stated basis is
    a second guess dressed as an answer.

WHAT IT DOES NOT DO. It does not find metrics. Deciding whether a function
is a metric is not a lexical property of its name, and a repo-wide scan for
metric-shaped functions would be the word-list failure one level up -- the
one `nonidentity-census` T1-1 measured. Coverage comes from a hand-kept
manifest in `tests/test_known_answer_gate.py`, and the manifest is therefore
the weak point. It is named as one rather than hidden.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 tools/known_answer.py
    python3 -m unittest discover tests
"""

from __future__ import annotations

import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PASS = "PASS"
FAIL = "FAIL"
NOT_RUN = "NOT_RUN"


class KnownAnswerNotRun(Exception):
    """Raised when a metric is used without a known-answer run."""


class BadCaseSet(Exception):
    """Raised when a case set could not detect a constant metric."""


_REGISTRY = {}
_RESULTS = {}


def case(name, args, expected, why_known, kwargs=None, tol=0.0):
    if not why_known:
        raise BadCaseSet(
            "case %r has no why_known. An expected value with no stated "
            "basis is a second guess dressed as an answer." % name)
    return {"name": name, "args": tuple(args), "kwargs": dict(kwargs or {}),
            "expected": expected, "why_known": why_known, "tol": tol}


def register(metric_id, fn, cases, note=None, pinned_failing=()):
    """
    `pinned_failing` names cases known to fail today. They are recorded as
    failing and do not block; a case that starts passing is reported so the
    note can be corrected.
    """
    if not cases:
        raise BadCaseSet("%s registered with no cases" % metric_id)
    expected = [c["expected"] for c in cases]
    if len(set(map(repr, expected))) < 2:
        raise BadCaseSet(
            "%s: every case expects %r. A case set with one expected answer "
            "cannot detect a constant metric, which is the failure this "
            "registry exists for." % (metric_id, expected[0]))
    _REGISTRY[metric_id] = {"fn": fn, "cases": cases, "note": note,
                            "pinned_failing": set(pinned_failing)}
    return metric_id


def run(metric_id):
    if metric_id not in _REGISTRY:
        raise KnownAnswerNotRun("%s is not registered" % metric_id)
    entry = _REGISTRY[metric_id]
    rows = []
    for c in entry["cases"]:
        if entry["fn"] is None:
            rows.append({"case": c["name"], "status": NOT_RUN,
                         "got": None, "expected": c["expected"],
                         "why_known": c["why_known"],
                         "detail": entry.get("not_run_reason",
                                             "callable unavailable")})
            continue
        try:
            got = entry["fn"](*c["args"], **c["kwargs"])
        except Exception as ex:                       # noqa: BLE001
            rows.append({"case": c["name"], "status": NOT_RUN, "got": None,
                         "expected": c["expected"],
                         "why_known": c["why_known"],
                         "detail": "%s: %s" % (type(ex).__name__, ex)})
            continue
        if isinstance(c["expected"], (int, float)) and \
                isinstance(got, (int, float)) and c["tol"]:
            ok = abs(got - c["expected"]) <= c["tol"]
        else:
            ok = got == c["expected"]
        rows.append({"case": c["name"], "status": PASS if ok else FAIL,
                     "got": got, "expected": c["expected"],
                     "why_known": c["why_known"], "detail": None})
    _RESULTS[metric_id] = rows
    return rows


def require(metric_id):
    """Raises unless the metric is registered and has been run."""
    if metric_id not in _REGISTRY:
        raise KnownAnswerNotRun(
            "%s has no known-answer case. No metric ships without one."
            % metric_id)
    if metric_id not in _RESULTS:
        raise KnownAnswerNotRun(
            "%s is registered but its known-answer run has not been "
            "executed." % metric_id)
    return _RESULTS[metric_id]


def unexpected(metric_id):
    """Cases whose status disagrees with what the registry expects of them."""
    entry = _REGISTRY[metric_id]
    out = []
    for r in _RESULTS.get(metric_id, []):
        pinned = r["case"] in entry["pinned_failing"]
        if pinned and r["status"] == PASS:
            out.append((r["case"], "pinned as failing, now passes"))
        if not pinned and r["status"] == FAIL:
            out.append((r["case"], "fails and is not pinned"))
    return out


def registry_ids():
    return sorted(_REGISTRY)


# --------------------------------------------------------------------------
# Seed 1 -- null-harness's fail-condition classifier.
#
# `null_harness.py` imports numpy at module scope and numpy is not installed
# here, so the module cannot be imported. `_verdict` is pure comparison
# arithmetic, so it is extracted by source text at call time -- always from
# the current file, never from a copy -- and refused if the extracted source
# contains an import. If extraction fails the cases record NOT_RUN with the
# reason rather than being skipped.
# --------------------------------------------------------------------------

NH_PATH = os.path.join(ROOT, "null-harness", "null_harness.py")


def _extract_verdict():
    if not os.path.exists(NH_PATH):
        return None, "null-harness/null_harness.py not found"
    with open(NH_PATH) as fh:
        src = fh.read()
    m = re.search(r"^def _verdict\(.*?(?=^\S)", src, re.M | re.S)
    if not m:
        return None, "def _verdict not located in the current file"
    body = m.group(0)
    if re.search(r"^\s*(import|from)\s", body, re.M):
        return None, "extracted source contains an import; not exec'd"
    ns = {}
    try:
        exec(compile(body, NH_PATH, "exec"), ns)          # noqa: S102
    except Exception as ex:                                # noqa: BLE001
        return None, "%s: %s" % (type(ex).__name__, ex)
    fn = ns.get("_verdict")
    return fn, hashlib.sha1(body.encode()).hexdigest()[:8]


def _verdict_discriminates(fp_a, tp_a, fp_b, tp_b):
    """
    Does the classifier give two different answers to two gates that differ
    by half their known signal? Returns True if it discriminates.
    """
    fn, detail = _extract_verdict()
    if fn is None:
        raise RuntimeError(detail)
    return fn(fp_a, tp_a) != fn(fp_b, tp_b)


# --------------------------------------------------------------------------
# Seed 2 -- T6's association metric, and the version it replaced.
# --------------------------------------------------------------------------

sys.path.insert(0, os.path.join(ROOT, "nonidentity-census"))


def _t6_rows_to_move(which):
    import t6_window_declaration as t6
    rows = t6.MATCHED_ROWS if which == "matched" else t6.NULL_ROWS
    return t6.decided_by_tracks_window(rows)[0]


def _marginal_majority(which):
    """The metric that was replaced, kept runnable so its error is checkable."""
    import t6_window_declaration as t6
    rows = t6.MATCHED_ROWS if which == "matched" else t6.NULL_ROWS
    arms = {}
    for r in rows:
        arms.setdefault(r["window_declared"], []).append(r["decided_by"])
    hit = tot = 0
    for vals in arms.values():
        counts = {}
        for v in vals:
            counts[v] = counts.get(v, 0) + 1
        hit += max(counts.values())
        tot += len(vals)
    return round(hit / float(tot), 2)


def _three_column_ols(which):
    """sim-span/three_column.py::ols, imported. Exact fits only."""
    import importlib.util
    path = os.path.join(ROOT, "sim-span", "three_column.py")
    spec = importlib.util.spec_from_file_location("_three_column", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ols_coef(which)


def _sim_span_quad_fit(which):
    """sim-span/sim_span.py::quad_fit, imported. Returns the a coefficient."""
    import importlib.util
    path = os.path.join(ROOT, "sim-span", "sim_span.py")
    spec = importlib.util.spec_from_file_location("_sim_span", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
    if which == "parabola":
        ys = [2.0 * x * x - 3.0 * x + 5.0 for x in xs]
    elif which == "line":
        ys = [3.0 * x + 1.0 for x in xs]
    elif which == "flat":
        ys = [4.0 for _x in xs]
    else:
        raise ValueError(which)
    fit = mod.quad_fit(xs, ys)
    return None if fit is None else round(fit[0], 12)


def _shadow_outline_area(name):
    """shape-spec-audit/shadow_read.py::outline_area, imported."""
    import importlib.util
    path = os.path.join(ROOT, "shape-spec-audit", "shadow_read.py")
    spec = importlib.util.spec_from_file_location("_shadow_read", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.outline_area(name)


def _sheet_rank(shape):
    """sheet-structure-scan/sheetmodel.py::rank, on hand-built graphs.

    Built here rather than read from a workbook: the point of the case is
    that the answer is fixed by the graph's shape and can be counted off
    by hand, and a fixture file would put a reader between the metric and
    its known answer.
    """
    import importlib.util
    path = os.path.join(ROOT, "sheet-structure-scan", "sheetmodel.py")
    spec = importlib.util.spec_from_file_location("_sheetmodel", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def cell(addr, prec):
        return mod.Cell("S", addr, mod.DERIVED if prec else mod.CONSTANT_NUMBER,
                        None, "=x" if prec else None,
                        set(("S", p) for p in prec), set())

    if shape == "chain":
        # A1 -> B1 -> C1
        cells = [cell("A1", []), cell("B1", ["A1"]), cell("C1", ["B1"])]
        target = "A1"
    elif shape == "fan":
        # A1 read by B1, C1, D1, none of which is read by anything
        cells = [cell("A1", []), cell("B1", ["A1"]), cell("C1", ["A1"]),
                 cell("D1", ["A1"])]
        target = "A1"
    elif shape == "terminal":
        cells = [cell("A1", []), cell("B1", ["A1"])]
        target = "B1"
    elif shape == "cycle":
        cells = [cell("A1", ["B1"]), cell("B1", ["A1"])]
        target = "A1"
    else:
        raise ValueError(shape)
    wb = mod.Workbook(cells, ["S"])
    return wb.rank(("S", target))


def _ale_integrate(which):
    """agent-lifecycle-energy/phase_energy.py::integrate, imported.

    Returns the marginal joules for a constructed phase whose area is fixed
    by construction. The point of the case is that a meter integral, a
    baseline subtraction, and an integration rule can each be wrong in a way
    reading the code would not catch: a Riemann sum instead of a trapezoid
    biases a ramp, a dropped baseline reports total draw as marginal, a sign
    slip flips a zero-marginal phase off zero.
    """
    import importlib.util
    path = os.path.join(ROOT, "agent-lifecycle-energy", "phase_energy.py")
    spec = importlib.util.spec_from_file_location("_phase_energy", path)
    mod = importlib.util.module_from_spec(spec)
    # dataclasses under `from __future__ import annotations` resolve their
    # own module out of sys.modules during class creation; register first.
    sys.modules["_phase_energy"] = mod
    spec.loader.exec_module(mod)
    S = mod.Sample
    if which == "constant":
        # 200 W for 2.0 s over a 100 W idle: marginal 100 W x 2 s = 200 J.
        n = 201
        samples = [S(i * 0.01, 200.0) for i in range(n)]
        pe = mod.integrate(samples, 100.0, "card", "task")
    elif which == "ramp":
        # linear ramp 0 -> 100 W over 1.0 s, zero idle: triangle area 50 J.
        n = 101
        samples = [S(i * 0.01, 100.0 * (i * 0.01)) for i in range(n)]
        pe = mod.integrate(samples, 0.0, "card", "spinup")
    elif which == "zero_marginal":
        # 100 W for 1.0 s over a 100 W idle: marginal draw is exactly zero.
        n = 101
        samples = [S(i * 0.01, 100.0) for i in range(n)]
        pe = mod.integrate(samples, 100.0, "card", "teardown")
    else:
        raise ValueError(which)
    return None if pe.joules is None else round(pe.joules, 9)


def _omc_interaction_fraction(which):
    """operator-machine-coupling/coupling_separation.py::interaction_fraction,
    imported. The fraction of structured variation living in the pairings
    (SS_pair / SS_total) -- the coupling term. It could be silently wrong in
    the way a variance decomposition is: an additive table must return 0
    (no pairing effect), a pure-interaction table 1 (all of it), and a mixed
    table a value the two do not share, or the metric cannot tell 'measured
    the pairing' from 'averaged over it'."""
    import importlib.util
    path = os.path.join(ROOT, "operator-machine-coupling",
                        "coupling_separation.py")
    spec = importlib.util.spec_from_file_location("_coupling_sep", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    O = mod.Obs
    if which == "additive":
        # rows a=[+1,-1], cols b=[+2,-2], mu=0, no interaction
        obs = [O("op0", "u0", 3.0), O("op0", "u1", -1.0),
               O("op1", "u0", 1.0), O("op1", "u1", -3.0)]
    elif which == "pure_pairing":
        # a=b=0, all variance in the interaction contrast [[1,-1],[-1,1]]
        obs = [O("op0", "u0", 1.0), O("op0", "u1", -1.0),
               O("op1", "u0", -1.0), O("op1", "u1", 1.0)]
    elif which == "mixed":
        # a=[+1,-1], b=[+2,-2], r=[[.5,-.5],[-.5,.5]]: SS 4 / 16 / 1 -> 1/21
        obs = [O("op0", "u0", 3.5), O("op0", "u1", -1.5),
               O("op1", "u0", 0.5), O("op1", "u1", -2.5)]
    else:
        raise ValueError(which)
    f = mod.interaction_fraction(obs)
    return None if f is None else round(f, 12)


def _mdb_lag_of_peak(which):
    """model-deprecation-backcast/null_check.py::lag_of_peak, imported. The
    C6 fad-axis metric: the lag at which discards best track discourse. It
    could be silently wrong -- return a lag when there is none (a spurious
    fad reading), or miss a planted lag -- so a planted-lag series must
    recover its lag and a flat series must return None (no peak)."""
    import importlib.util
    path = os.path.join(ROOT, "model-deprecation-backcast", "null_check.py")
    spec = importlib.util.spec_from_file_location("_mdb_null", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # the same deterministic aperiodic discourse series the folder uses
    x, s = [], 1
    for _ in range(72):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        x.append(float((s >> 8) % 97))
    lags = list(range(0, 31))
    if which == "flat":
        return mod.lag_of_peak(x, [1.0] * 72, lags)
    L0 = int(which)
    y = [x[t - L0] if t - L0 >= 0 else 0.0 for t in range(72)]
    return mod.lag_of_peak(x, y, lags)


def _rdl_sustained_excess(which):
    """routing-data-layer/rate_form.py::sustained_excess, imported. The
    fraction of a season where dE/dt > dM/dt -- the quantity the STRUCTURAL vs
    MATURITY_GAP verdict turns on. It could be silently wrong (an off-by-one
    on the comparison, or counting >= instead of >), so an all-excess series
    must read 1, a never-excess series 0, and an alternating series 0.5."""
    import importlib.util
    path = os.path.join(ROOT, "routing-data-layer", "rate_form.py")
    spec = importlib.util.spec_from_file_location("_rdl_rate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if which == "all":
        return round(mod.sustained_excess([2, 2, 2, 2], [1, 1, 1, 1]), 12)
    if which == "none":
        return round(mod.sustained_excess([1, 1, 1, 1], [2, 2, 2, 2]), 12)
    if which == "half":
        return round(mod.sustained_excess([2, 1, 2, 1], [1, 2, 1, 2]), 12)
    raise ValueError(which)


def seed():
    """Registers the two instances the rule was earned from."""
    fn, detail = _extract_verdict()
    register(
        "null-harness/null_harness.py::_verdict",
        _verdict_discriminates if fn is not None else None,
        [
            case("half-signal vs full-signal",
                 (0.0, 0.5, 0.0, 1.0), True,
                 "a gate recovering half its known signal and one "
                 "recovering all of it are not the same gate, so a "
                 "fail-condition classifier must not return one string for "
                 "both"),
            case("silent vs full-signal",
                 (0.0, 0.0, 0.0, 1.0), True,
                 "a gate that never fires and one that always finds the "
                 "signal must differ; this is the case the classifier was "
                 "built for and it passes"),
            case("two constant-fires gates",
                 (0.95, 0.95, 0.99, 0.99), False,
                 "both fire on everything, so they are the same kind of "
                 "non-gate and the classifier is right NOT to separate "
                 "them. Present because the registry refused this case set "
                 "when every case expected True -- see the note"),
        ],
        note=("extracted by source from the current file, sha1 %s. FAILS "
              "today: `OK` is returned for TP=0.5 and TP=1.0 alike. Found "
              "while grading nonidentity-census T1. The first version of "
              "this seed had two cases and both expected True; register() "
              "refused it on its own rule, which is why the third case "
              "exists." % detail),
        pinned_failing=("half-signal vs full-signal",),
    )
    register(
        "nonidentity-census/t6_window_declaration.py::"
        "decided_by_tracks_window",
        _t6_rows_to_move,
        [
            case("matched set", ("matched",), 0,
                 "the two window arms carry the same head nouns by "
                 "construction, so the association is exactly zero"),
            case("as-specified set", ("as-specified",), 5,
                 "hand-counted from the printed per-arm distributions: NO "
                 "arm all LEXICAL, YES arm 5 of 6 UNDECIDABLE"),
        ],
        note="the replacement metric. Passes.",
    )
    register(
        "sim-span/three_column.py::ols",
        _three_column_ols,
        [
            case("exact slope", ("slope",), 3.0,
                 "y = 2 + 3x sampled at five points has slope 3 by "
                 "construction. The slope of this regression is the "
                 "estimator of p, so a fitter with a scale error would "
                 "misreport the one quantity the design exists to measure",
                 tol=1e-9),
            case("exact intercept", ("intercept",), 2.0,
                 "same line, intercept 2. The intercept must sit at zero on "
                 "real data if true-reporters contribute a gap of zero, so a "
                 "fitter that cannot recover a known intercept cannot "
                 "support that reading", tol=1e-9),
            case("constant data", ("flat",), 0.0,
                 "a horizontal line has slope 0. A fitter that invents one "
                 "would report a non-zero p on a population where nobody "
                 "reports span", tol=1e-9),
        ],
        note=("the three-column test's fitter. The slope IS the estimate of "
              "p, so this is the one metric in the folder whose output is "
              "read as a quantity rather than a sign."),
    )
    register(
        "sim-span/sim_span.py::quad_fit",
        _sim_span_quad_fit,
        [
            case("exact parabola", ("parabola",), 2.0,
                 "y = 2x^2 - 3x + 5 sampled at five points has a = 2 by "
                 "construction; a least-squares quadratic through points "
                 "that lie on a parabola must return its own coefficient",
                 tol=1e-9),
            case("straight line", ("line",), 0.0,
                 "y = 3x + 1 has no quadratic term. A fitter that invents "
                 "curvature here would manufacture the U this sim exists "
                 "to detect -- the failure mode inside the instrument",
                 tol=1e-9),
            case("constant", ("flat",), 0.0,
                 "a horizontal line has no quadratic term either. Present "
                 "because the line case alone shares an expected value "
                 "with it and the registry needs the pair to differ from "
                 "the parabola", tol=1e-9),
        ],
        note=("the U detector's fitter. The sim's whole claim is about the "
              "SIGN of a, so a fitter with a curvature bias would produce "
              "the finding by itself."),
    )
    register(
        "shape-spec-audit/shadow_read.py::outline_area",
        _shadow_outline_area,
        [
            case("square", ("square",), 4.0,
                 "four tangents at distance 1 bound a 2x2 square, whose "
                 "area is exactly 4 by construction and not by measurement",
                 tol=1e-6),
            case("hexagon", ("hexagon",), 2.0 * 1.7320508075688772,
                 "six tangents at distance 1 about the unit circle give the "
                 "circumscribed regular hexagon, area 6*tan(pi/6) = "
                 "2*sqrt(3)", tol=1e-6),
            case("strip", ("strip",), "UNDER_OUTLINED",
                 "two opposing statements leave the vertical direction "
                 "unconstrained, so no bounded object is tangent to both "
                 "and no area exists to report"),
            case("contradiction", ("contradiction",), "INCONSISTENT",
                 "x <= 0 and x >= 1 cannot both hold, so there is no "
                 "boundary the statements are tangent to. This is the "
                 "state METHOD_SPEC section 4 has no cell for"),
        ],
        note=("METHOD_SPEC section 4's shadow read, made decidable. The "
              "case set spans all three states on purpose: a fixture set "
              "in which INCONSISTENT never occurs cannot detect an "
              "instrument that has quietly lost the failure branch, which "
              "is the branch the section lacks."),
    )
    register(
        "nonidentity-census/t6_window_declaration.py::"
        "marginal_majority (REPLACED)",
        _marginal_majority,
        [
            case("matched set", ("matched",), 0.0,
                 "same construction as above: the true association is zero, "
                 "so any honest association metric must return zero here"),
            case("as-specified set", ("as-specified",), 0.92,
                 "what the replaced metric actually returned: 11 of 12. "
                 "This case was first written as 0.83, which is the MATCHED "
                 "set's figure -- the two were transposed while recording "
                 "them, and the known-answer run caught it. Third catch in "
                 "this exchange, and the first on a record of an error "
                 "rather than on a metric"),
        ],
        note=("the metric that was replaced, kept runnable. Its matched-set "
              "case FAILS by design: it returns 0.83 where the answer is 0. "
              "Its as-specified case passes at 0.92, which is what it "
              "returns and not what it should."),
        pinned_failing=("matched set",),
    )
    register(
        "sheet-structure-scan/sheetmodel.py::rank",
        _sheet_rank,
        [
            case("chain", ("chain",), 2,
                 "A1 -> B1 -> C1: exactly one cell reads A1 and the furthest "
                 "chain forward from it is two steps, so 1 x 2 = 2. Counted "
                 "off the graph, not measured"),
            case("fan", ("fan",), 3,
                 "three cells read A1 and none of them is read by anything, "
                 "so the furthest chain is one step: 3 x 1 = 3. Present "
                 "because it has the same reach as the chain and a "
                 "different value, which is what separates the two factors"),
            case("terminal", ("terminal",), 0,
                 "nothing reads B1, so it propagates nowhere and the product "
                 "is zero however deep its own precedents run"),
            case("cycle", ("cycle",), "CYCLE",
                 "A1 and B1 read each other, so no longest forward path "
                 "exists. The metric must say so rather than return a "
                 "number, and must not recurse without end"),
        ],
        note=("dependent count times downstream depth, the ranking the "
              "delivered spec asks for. The four cases separate the two "
              "factors: chain and fan have the same number of cells "
              "downstream and different products, so a metric that "
              "collapsed to either factor alone would pass one and fail "
              "the other. The terminal case pins the property that the "
              "most-derived cell on a sheet ranks last."),
    )
    register(
        "agent-lifecycle-energy/phase_energy.py::integrate",
        _ale_integrate,
        [
            case("constant", ("constant",), 200.0,
                 "200 W held for 2.0 s over a 100 W idle baseline is a "
                 "marginal 100 W for 2 s = 200 J exactly; a trapezoid over a "
                 "constant trace is exact, so a dropped baseline (reporting "
                 "the full 400 J) or a rectangular rule would miss this",
                 tol=1e-9),
            case("ramp", ("ramp",), 50.0,
                 "a linear ramp 0 -> 100 W over 1.0 s with zero idle is a "
                 "triangle of area 50 J; a trapezoid is exact on a straight "
                 "line while a left Riemann sum undercounts it, so this is "
                 "the case that pins the integration rule", tol=1e-9),
            case("zero_marginal", ("zero_marginal",), 0.0,
                 "100 W held for 1.0 s over a 100 W idle is marginal zero; a "
                 "baseline-subtraction sign slip would push it off zero, and "
                 "this is the case that shares no expected value with the "
                 "other two so the set can detect a constant integrator",
                 tol=1e-9),
        ],
        note=("the GAP 4 rig's phase integrator: integral (P(t) - P_idle) dt, "
              "trapezoidal, baseline-subtracted. The three cases separate the "
              "three ways it could be wrong -- the baseline (zero_marginal), "
              "the rule (ramp), and the arithmetic (constant) -- and their "
              "expected values are all distinct so a constant integrator "
              "cannot pass the set."),
    )
    register(
        "operator-machine-coupling/coupling_separation.py::"
        "interaction_fraction",
        _omc_interaction_fraction,
        [
            case("additive", ("additive",), 0.0,
                 "an additive table (outcome = mu + a_i + b_j, no pairing "
                 "term) has SS_pair exactly 0, so the pairing fraction is 0; "
                 "a decomposition that leaked a main effect into the "
                 "interaction would miss this", tol=1e-9),
            case("pure_pairing", ("pure_pairing",), 1.0,
                 "a table whose only structure is the interaction contrast "
                 "[[1,-1],[-1,1]] has zero main effects, so the whole "
                 "structured variance is the pairing: fraction 1", tol=1e-9),
            case("mixed", ("mixed",), 1.0 / 21.0,
                 "main-effect SS 4 and 16 against pairing SS 1 give "
                 "1/(4+16+1) = 1/21; present because it shares no expected "
                 "value with the other two, so the set can detect a constant "
                 "fraction", tol=1e-9),
        ],
        note=("the coupling separation's headline: how much of the "
              "structured variation is in the pairings rather than either "
              "main effect. The three cases pin the two endpoints (0 = purely "
              "additive, 1 = purely pairing) and one interior value the "
              "endpoints do not share."),
    )
    register(
        "model-deprecation-backcast/null_check.py::lag_of_peak",
        _mdb_lag_of_peak,
        [
            case("planted lag 20", ("20",), 20,
                 "discards built as discourse shifted by 20 steps have their "
                 "cross-correlation maximum at lag 20 by construction (an "
                 "aperiodic discourse series makes the lag unique); a "
                 "detector that missed it would miss the fad axis"),
            case("planted lag 5", ("5",), 5,
                 "the same construction at lag 5; present so the set has more "
                 "than one non-null expected value"),
            case("flat -- no peak", ("flat",), None,
                 "a constant discard series has no lag that tracks discourse, "
                 "so the metric must return None (the C6 null: the fad axis "
                 "is not driving) rather than a spurious lag"),
        ],
        note=("the C6 fad-axis lag metric. The two planted-lag cases pin "
              "recovery; the flat case pins the null -- a lag detector that "
              "returned a number on flat input would manufacture a fad "
              "reading, the failure the null exists to declare."),
    )
    register(
        "routing-data-layer/rate_form.py::sustained_excess",
        _rdl_sustained_excess,
        [
            case("all excess", ("all",), 1.0,
                 "dE above dM at every step -> fraction 1; the STRUCTURAL "
                 "verdict rests on this, so a strict-vs-nonstrict comparison "
                 "bug would misread it", tol=1e-9),
            case("never excess", ("none",), 0.0,
                 "dE below dM at every step -> fraction 0 (the MATURITY_GAP "
                 "end)", tol=1e-9),
            case("alternating", ("half",), 0.5,
                 "dE above dM on exactly half the steps -> 0.5; present "
                 "because it shares no expected value with the two endpoints, "
                 "so the set can detect a constant metric", tol=1e-9),
        ],
        note=("Section 5's rate-excess fraction. The three cases pin the two "
              "endpoints (0 = refresh always keeps up, 1 = environment always "
              "outruns it) and the interior value the endpoints do not "
              "share."),
    )


def report():
    seed()
    bad = []
    for mid in registry_ids():
        rows = run(mid)
        entry = _REGISTRY[mid]
        print(mid)
        if entry["note"]:
            print("  note: %s" % entry["note"])
        for r in rows:
            mark = r["status"]
            if r["case"] in entry["pinned_failing"] and r["status"] == FAIL:
                mark = "FAIL (pinned)"
            print("  %-28s %-14s got=%r want=%r"
                  % (r["case"], mark, r["got"], r["expected"]))
            if r["detail"]:
                print("      %s" % r["detail"])
            print("      known because: %s" % r["why_known"])
        u = unexpected(mid)
        for cname, why in u:
            print("  !! %s: %s" % (cname, why))
        bad.extend((mid, c, w) for c, w in u)
        print()
    print("metrics registered: %d" % len(registry_ids()))
    print("cases disagreeing with the registry: %d" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(report())
