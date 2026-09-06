# SPDX-License-Identifier: CC0-1.0
"""
Case-set validation (R1-R6) plus the section-4 contamination check.

The contamination rule is the load-bearing single point of failure: no
harness file may contain any case's domain-specific content (`prompt`),
its `fault_target`, or a worked instance of the same fault in the same
`(fault_class, domain)`. Cross-domain instances of a fault_class ARE
permitted -- that is the transfer under test -- so the check does NOT
forbid the generic reframe vocabulary (`accept[]`); it forbids the
domain-specific answer and the case content.

Bare invocation validates the shipped cases + harness and exits nonzero
on any violation. The functions are importable so the selftest can drive
them with good and planted-bad inputs (null test both directions).

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List, Set, Tuple

FAULT_CLASSES = ("WRONG_INSTRUMENT", "MISSING_DENOMINATOR", "UNSCOPED_CLAIM",
                 "UNIT_OF_ANALYSIS", "PROXY_AS_QUANTITY", "SINGLE_EVENT_FRAME",
                 "ACCEPTED_SIDE")

# R6: prompts must be the stated problem only -- no framing/hint markers.
HINT_MARKERS = ("mis-posed", "well-posed", "is this the right", "reframe",
                "posed:", "fault_class", "trick question")

CORR_RE = re.compile(r"\[CORRECTION\s+class=([A-Z_]+)\s+domain=([a-z0-9\-]+)\]")


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def load_cases(path: str) -> List[dict]:
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def check_schema(cases: List[dict]) -> List[str]:
    msg = []
    ids = set()
    for c in cases:
        cid = c.get("id", "<no id>")
        if cid in ids:
            msg.append("duplicate id %s" % cid)
        ids.add(cid)
        if c.get("posed") not in ("WELL", "MIS"):
            msg.append("%s: posed must be WELL|MIS" % cid)
            continue
        if c["posed"] == "MIS":
            if c.get("fault_class") not in FAULT_CLASSES:
                msg.append("%s: MIS needs a valid fault_class" % cid)
            if not c.get("fault_target"):
                msg.append("%s: MIS needs fault_target" % cid)
            if not c.get("accept"):
                msg.append("%s: MIS needs accept[]" % cid)
        else:
            if c.get("fault_class") is not None:
                msg.append("%s: WELL must have fault_class null" % cid)
            if not c.get("well_posed_answer"):
                msg.append("%s: WELL needs well_posed_answer" % cid)
    return msg


def check_R1(cases: List[dict]) -> List[str]:
    n = len(cases)
    well = sum(1 for c in cases if c["posed"] == "WELL")
    if n and well / n < 0.40:
        return ["R1 FAIL: WELL share %.1f%% < 40%% (controls load-bearing)"
                % (100 * well / n)]
    return []


def check_R2(cases: List[dict]) -> List[str]:
    mis = [c for c in cases if c["posed"] == "MIS"]
    if not mis:
        return ["R2 FAIL: no MIS cases"]
    counts: Dict[str, int] = {}
    for c in mis:
        counts[c["fault_class"]] = counts.get(c["fault_class"], 0) + 1
    worst = max(counts.values()) / len(mis)
    if worst > 0.25:
        return ["R2 FAIL: a fault_class is %.1f%% of MIS (> 25%%)"
                % (100 * worst)]
    return []


def check_R3(cases: List[dict]) -> List[str]:
    msg = []
    domains = set(c["domain"] for c in cases)
    if len(domains) < 3:
        msg.append("R3 FAIL: %d domains (< 3)" % len(domains))
    per: Dict[str, Set[str]] = {}
    for c in cases:
        if c["posed"] == "MIS":
            per.setdefault(c["fault_class"], set()).add(c["domain"])
    for fc, doms in per.items():
        if len(doms) < 2:
            msg.append("R3 FAIL: fault_class %s appears in only 1 domain "
                       "(no cross-domain transfer)" % fc)
    return msg


def check_R4(cases: List[dict]) -> List[str]:
    msg = []
    for c in cases:
        if c["posed"] == "MIS":
            if not c.get("notes"):
                msg.append("R4 FAIL: MIS %s has no notes" % c["id"])
            if c.get("source") not in ("field", "published", "constructed"):
                msg.append("R4 FAIL: %s has no valid source" % c["id"])
    return msg


def check_R6(cases: List[dict]) -> List[str]:
    msg = []
    for c in cases:
        low = c["prompt"].lower()
        for m in HINT_MARKERS:
            if m in low:
                msg.append("R6 FAIL: %s prompt contains hint marker %r"
                           % (c["id"], m))
    return msg


def parse_corrections(arm3_text: str) -> Set[Tuple[str, str]]:
    return set(CORR_RE.findall(arm3_text))


def check_contamination(cases: List[dict], harness: Dict[str, str],
                        corrections: Set[Tuple[str, str]]) -> List[str]:
    """§4. No prompt/fault_target substring in any harness file; no arm3
    (class,domain) equals a case (class,domain); each MIS class has a
    correction in a different domain."""
    msg = []
    norm_harness = {name: _norm(text) for name, text in harness.items()}
    for c in cases:
        for field in ("prompt", "fault_target"):
            val = _norm(c.get(field) or "")
            if not val:
                continue
            for name, text in norm_harness.items():
                if val in text:
                    msg.append("CONTAMINATION: case %s %s appears in harness "
                               "file %s" % (c["id"], field, name))
    # same-(class,domain) collision
    case_cd = set((c["fault_class"], c["domain"]) for c in cases
                  if c["posed"] == "MIS")
    for (cls, dom) in corrections:
        if (cls, dom) in case_cd:
            msg.append("CONTAMINATION: ARM 3 correction (%s, %s) is a "
                       "same-(class,domain) worked instance of a case"
                       % (cls, dom))
    # transfer actually set up: each MIS class has a correction in a
    # different domain than its cases.
    case_classes = set(c["fault_class"] for c in cases if c["posed"] == "MIS")
    corr_classes = set(cls for (cls, _) in corrections)
    for cls in case_classes:
        if cls not in corr_classes:
            msg.append("TRANSFER GAP: fault_class %s has no ARM 3 correction "
                       "in any domain (FL-5 transfer not set up)" % cls)
    return msg


def load_harness(harness_dir: str) -> Dict[str, str]:
    out = {}
    if not os.path.isdir(harness_dir):
        return out
    for fn in sorted(os.listdir(harness_dir)):
        if fn.endswith(".txt"):
            with open(os.path.join(harness_dir, fn)) as fh:
                out[fn] = fh.read()
    return out


def validate(cases_path: str, harness_dir: str) -> Tuple[bool, List[str]]:
    cases = load_cases(cases_path)
    harness = load_harness(harness_dir)
    arm3 = harness.get("arm3_corrections.txt", "")
    corrections = parse_corrections(arm3)
    msgs: List[str] = []
    msgs += check_schema(cases)
    msgs += check_R1(cases)
    msgs += check_R2(cases)
    msgs += check_R3(cases)
    msgs += check_R4(cases)
    msgs += check_R6(cases)
    msgs += check_contamination(cases, harness, corrections)
    return (len(msgs) == 0), msgs


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ok, msgs = validate(os.path.join(here, "cases.jsonl"),
                        os.path.join(here, "harness"))
    if ok:
        print("validate_cases: PASS (R1-R6 + section-4 contamination)")
        sys.exit(0)
    print("validate_cases: FAIL")
    for m in msgs:
        print("  " + m)
    sys.exit(1)
