# SPDX-License-Identifier: CC0-1.0
"""
CLASS-3 STAGE 2 -- RETRIEVE. The ONE network-touching runner (the §3
NETWORK EXCEPTION). A SEPARATE invocation from STAGE 1: the commit file is
NOT in context, so the search cannot be steered by the committed EXPECT.

It searches for material that could satisfy or contradict a case's posed
problem, and writes refs (title, venue, pub_date, locator, finding) to
refs/<case_id>.json. STAGE 3 (`score.py`) then checks B1 (pub_date > cutoff)
and matches each finding against the committed predicates.

NOT RUN HERE. This step needs (a) a retrieval-capable model and (b) network
egress, neither available in this environment (egress is an allowlist; only
github.com answers). `search()` therefore raises `NotRunnable` rather than
returning anything, and the runner NEVER fabricates a ref -- a fabricated
pub_date would forge the external key the whole class exists to supply.
Supplying real refs is the operator's step.

`write_refs` is the pure writer the operator's retrieval feeds; it does not
touch the network and is safe to import.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List

# This module is the network-touching piece. commit_store.py and score.py
# are not, and must run with the network unavailable (asserted in the
# selftest).
NETWORK_TOUCHING = True


class NotRunnable(Exception):
    pass


def search(query: str) -> List[Dict]:
    """Would issue a live search (network). Refuses to run here: no reachable
    retrieval and no model, and it must never fabricate a dated ref."""
    raise NotRunnable(
        "STAGE 2 retrieval needs a retrieval-capable model and network "
        "egress; neither is available here. No ref is fabricated -- a forged "
        "pub_date would forge the external key. Run STAGE 2 as a separate "
        "invocation with network, then supply refs via write_refs().")


def write_refs(refs_dir: str, case_id: str, refs: List[Dict]) -> str:
    """Pure writer. `refs` is a list of {title, venue, pub_date, locator,
    finding}. Offline; the operator's retrieval produces `refs`."""
    os.makedirs(refs_dir, exist_ok=True)
    for r in refs:
        for k in ("title", "venue", "pub_date", "locator", "finding"):
            if k not in r:
                raise ValueError("ref missing field %r" % k)
    path = os.path.join(refs_dir, "%s.json" % case_id)
    with open(path, "w") as fh:
        json.dump({"case_id": case_id, "refs": refs}, fh, indent=2)
    return path


if __name__ == "__main__":
    sys.stderr.write(
        "retrieve.py is STAGE 2 (the network-touching runner). It is NOT run "
        "here: no reachable retrieval, no model, and it never fabricates a "
        "dated ref. Run it as a separate invocation with network available, "
        "then feed refs to write_refs(). STAGE 1 (commit_store) and STAGE 3 "
        "(score) run offline.\n")
    sys.exit(2)
