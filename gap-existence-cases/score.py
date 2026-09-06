# SPDX-License-Identifier: CC0-1.0
"""
CLASS-3 STAGE 3 scorer. OFFLINE: no model, no network.

Reads the hashed commits (STAGE 1) and the stage-2 refs, and reports, per
model arm (cutoff_date + stage-separation -- B2, never pooled across
cutoffs):

    commit_specificity   fraction of EXPECT predicates that are falsifiable
                         (the N3 gate; a run is void below the gate)
    hit                  EXPECT satisfied by post-cutoff retrieved material
    miss_directional     retrieved material contradicts EXPECT
                         -> reasoned gap was real, located wrong
    null_retrieval       nothing retrievable either way
    void_rate            hash failures + unfalsifiable EXPECT

SCORING RULE (from the work order): hit counts ONLY against a falsifiable
EXPECT. A vague commit that matches anything is VOID, never hit -- the
single largest gaming surface, closed by the denominator, not by trust.

B1: a ref counts as resolving material only if its pub_date is strictly
after the model's cutoff_date. B3/N3: a commit below the specificity gate is
VOID. N5: every reported score carries its cutoff_date and stage-separation
status in the same line.

NO NETWORK. This module imports nothing that can reach the network; the
selftest asserts it (the §3 network exception is honored in code -- only
retrieve.py touches the network, and it is a separate invocation).

`commit_specificity` is registered in tools/known_answer.py.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import commit_store as cs  # noqa: E402

# [CHOICE 1] a run whose commit_specificity is below this is VOID before any
# hit is computed (N3). A non-falsifiable EXPECT cannot be hit or missed.
SPEC_GATE = 0.5

# outcome tokens
HIT = "hit"
MISS = "miss_directional"
NULL = "null_retrieval"
VOID_HASH = "void_hash"
VOID_SPEC = "void_unfalsifiable"


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def _matches(finding: str, keys: List[str]) -> bool:
    f = _norm(finding)
    return any(_norm(k) in f for k in (keys or []) if _norm(k))


def post_cutoff_refs(refs: List[Dict], cutoff_date: str) -> List[Dict]:
    """B1: a ref is resolving material only if pub_date > cutoff_date,
    strictly. ISO dates compare lexicographically."""
    return [r for r in refs if (r.get("pub_date") or "") > (cutoff_date or "")]


def score_case(rec: Dict, refs: List[Dict]) -> Dict:
    """One CLASS-3 case: verify hash, gate on specificity, then classify
    against post-cutoff refs."""
    if not cs.verify(rec):
        return {"outcome": VOID_HASH, "specificity": None}
    commit = rec["commit"]
    spec = cs.commit_specificity(commit)
    if spec < SPEC_GATE:
        return {"outcome": VOID_SPEC, "specificity": spec}
    cutoff = commit.get("cutoff_date") or ""
    live = post_cutoff_refs(refs, cutoff)
    preds = [p for p in (commit.get("expect") or [])
             if cs.is_falsifiable(p)]
    contradicted = False
    satisfied = False
    for p in preds:
        for r in live:
            finding = r.get("finding", "")
            if _matches(finding, p.get("contradicted_if")):
                contradicted = True
            elif _matches(finding, p.get("satisfied_if")):
                satisfied = True
    if contradicted:
        outcome = MISS   # located wrong; the reasoned gap was real
    elif satisfied:
        outcome = HIT
    else:
        outcome = NULL
    return {"outcome": outcome, "specificity": spec,
            "post_cutoff_refs": len(live)}


def load_refs(refs_dir: str) -> Dict[str, List[Dict]]:
    out: Dict[str, List[Dict]] = {}
    if not os.path.isdir(refs_dir):
        return out
    for fn in sorted(os.listdir(refs_dir)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(refs_dir, fn)) as fh:
            data = json.load(fh)
        cid = data.get("case_id", fn[:-5])
        out[cid] = data.get("refs", [])
    return out


def _rate(num: int, den: int) -> Optional[float]:
    return (num / den) if den else None


def score(commit_dir: str, refs_dir: str) -> Dict:
    """Group by (cutoff_date, stage_separation) -- an arm. B2: two cutoffs
    are different arms, never pooled."""
    commits = cs.load_commits(commit_dir)
    refs = load_refs(refs_dir)
    arms: Dict = {}
    for cid, rec in commits.items():
        commit = rec.get("commit", {})
        arm = (commit.get("cutoff_date") or "?",
               rec.get("stage_separation") or "?")
        res = score_case(rec, refs.get(cid, []))
        a = arms.setdefault(arm, {"cases": [], "n": 0})
        a["cases"].append((cid, res))
        a["n"] += 1
    # tally per arm
    for arm, a in arms.items():
        counts = {HIT: 0, MISS: 0, NULL: 0, VOID_HASH: 0, VOID_SPEC: 0}
        specs = []
        for _, res in a["cases"]:
            counts[res["outcome"]] += 1
            if res["specificity"] is not None:
                specs.append(res["specificity"])
        n = a["n"]
        void = counts[VOID_HASH] + counts[VOID_SPEC]
        scored = n - void
        a["counts"] = counts
        a["void_rate"] = _rate(void, n)
        a["mean_specificity"] = (sum(specs) / len(specs)) if specs else None
        # hit rate over NON-VOID cases (the denominator closes the gaming
        # surface: a void commit is never in the hit numerator or denominator)
        a["hit_rate"] = _rate(counts[HIT], scored)
    return arms


# ---- nulls ----------------------------------------------------------------

# [CHOICE 2] void_rate at or above this in every arm -> the instrument is
# measuring commit discipline, not gap-location (N1).
VOID_HIGH = 0.5


def null_flags(arms: Dict) -> List[str]:
    flags = []
    vrs = [a["void_rate"] for a in arms.values() if a["void_rate"] is not None]
    if vrs and min(vrs) >= VOID_HIGH:
        flags.append("N1: void_rate >= %.2f in every arm -- the instrument is "
                     "measuring commit discipline, not gap-location "
                     "(instrument property, not a model finding)" % VOID_HIGH)
    return flags


# ---- render (N5: cutoff + stage separation on every line) -----------------

def _fmt(x: Optional[float]) -> str:
    return "--" if x is None else "%.3f" % x


def render(commit_dir: str, refs_dir: str) -> str:
    arms = score(commit_dir, refs_dir)
    L = ["GAP-EXISTENCE CLASS-3 -- STAGE 3 SCORE REPORT",
         "=" * 46, ""]
    if not arms:
        L.append("no commits found under %s" % commit_dir)
        L.append("STAGE 1 (model commits) and STAGE 2 (retrieval) are the")
        L.append("operator's steps; they need a model and the network. No")
        L.append("model was run here; nothing below would be a result.")
        return "\n".join(L)
    L.append("NOTE: any commits/refs shipped here are CONSTRUCTED fixtures")
    L.append("that exercise the STAGE 3 scorer. No model was run and no")
    L.append("retrieval happened; nothing below is a result. Every score")
    L.append("carries its cutoff_date and stage-separation (N5).")
    L.append("")
    for arm in sorted(arms):
        cutoff, stage = arm
        a = arms[arm]
        c = a["counts"]
        L.append("cutoff=%s stage=%s  (n=%d)" % (cutoff, stage, a["n"]))
        L.append("  commit_specificity  %s   [cutoff=%s stage=%s] (N3 gate)"
                 % (_fmt(a["mean_specificity"]), cutoff, stage))
        L.append("  hit=%d miss_directional=%d null_retrieval=%d"
                 % (c[HIT], c[MISS], c[NULL]))
        L.append("  void: hash=%d unfalsifiable=%d  void_rate %s"
                 % (c[VOID_HASH], c[VOID_SPEC], _fmt(a["void_rate"])))
        L.append("  hit_rate (over non-void) %s   [cutoff=%s stage=%s]"
                 % (_fmt(a["hit_rate"]), cutoff, stage))
        L.append("  disposition (every case, N2 -- none discarded):")
        for cid, res in a["cases"]:
            L.append("    %-14s %s" % (cid, res["outcome"]))
        L.append("")
    flags = null_flags(arms)
    L.append("NULL / INSTRUMENT-STATUS FLAGS")
    if flags:
        for f in flags:
            L.append("  " + f)
    else:
        L.append("  none fired (with the arms present)")
    return "\n".join(L)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.stderr.write("score.py is the scorer; its checks live in "
                         "gap-existence-cases/selftest_gxc.py.\n")
        sys.exit(2)
    commit_dir = os.path.join(_HERE, "fixtures", "commit")
    refs_dir = os.path.join(_HERE, "fixtures", "refs")
    if "--commit" in args:
        commit_dir = args[args.index("--commit") + 1]
    if "--refs" in args:
        refs_dir = args[args.index("--refs") + 1]
    print(render(commit_dir, refs_dir))
