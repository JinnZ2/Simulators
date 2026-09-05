# SPDX-License-Identifier: CC0-1.0
"""
Rule 3 -- aggregation is a read operation. No aggregate, rounding, or bucket
is stored as a base field; every aggregate is computed at read time from raw
entries and a spec. Store the recipe, not the result. If an aggregate is
expensive it may be cached, but the cache is keyed to the spec AND the
base-entry version and is treated as derived -- it is never the record.

This module also enforces two rules at the point they bite in a read:

  - Rule 5: entries are summed only if their boundaries match or a declared
    reconciliation covers the set; otherwise the compute REFUSES
    (`BoundaryMismatch`). An undeclared boundary raises.
  - Rule 7: `measured_zero` enters a numeric fold as 0.0; the `unmeasured_*`
    states never enter it and never read as zero -- they are counted apart,
    and an all-absent group is NOT_COMPUTABLE, never 0.0.

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from base_entry import (BaseEntry, Reconciliation, UndeclaredBoundary,
                        BoundaryMismatch, MEASURED, MEASURED_ZERO,
                        UNMEASURED_NO_INSTRUMENT, UNMEASURED_OUT_OF_SCOPE)
from views import ViewRegistry

SUM = "sum"
MEAN = "mean"
RATE = "rate"
RATIO = "ratio"
OPERATIONS = (SUM, MEAN, RATE, RATIO)

NOT_COMPUTABLE = "NOT_COMPUTABLE"


@dataclass
class AggregateSpec:
    agg_id: str
    over_view: str                    # which view's labels group by
    operation: str                    # sum | mean | rate | ratio
    denominator: str = ""             # declared explicitly; a field name or
                                      # "measured_count" (Rule 5 / Rule 3)
    # filter: which base entries are in scope. A named, inspectable predicate.
    filter: Optional[Callable[[BaseEntry], bool]] = None
    filter_desc: str = "all"

    def in_scope(self, e: BaseEntry) -> bool:
        return True if self.filter is None else self.filter(e)


@dataclass
class GroupResult:
    label: Optional[str]
    value: Optional[float]            # None == NOT_COMPUTABLE / undefined
    flag: str                         # OK | NOT_COMPUTABLE
    n_measured: int
    n_measured_zero: int
    n_unmeasured_no_instrument: int
    n_unmeasured_out_of_scope: int

    @property
    def n_absent(self) -> int:
        return (self.n_unmeasured_no_instrument +
                self.n_unmeasured_out_of_scope)


@dataclass
class AggregateResult:
    agg_id: str
    operation: str
    base_version: int
    groups: List[GroupResult]
    derived: bool = True              # an aggregate is always derived (Rule 3)

    def by_label(self) -> Dict[Optional[str], GroupResult]:
        return {g.label: g for g in self.groups}


def _denominator_field(e: BaseEntry, name: str) -> Optional[float]:
    if name == "exposure":
        return e.exposure_value()      # None if the exposure column is absent
    if name == "joules_in":
        return e.numeric_joules()
    raise ValueError("unknown denominator field %r (declare exposure, "
                     "joules_in, or measured_count)" % name)


def _summable(entries: List[BaseEntry],
              reconciliations: List[Reconciliation]) -> None:
    """Rule 5. Raise if the in-scope entries cannot be summed: an undeclared
    boundary anywhere, or two distinct boundaries with no reconciliation
    connecting them. Reconciliations must connect the distinct boundaries
    into one set."""
    for e in entries:
        if not e.comparable():
            raise UndeclaredBoundary(
                "entry %r has no declared boundary; not comparable, flag it "
                "unusable rather than summing it (Rule 5)" % e.entry_id)
    keys = []
    for e in entries:
        k = e.boundary.key()
        if k not in keys:
            keys.append(k)
    if len(keys) <= 1:
        return
    # union-find over the distinct boundary keys, joined by reconciliations
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r in (reconciliations or ()):
        if r.boundary_a in parent and r.boundary_b in parent:
            parent[find(r.boundary_a)] = find(r.boundary_b)
    roots = {find(k) for k in keys}
    if len(roots) > 1:
        raise BoundaryMismatch(
            "in-scope entries carry %d distinct boundaries not connected by "
            "a declared reconciliation; refusing to sum across them (Rule 5)"
            % len(keys))


def compute(spec: AggregateSpec, entries: List[BaseEntry],
            registry: ViewRegistry, base_version: int = 0,
            reconciliations: Optional[List[Reconciliation]] = None
            ) -> AggregateResult:
    """Compute the aggregate at read time from raw entries and the spec
    alone. Deterministic; the same entries + spec give the same result
    (acceptance #2)."""
    if spec.operation not in OPERATIONS:
        raise ValueError("operation must be one of %r; got %r"
                         % (OPERATIONS, spec.operation))
    scope = [e for e in entries if spec.in_scope(e)]
    ids = [e.entry_id for e in scope]
    groups_map = registry.group_by(spec.over_view, ids)
    by_id = {e.entry_id: e for e in scope}

    results: List[GroupResult] = []
    for label in sorted(groups_map, key=lambda x: (x is None, x)):
        gents = [by_id[i] for i in groups_map[label]]
        # Rule 7 is per COLUMN: an entry contributes to the joules fold iff
        # its joules_in COLUMN is measured/measured_zero, even if the entry
        # status is measured on other columns (Case B: measured output,
        # absent joules). Counts are over the folded column's status.
        def _cs(e):
            return e.column_status_of("joules_in")
        nm = sum(1 for e in gents if _cs(e) == MEASURED)
        nz = sum(1 for e in gents if _cs(e) == MEASURED_ZERO)
        nni = sum(1 for e in gents if _cs(e) == UNMEASURED_NO_INSTRUMENT)
        nos = sum(1 for e in gents if _cs(e) == UNMEASURED_OUT_OF_SCOPE)
        contributing = [e for e in gents if _cs(e) in (MEASURED, MEASURED_ZERO)]
        if not contributing:
            results.append(GroupResult(label, None, NOT_COMPUTABLE,
                                       nm, nz, nni, nos))
            continue
        _summable(contributing, reconciliations or [])
        num = sum(e.numeric_joules() for e in contributing)
        if spec.operation == SUM:
            value = num
        elif spec.operation == MEAN:
            if spec.denominator not in ("", "measured_count"):
                raise ValueError("mean's denominator must be declared as "
                                 "'measured_count'; got %r" % spec.denominator)
            n = nm + nz
            value = num / n if n else None
        else:  # RATE or RATIO
            if not spec.denominator or spec.denominator == "measured_count":
                raise ValueError("%s requires an explicitly declared field "
                                 "denominator (Rule 5); got %r"
                                 % (spec.operation, spec.denominator))
            dvals = [_denominator_field(e, spec.denominator)
                     for e in contributing]
            if any(d is None for d in dvals):
                value = None
            else:
                den = sum(dvals)
                value = num / den if den else None
        flag = NOT_COMPUTABLE if value is None else "OK"
        results.append(GroupResult(label, value, flag, nm, nz, nni, nos))
    return AggregateResult(spec.agg_id, spec.operation, base_version, results)


# ---- Rule 3: a cache keyed to spec + base version, treated as derived ------

class AggregateCache:
    """Caches results keyed to (agg_id, base_version). A cache from a stale
    base_version is a miss -- it never shadows the record. The cached object
    is marked derived."""

    def __init__(self):
        self._c: Dict[Tuple[str, int], AggregateResult] = {}

    def cached_or_compute(self, spec, entries, registry, base_version,
                          reconciliations=None) -> AggregateResult:
        key = (spec.agg_id, base_version)
        if key in self._c:
            return self._c[key]
        res = compute(spec, entries, registry, base_version, reconciliations)
        res.derived = True
        self._c[key] = res
        return res

    def has(self, agg_id, base_version) -> bool:
        return (agg_id, base_version) in self._c


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("aggregate.py is a library; its checks live in "
                    "machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
