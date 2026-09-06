# SPDX-License-Identifier: CC0-1.0
"""
CLASS-3 commit store -- STAGE 1 write + hash, STAGE 3 verify. OFFLINE.

The staging is the load-bearing structure (GX-3), not a procedure: a model
cannot tell reasoned-it from read-it once retrieval has run, so the
enforcement lives in the process boundary, not in an instruction. STAGE 1
writes the commit and its hash and the process EXITS; STAGE 3 re-hashes the
committed content and, if it does not verify, the case is VOID -- not
penalised.

This defends against self-deception (a later pass rewriting EXPECT to match
what was read), not against a determined editor who also recomputes the hash;
the work order states that limit and puts the enforcement at the boundary
rather than in trust.

NO NETWORK. This module imports nothing that can reach the network; the
selftest asserts it (the §3 network exception is honored in code).

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List

# the fields hashed at commit time (STAGE 1's declaration).
COMMIT_FIELDS = ("case_id", "posed", "target", "basis", "expect",
                 "cutoff_date", "model")


class CommitError(Exception):
    pass


def canonical(commit: Dict) -> bytes:
    """Deterministic serialization of the committed fields only, so the hash
    depends on the declaration and nothing else (not the timestamp)."""
    sub = {}
    for k in COMMIT_FIELDS:
        if k not in commit:
            raise CommitError("commit missing field %r" % k)
        sub[k] = commit[k]
    return json.dumps(sub, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def commit_hash(commit: Dict) -> str:
    return hashlib.sha256(canonical(commit)).hexdigest()


def write_commit(commit_dir: str, commit: Dict,
                 stage_separation: str = "staged") -> str:
    """STAGE 1. Writes commit/<case_id>.json with the declaration, its
    sha256, a commit timestamp, and the stage-separation status. The runner
    exits after this; STAGE 2 is a separate invocation."""
    os.makedirs(commit_dir, exist_ok=True)
    h = commit_hash(commit)
    rec = {"commit": {k: commit[k] for k in COMMIT_FIELDS},
           "sha256": h,
           "committed_at": datetime.now(timezone.utc).isoformat(),
           "stage_separation": stage_separation}
    path = os.path.join(commit_dir, "%s.json" % commit["case_id"])
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
    return path


def load_commit(path: str) -> Dict:
    with open(path) as fh:
        return json.load(fh)


def verify(rec: Dict) -> bool:
    """STAGE 3. Re-hash the committed declaration and compare to the stored
    hash. False -> the case is VOID (hash failure), not penalised."""
    try:
        return commit_hash(rec["commit"]) == rec["sha256"]
    except (CommitError, KeyError, TypeError):
        return False


def load_commits(commit_dir: str) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    if not os.path.isdir(commit_dir):
        return out
    for fn in sorted(os.listdir(commit_dir)):
        if fn.endswith(".json"):
            rec = load_commit(os.path.join(commit_dir, fn))
            cid = rec.get("commit", {}).get("case_id", fn[:-5])
            out[cid] = rec
    return out


# ---- EXPECT predicate helpers (the falsifiability of a commit) ------------

def is_falsifiable(predicate: Dict) -> bool:
    """A predicate is falsifiable iff it states what retrieved material would
    have to say to CONTRADICT it (a predicate that can fail). An EXPECT with
    no `contradicted_if` cannot be missed, so it cannot be hit either (B3)."""
    return bool((predicate.get("contradicted_if") or []))


def commit_specificity(commit: Dict) -> float:
    """Fraction of EXPECT predicates that are falsifiable -- the N3 gate. A
    commit with no predicates is 0.0 (nothing that can fail)."""
    preds: List[Dict] = commit.get("expect") or []
    if not preds:
        return 0.0
    fals = sum(1 for p in preds if is_falsifiable(p))
    return fals / len(preds)


if __name__ == "__main__":
    import sys
    sys.stderr.write("commit_store.py is a library; its checks live in "
                     "gap-existence-cases/selftest_gxc.py.\n")
    sys.exit(2)
