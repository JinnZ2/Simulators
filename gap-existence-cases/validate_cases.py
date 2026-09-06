# SPDX-License-Identifier: CC0-1.0
"""
Admission checks. CLASS-2 (dated archive) A1-A5; CLASS-3 (post-cutoff) B4
prompt screen. OFFLINE, no network.

CLASS-2 blocks on the archive consolidation with timestamps (build order
step 5), which needs the archive and is not reachable here. The seed set
(§2.4) has no entry dates established, so NONE is admissible under A1
(pub_date > entry_date strictly). Per N4, when CLASS-2 admits fewer than ~10
cases the honest handling is to say so and report CLASS-3 alone -- NOT to
relax A1-A5 to reach a sample size. So `archive_cases.jsonl` ships empty (0
admitted) and this validator reports that state rather than treating it as a
failure.

The functions are importable so the selftest can drive them with good and
planted-bad inputs (null test both directions).

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List

MATCH_CLASSES = ("CORRECTED", "REPLICATED", "ADJACENT", "NULL")

# N4: below this admitted count, report CLASS-3 alone (do not relax A1-A5).
MIN_CLASS2 = 10


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def load_archive_cases(path: str) -> List[Dict]:
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def check_A1_A5(cases: List[Dict]) -> List[str]:
    """Every admitted CLASS-2 case must satisfy the admission rules. A2
    (verbatim) and A3 (target predictive) are judgements the schema can only
    partly enforce; the mechanical parts are checked and the rest required to
    be present."""
    msg = []
    for c in cases:
        cid = c.get("id", "<no id>")
        ed = c.get("entry_date") or ""
        ref = c.get("resolving_ref") or {}
        pd = ref.get("pub_date") or ""
        # A1: pub_date > entry_date strictly, and not the same month
        if not (ed and pd):
            msg.append("A1 FAIL %s: entry_date and pub_date required" % cid)
        elif pd <= ed:
            msg.append("A1 FAIL %s: pub_date %s not strictly after entry_date "
                       "%s" % (cid, pd, ed))
        elif ed[:7] == pd[:7]:
            msg.append("A1 FAIL %s: same-month admission (%s / %s)"
                       % (cid, ed, pd))
        # A2: entry_text present (verbatim is a judgement; require non-empty)
        if not c.get("entry_text"):
            msg.append("A2 FAIL %s: entry_text required (verbatim, no "
                       "after-the-fact sharpening)" % cid)
        # A3: target specific enough to be wrong (require non-empty specific)
        if not c.get("target") or len(_norm(c.get("target"))) < 3:
            msg.append("A3 FAIL %s: target must be specific enough to be "
                       "wrong" % cid)
        # A4: independence stated
        if not c.get("independence"):
            msg.append("A4 FAIL %s: independence must be stated (say so if "
                       "downstream carriage cannot be excluded)" % cid)
        # A5: match_class valid and a coding timestamp logged
        if c.get("match_class") not in MATCH_CLASSES:
            msg.append("A5 FAIL %s: match_class must be one of %r"
                       % (cid, MATCH_CLASSES))
        if not c.get("match_class_coded_at"):
            msg.append("A5 FAIL %s: match_class_coded_at timestamp required "
                       "(assigned before reading beyond the abstract)" % cid)
    return msg


def class2_disposition(cases: List[Dict]) -> Dict[str, int]:
    """N2: the full disposition table -- ADJACENT and NULL are results,
    never discarded."""
    d = {mc: 0 for mc in MATCH_CLASSES}
    for c in cases:
        mc = c.get("match_class")
        if mc in d:
            d[mc] += 1
    return d


def screen_prompt(prompt: str, blocked_terms: List[str]) -> List[str]:
    """B4: a prompt must not contain post-cutoff terminology -- a term the
    model has never seen leaks the date. `blocked_terms` is operator-supplied
    per model (the post-cutoff vocabulary). Returns the leaked terms."""
    p = _norm(prompt)
    return [t for t in (blocked_terms or []) if _norm(t) and _norm(t) in p]


def validate(archive_path: str) -> (bool, List[str]):
    cases = load_archive_cases(archive_path)
    msgs = check_A1_A5(cases)
    # N4 state is reported by the caller; A1-A5 violations are failures.
    return (len(msgs) == 0), msgs


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    archive = os.path.join(here, "archive_cases.jsonl")
    cases = load_archive_cases(archive)
    ok, msgs = validate(archive)
    print("validate_cases (CLASS-2 admission, A1-A5)")
    print("  admitted CLASS-2 cases: %d" % len(cases))
    if len(cases) < MIN_CLASS2:
        print("  N4: fewer than %d admitted -- report CLASS-3 alone. The "
              "archive consolidation with timestamps (build order step 5) is "
              "not reachable here, and the §2.4 seed set has no entry dates "
              "established, so nothing is admissible under A1. The admission "
              "rules were NOT relaxed to reach a sample size." % MIN_CLASS2)
    if ok:
        print("  A1-A5: PASS (no admitted case violates a rule)")
        sys.exit(0)
    print("  A1-A5: FAIL")
    for m in msgs:
        print("    " + m)
    sys.exit(1)
