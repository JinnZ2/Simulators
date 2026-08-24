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


def _shadow_outline_area(name):
    """shape-spec-audit/shadow_read.py::outline_area, imported."""
    import importlib.util
    path = os.path.join(ROOT, "shape-spec-audit", "shadow_read.py")
    spec = importlib.util.spec_from_file_location("_shadow_read", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.outline_area(name)


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
