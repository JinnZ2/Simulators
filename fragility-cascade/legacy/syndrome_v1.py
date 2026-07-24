"""
syndrome.py -- parity / trace / mesh on the divergence log. CC0. stdlib only.
imports divlog. (entrain is orthogonal; syndrome reads whatever phase fields
are already on the entries.)

Reads a divergence log and returns FLAT LISTS:
    parity(entries)          count entries by KIND, on digest+band only.
                             Never a score. Counts are for the operator.
    trace(entries, primary)  entries where axis_a or axis_b is `primary`,
                             ordered as recorded. The primary's own history.
    mesh(entries)            the 3x3 (target x kind), flat list of cells.
                             Every cell carries its entries; nothing is
                             aggregated into a scalar.

No aggregation. No verdicts. The log's shape is the answer; the operator
looks at it.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Iterable

import divlog


TARGETS = ("claim", "mode_sensitivity", "independence")

MESH_KINDS = (divlog.KIND_DIVERGENCE_SAME_FACTS,
              divlog.KIND_HOMOPLASY,
              divlog.KIND_DIVERGENCE_DIFFERENT_INPUTS)
# AGREEMENT_SAME_FACTS is intentionally omitted from the mesh -- trivial
# agreement is logged (see divlog docstring) but is not part of the syndrome
# shape. The mesh is what needs looking at.


# --------------------------------------------------------------------- parity

def parity(entries: Iterable[divlog.Entry]) -> Dict[str, int]:
    """Count entries by KIND. Digest+band only; no other axis reads."""
    counts = {k: 0 for k in divlog.KINDS}
    for e in entries:
        counts[e.kind] = counts.get(e.kind, 0) + 1
    return counts


# ---------------------------------------------------------------------- trace

def trace(entries: Iterable[divlog.Entry], primary: str) -> List[divlog.Entry]:
    """Return every entry involving `primary` on either axis, in original order.
    The primary is the reference; trace is the primary's own divergence
    history."""
    return [e for e in entries if e.axis_a == primary or e.axis_b == primary]


# ----------------------------------------------------------------------- mesh

@dataclass
class MeshCell:
    target: str
    kind: str
    entries: List[divlog.Entry] = field(default_factory=list)


def mesh(entries: Iterable[divlog.Entry],
         targets=TARGETS, kinds=MESH_KINDS) -> List[MeshCell]:
    """
    Flat list of `len(targets) * len(kinds)` cells. Every cell carries the
    entries that landed in it. Nothing is counted, nothing is scored.

    Cells are emitted in row-major order (all kinds of target[0], then all
    kinds of target[1], ...). Empty cells are emitted with `entries=[]`.
    """
    cells: List[MeshCell] = []
    by_key: Dict[tuple, List[divlog.Entry]] = {}
    for e in entries:
        by_key.setdefault((e.target, e.kind), []).append(e)
    for t in targets:
        for k in kinds:
            cells.append(MeshCell(target=t, kind=k,
                                  entries=list(by_key.get((t, k), []))))
    return cells


# ------------------------------------------------------------ pretty-print

def print_mesh(cells: List[MeshCell]) -> None:
    """Diagnostic view: rows are targets, columns are kinds, cells show
    count and a leading subject sample. No aggregation happens here either
    -- this is a formatter, not a metric."""
    from collections import OrderedDict
    per_target: Dict[str, List[MeshCell]] = OrderedDict()
    for c in cells:
        per_target.setdefault(c.target, []).append(c)
    if not per_target:
        print("  (empty mesh)")
        return
    kinds = [c.kind for c in next(iter(per_target.values()))]
    print("  " + " " * 22 + "  ".join(f"{k[:26]:>26s}" for k in kinds))
    for t, row in per_target.items():
        cells_txt = []
        for c in row:
            n = len(c.entries)
            sample = ""
            if c.entries:
                s = c.entries[0].subject
                sample = f" e.g. {s[:18]}"
            cells_txt.append(f"n={n}{sample:<21}")
        print(f"  {t:20s}  " + "  ".join(f"{txt:>26s}" for txt in cells_txt))
