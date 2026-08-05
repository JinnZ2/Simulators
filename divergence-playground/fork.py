#!/usr/bin/env python3
"""
fork.py -- Fork records for the DIVERGENCE PLAYGROUND.  stdlib only, CC0.

A Fork is a point in a piece of work where the raw data admits more
than one honest reading.  Loading a Fork gives a reader (human or AI)
everything needed to commit an independent reading -- the data, the
named branches, the collapse condition, the cost -- without seeing
what any other reader posted.  That's the anti-anchoring seal.

Field contract (checked at load time):

    id                       str    stable identifier, e.g. "FK-1"
    title                    str    one-line description
    data                     str    what the reader is looking at
    branches                 list   named forks the reader chooses among
    collapse                 str    experiment that would resolve them
    cost                     str    LOW | MEDIUM | HIGH  (compute/effort)
    status                   str    OPEN | RESOLVED | PARTIAL | STAKED
    resolved_by              str    optional: DP-# or F-# or free text
    source                   str    where this fork was harvested from

Storage: newline-delimited JSON, one Fork per line (FORKS.jsonl).
No hidden state, no crypto -- the seal is enforced by seal.py, not by
the storage format.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional


COST_LEVELS = ("LOW", "MEDIUM", "HIGH")
STATUS_LEVELS = ("OPEN", "RESOLVED", "PARTIAL", "STAKED")


@dataclass
class Fork:
    id: str
    title: str
    data: str
    branches: List[str]
    collapse: str
    cost: str = "MEDIUM"
    status: str = "OPEN"
    resolved_by: str = ""
    source: str = ""

    def __post_init__(self):
        if self.cost not in COST_LEVELS:
            raise ValueError(f"cost must be one of {COST_LEVELS}, got {self.cost!r}")
        if self.status not in STATUS_LEVELS:
            raise ValueError(f"status must be one of {STATUS_LEVELS}, got {self.status!r}")
        if not self.branches:
            raise ValueError(f"{self.id}: branches must be non-empty")
        if len(self.branches) < 2:
            raise ValueError(f"{self.id}: a fork needs >= 2 branches (got {len(self.branches)})")

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, line: str) -> "Fork":
        return cls(**json.loads(line))


def load(path: str) -> List[Fork]:
    """Read all forks from a FORKS.jsonl file."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [Fork.from_json(line) for line in f if line.strip()]


def save(forks: List[Fork], path: str) -> None:
    """Write forks to a FORKS.jsonl file (overwrites)."""
    with open(path, "w", encoding="utf-8") as f:
        for fk in forks:
            f.write(fk.to_json() + "\n")


def get(path: str, fork_id: str) -> Fork:
    """Load a specific fork by id."""
    for fk in load(path):
        if fk.id == fork_id:
            return fk
    raise KeyError(f"no fork with id={fork_id!r} in {path}")


def summary(path: str) -> None:
    """Print a compact status table."""
    forks = load(path)
    if not forks:
        print(f"no forks in {path}")
        return
    by_status = {}
    for f in forks:
        by_status.setdefault(f.status, []).append(f)
    print(f"{'id':<7}{'cost':<8}{'status':<11}branches")
    for f in forks:
        b = " | ".join(f.branches)
        print(f"{f.id:<7}{f.cost:<8}{f.status:<11}{b}")
    print()
    for s in STATUS_LEVELS:
        if s in by_status:
            print(f"  {s:<10} {len(by_status[s])}")


# --- self-test ------------------------------------------------------------

def _t_roundtrip():
    fk = Fork(id="TEST-0", title="test", data="d",
              branches=["a", "b"], collapse="c")
    fk2 = Fork.from_json(fk.to_json())
    assert fk == fk2


def _t_reject_bad_cost():
    try:
        Fork(id="X", title="t", data="d", branches=["a", "b"],
             collapse="c", cost="BOGUS")
    except ValueError:
        return
    raise AssertionError("should have rejected bogus cost")


def _t_reject_single_branch():
    try:
        Fork(id="X", title="t", data="d", branches=["only"], collapse="c")
    except ValueError:
        return
    raise AssertionError("should have rejected 1-branch fork")


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
