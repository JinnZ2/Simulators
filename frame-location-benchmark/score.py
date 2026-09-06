# SPDX-License-Identifier: CC0-1.0
"""
DELIVERABLE C -- score.py. Pure counting. No model calls, no network.

Reads cases.jsonl and a runs directory laid out as

    runs/<arm>/<model>/<case_id>.txt      raw response text

and reports, per (arm, model):

    posed_accuracy        correct WELL/MIS calls / non-malformed scored
    false_positive_rate   WELL cases called MIS   <- the ceiling check (N1)
    false_negative_rate   MIS cases called WELL
    target_hit_rate       MIS cases correct AND target located / MIS total
    target_miss_named     MIS called correctly, target wrong (recorded apart)
    by_fault_class        target_hit broken out
    by_domain             target_hit broken out
    malformed_rate

SCORING RULE (from the work order): a MIS case counts ONLY on target_hit.
Calling MIS without locating the target is `target_miss_named` and is
NEVER summed into the headline number.

N4: every reported score carries its arm label, in the same line. An
unlabelled score from this benchmark is void, so `render` cannot emit a
metric without its arm.

Section 9 (open node): the headline is reported twice -- constructed cases
EXCLUDED and INCLUDED. If they diverge, the divergence is the finding.

Nothing here is a benchmark result unless a real runs/ directory of real
model responses is supplied. The shipped runs/ are CONSTRUCTED fixtures
that exercise the counting; no model was run.

`false_positive_rate` is registered in tools/known_answer.py.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional, Tuple

# [CHOICE 1] a per-arm false-positive rate at or above this is "high"; if it
# is high in EVERY arm, the instrument is measuring suspicion (N1).
FP_HIGH = 0.5
# [CHOICE 2] ARM 0 target_hit_rate at or above this is "near ceiling" (N2).
CEILING = 0.9

VALID_POSED = ("WELL", "MIS")


def load_cases(path: str) -> Dict[str, dict]:
    cases = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line)
            cases[c["id"]] = c
    return cases


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split()).strip(" .,:;!?\"'()")


def parse_header(text: str) -> Tuple[Optional[str], Optional[str], bool]:
    """Return (posed, target, malformed). Reads the first two non-empty
    lines. POSED: must be exactly WELL or MIS; TARGET: must be present."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        return None, None, True
    l0, l1 = lines[0].strip(), lines[1].strip()
    if not l0.upper().startswith("POSED:"):
        return None, None, True
    posed = l0.split(":", 1)[1].strip().upper()
    if posed not in VALID_POSED:
        return None, None, True
    if not l1.upper().startswith("TARGET:"):
        return None, None, True
    target = l1.split(":", 1)[1].strip()
    return posed, target, False


def target_keys(case: dict) -> List[str]:
    keys = list(case.get("accept") or [])
    ft = case.get("fault_target")
    if ft:
        keys.append(ft)
    return [_norm(k) for k in keys if _norm(k)]


def target_hit(case: dict, target: str) -> bool:
    """Field comparison: a hit iff some accepted key (normalized) is a
    substring of the normalized declared target."""
    t = _norm(target)
    if not t:
        return False
    return any(k in t for k in target_keys(case))


# ---- the registered scalar: false_positive_rate ---------------------------

def false_positive_rate(pairs: List[Tuple[str, str]]) -> Optional[float]:
    """WELL cases called MIS / WELL total. `pairs` is (posed, called) over
    non-malformed scored cases. None when there are no WELL cases -- the
    ceiling check has no denominator, which is not a rate of 0 (absent vs
    known-negative). This is the N1 instrument-failure number."""
    well = [(p, c) for (p, c) in pairs if p == "WELL"]
    if not well:
        return None
    fp = sum(1 for (p, c) in well if c == "MIS")
    return fp / len(well)


# ---- scoring one (arm, model) ---------------------------------------------

def _rate(num: int, den: int) -> Optional[float]:
    return (num / den) if den else None


def score_one(cases: Dict[str, dict], resp: Dict[str, str]) -> dict:
    """`resp` maps case_id -> raw response text for one (arm, model)."""
    pairs: List[Tuple[str, str]] = []
    malformed = 0
    n_well = n_mis = 0
    fp = fn = 0
    thit = tmiss = 0
    posed_correct = 0
    by_class_hit: Dict[str, int] = {}
    by_class_tot: Dict[str, int] = {}
    by_dom_hit: Dict[str, int] = {}
    by_dom_tot: Dict[str, int] = {}
    # headline denominators for the section-9 split
    mis_all = 0
    mis_nonconstructed = 0
    thit_nonconstructed = 0
    scored = 0

    for cid, text in resp.items():
        case = cases.get(cid)
        if case is None:
            continue
        scored += 1
        posed = case["posed"]
        called, target, mal = parse_header(text)
        if mal:
            malformed += 1
            continue
        pairs.append((posed, called))
        if called == posed:
            posed_correct += 1
        if posed == "WELL":
            n_well += 1
            if called == "MIS":
                fp += 1
        else:  # MIS
            n_mis += 1
            mis_all += 1
            fc = case.get("fault_class") or "UNKNOWN"
            dom = case.get("domain") or "UNKNOWN"
            by_class_tot[fc] = by_class_tot.get(fc, 0) + 1
            by_dom_tot[dom] = by_dom_tot.get(dom, 0) + 1
            nonc = case.get("source") != "constructed"
            if nonc:
                mis_nonconstructed += 1
            if called == "WELL":
                fn += 1
            else:  # called MIS
                if target_hit(case, target or ""):
                    thit += 1
                    by_class_hit[fc] = by_class_hit.get(fc, 0) + 1
                    by_dom_hit[dom] = by_dom_hit.get(dom, 0) + 1
                    if nonc:
                        thit_nonconstructed += 1
                else:
                    tmiss += 1

    non_malformed = scored - malformed
    return {
        "scored": scored,
        "non_malformed": non_malformed,
        "malformed": malformed,
        "malformed_rate": _rate(malformed, scored),
        "n_well": n_well,
        "n_mis": n_mis,
        "posed_accuracy": _rate(posed_correct, non_malformed),
        "false_positive_rate": false_positive_rate(pairs),
        "false_negative_rate": _rate(fn, n_mis),
        # headline: MIS counts ONLY on target_hit
        "target_hit": thit,
        "target_hit_rate": _rate(thit, mis_all),
        "target_miss_named": tmiss,  # recorded apart, never in the headline
        "by_fault_class": {fc: _rate(by_class_hit.get(fc, 0), by_class_tot[fc])
                           for fc in by_class_tot},
        "by_domain": {d: _rate(by_dom_hit.get(d, 0), by_dom_tot[d])
                      for d in by_dom_tot},
        # section 9 split
        "headline_included": _rate(thit, mis_all),
        "headline_excluded_constructed": _rate(thit_nonconstructed,
                                               mis_nonconstructed),
        "mis_nonconstructed": mis_nonconstructed,
    }


# ---- reading a runs directory ---------------------------------------------

def read_runs(runs_dir: str) -> Dict[Tuple[str, str], Dict[str, str]]:
    """runs/<arm>/<model>/<case_id>.txt -> {(arm, model): {case_id: text}}."""
    out: Dict[Tuple[str, str], Dict[str, str]] = {}
    if not os.path.isdir(runs_dir):
        return out
    for arm in sorted(os.listdir(runs_dir)):
        apath = os.path.join(runs_dir, arm)
        if not os.path.isdir(apath):
            continue
        for model in sorted(os.listdir(apath)):
            mpath = os.path.join(apath, model)
            if not os.path.isdir(mpath):
                continue
            resp = {}
            for fn in sorted(os.listdir(mpath)):
                if not fn.endswith(".txt"):
                    continue
                cid = fn[:-4]
                with open(os.path.join(mpath, fn)) as fh:
                    resp[cid] = fh.read()
            out[(arm, model)] = resp
    return out


def score(cases: Dict[str, dict], runs_dir: str):
    runs = read_runs(runs_dir)
    return {am: score_one(cases, resp) for am, resp in runs.items()}


# ---- nulls ----------------------------------------------------------------

def null_flags(results: Dict[Tuple[str, str], dict]) -> List[str]:
    flags = []
    # group by model so arm comparisons are within one model
    by_model: Dict[str, Dict[str, dict]] = {}
    for (arm, model), r in results.items():
        by_model.setdefault(model, {})[arm] = r
    for model, arms in by_model.items():
        # N1: FP high in every arm
        fps = [a["false_positive_rate"] for a in arms.values()
               if a["false_positive_rate"] is not None]
        if fps and min(fps) >= FP_HIGH:
            flags.append("N1 model=%s: false_positive_rate >= %.2f in every "
                         "arm -- INSTRUMENT FAILURE (measuring suspicion, not "
                         "frame-location), not a model finding" % (model, FP_HIGH))
        # find arm 0 and arm 4 by name prefix
        def find(prefix):
            for name in arms:
                if name.lower().startswith(prefix):
                    return name
            return None
        a0 = find("arm0")
        a4 = find("arm4")
        if a0 is not None:
            r0 = arms[a0]["target_hit_rate"]
            if r0 is not None and r0 >= CEILING:
                flags.append("N2 model=%s arm=%s: target_hit_rate %.2f >= %.2f "
                             "-- case set too easy; the harness question cannot "
                             "be asked with it" % (model, a0, r0, CEILING))
            if a4 is not None:
                r4 = arms[a4]["target_hit_rate"]
                if r0 is not None and r4 is not None and r4 < r0:
                    flags.append("N3 model=%s: ARM 4 target_hit_rate %.2f < "
                                 "ARM 0 %.2f -- a carried file over-fit the "
                                 "reader; real and reportable, not suppressed"
                                 % (model, r4, r0))
    return flags


# ---- render (N4: every score carries its arm) -----------------------------

def _fmt(x: Optional[float]) -> str:
    return "--" if x is None else "%.3f" % x


def render(cases: Dict[str, dict], runs_dir: str) -> str:
    results = score(cases, runs_dir)
    L = ["FRAME-LOCATION BENCHMARK -- SCORE REPORT",
         "=" * 42, ""]
    if not results:
        L.append("no runs found under %s" % runs_dir)
        L.append("The benchmark run is the operator's step: supply real model")
        L.append("responses under runs/<arm>/<model>/<case_id>.txt. No model")
        L.append("was run here; nothing below would be a result.")
        return "\n".join(L)
    L.append("NOTE: any runs/ shipped in this folder are CONSTRUCTED fixtures")
    L.append("that exercise the counting. They are NOT a benchmark result and")
    L.append("no model was run. Every score below carries its arm label (N4).")
    L.append("")
    for (arm, model) in sorted(results):
        r = results[(arm, model)]
        L.append("arm=%s model=%s" % (arm, model))
        L.append("  scored=%d non_malformed=%d malformed=%d (rate %s)"
                 % (r["scored"], r["non_malformed"], r["malformed"],
                    _fmt(r["malformed_rate"])))
        L.append("  posed_accuracy       %s   [arm=%s]"
                 % (_fmt(r["posed_accuracy"]), arm))
        L.append("  false_positive_rate  %s   [arm=%s] (ceiling check, N1)"
                 % (_fmt(r["false_positive_rate"]), arm))
        L.append("  false_negative_rate  %s   [arm=%s]"
                 % (_fmt(r["false_negative_rate"]), arm))
        L.append("  target_hit_rate      %s   [arm=%s] (HEADLINE; MIS counts "
                 "only on target_hit)" % (_fmt(r["target_hit_rate"]), arm))
        L.append("  target_miss_named    %d       [arm=%s] (detected strain, "
                 "mislocated; not in headline)" % (r["target_miss_named"], arm))
        L.append("  section-9 split [arm=%s]: included=%s  "
                 "excluded_constructed=%s (n_nonconstructed_mis=%d)"
                 % (arm, _fmt(r["headline_included"]),
                    _fmt(r["headline_excluded_constructed"]),
                    r["mis_nonconstructed"]))
        L.append("")
    flags = null_flags(results)
    L.append("NULL / INSTRUMENT-STATUS FLAGS")
    if flags:
        for f in flags:
            L.append("  " + f)
    else:
        L.append("  none fired (with the arms/models present)")
    L.append("")
    L.append("Section 9: every reported set here is source=constructed, so the")
    L.append("constructed-excluded headline has no denominator (--). The")
    L.append("divergence test requires an externally-checked (field/published)")
    L.append("case, which this environment cannot supply (egress-blocked).")
    return "\n".join(L)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.stderr.write("score.py is the scorer; its checks live in "
                         "frame-location-benchmark/selftest_flb.py.\n")
        sys.exit(2)
    here = os.path.dirname(os.path.abspath(__file__))
    cases_path = os.path.join(here, "cases.jsonl")
    runs_path = os.path.join(here, "runs")
    if "--cases" in args:
        cases_path = args[args.index("--cases") + 1]
    if "--runs" in args:
        runs_path = args[args.index("--runs") + 1]
    print(render(load_cases(cases_path), runs_path))
