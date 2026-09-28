#!/usr/bin/env python3
"""The claim record: schema, intake validation, and reference resolution.

A claim record is what a sim emits. The ledger reads records; it does not run
sims and does not time anything.

FIELDS, per the order:

    claim_id     the sim's own id for the claim
    sim          the folder that owns it
    value        a decimal STRING, never a float
    precision    declared by the emitter
    operands     claim references or literals this value was computed from
    falsifier    the existing falsifier text
    status       the existing status
    provenance   MEASURED | DERIVED | CARRIED

TWO ADDITIONS THE ORDER'S OWN REQUIREMENTS FORCE, both declared rather than
slipped in:

1. `expression`, required for DERIVED. The order requires the ledger to
   "recompute every DERIVED claim from its operands, exact decimal". A list of
   operands does not say what was done with them: `[a, b]` recomputes to a+b,
   a*b, a/b or a-b with equal warrant, and picking one would be the ledger
   inventing the arithmetic it exists to check. The expression names the
   operation and nothing else; operands must match the names it uses.

2. Qualified references. The order writes operands as "a list of claim_ids",
   and in this tree a claim_id is NOT unique. Measured: CA_, RC_, MP_, SS_ and
   EMRG_ are each owned by two or three different folders, every one of them
   numbering from 001. `RC_003` alone names three different claims. So a
   reference is `sim:claim_id`, and a bare `claim_id` resolves inside the
   emitting sim only. A bare reference that matches nothing local is an intake
   failure rather than a guess at which folder was meant.

INTAKE FAILURES are results, not crashes. `validate()` returns a list of
problems; nothing here raises on a bad record.

stdlib only. CC0.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "1.0"

REF = re.compile(r"^(?:([A-Za-z0-9_.-]+):)?([A-Za-z][A-Za-z0-9_]*)$")
DECIMAL_STR = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")


class Provenance(str, Enum):
    MEASURED = "MEASURED"
    DERIVED = "DERIVED"
    CARRIED = "CARRIED"
    # Resolved transitively by the ledger, never declared by an emitter.
    DERIVED_WEAK = "DERIVED_WEAK"


DECLARABLE = (Provenance.MEASURED, Provenance.DERIVED, Provenance.CARRIED)

REQUIRED = ("claim_id", "sim", "value", "precision", "operands", "falsifier",
            "status", "provenance")


@dataclass
class ClaimRecord:
    claim_id: str
    sim: str
    value: str
    precision: int
    operands: List[str]
    falsifier: str
    status: str
    provenance: Provenance
    expression: Optional[str] = None
    falsifier_test: Optional[str] = None
    source: Optional[str] = None

    def key(self) -> Tuple[str, str]:
        return (self.sim, self.claim_id)

    def ref(self) -> str:
        return "%s:%s" % (self.sim, self.claim_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id, "sim": self.sim, "value": self.value,
            "precision": self.precision, "operands": list(self.operands),
            "falsifier": self.falsifier, "status": self.status,
            "provenance": self.provenance.value, "expression": self.expression,
            "falsifier_test": self.falsifier_test, "source": self.source,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClaimRecord":
        return cls(
            claim_id=str(d["claim_id"]), sim=str(d["sim"]),
            value=str(d["value"]), precision=int(d["precision"]),
            operands=[str(o) for o in d.get("operands") or []],
            falsifier=str(d.get("falsifier", "")),
            status=str(d.get("status", "")),
            provenance=Provenance(str(d["provenance"])),
            expression=d.get("expression"),
            falsifier_test=d.get("falsifier_test"),
            source=d.get("source"))


def parse_ref(text: str, emitting_sim: str) -> Optional[Tuple[str, str]]:
    """`sim:claim_id`, or a bare id resolving inside the emitting sim."""
    m = REF.match(text.strip())
    if not m:
        return None
    sim, cid = m.group(1), m.group(2)
    return (sim or emitting_sim, cid)


def is_literal(text: str) -> bool:
    return bool(DECIMAL_STR.match(text.strip()))


def validate(d: Dict[str, Any]) -> List[str]:
    """Problems with one raw record. Empty means it passes intake."""
    problems: List[str] = []
    for f in REQUIRED:
        if f not in d:
            problems.append("missing required field: %s" % f)
    if problems:
        return problems

    if not isinstance(d["value"], str):
        problems.append(
            "value must be a decimal STRING, never a float. got %s"
            % type(d["value"]).__name__)
    elif not DECIMAL_STR.match(d["value"].strip()):
        problems.append("value is not a decimal string: %r" % d["value"])

    try:
        prec = int(d["precision"])
        if prec < 1:
            problems.append("precision must be a positive integer")
    except (TypeError, ValueError):
        problems.append("precision is not an integer: %r" % d["precision"])

    try:
        prov = Provenance(str(d["provenance"]))
    except ValueError:
        problems.append("provenance not in %s"
                        % [p.value for p in DECLARABLE])
        return problems
    if prov is Provenance.DERIVED_WEAK:
        problems.append(
            "DERIVED_WEAK is resolved by the ledger and cannot be declared "
            "by an emitter")

    ops = d.get("operands") or []
    if not isinstance(ops, list):
        problems.append("operands must be a list")
        ops = []

    # The order's own intake rule.
    if prov is Provenance.DERIVED and not ops:
        problems.append(
            "a claim with no operands and provenance DERIVED fails intake")

    expr = d.get("expression")
    if prov is Provenance.DERIVED:
        if not expr:
            problems.append(
                "DERIVED requires an expression: operands alone do not say "
                "what was done with them, and the ledger will not choose")
        else:
            names = set(re.findall(r"[A-Za-z][A-Za-z0-9_:.-]*", str(expr)))
            declared = set(str(o).strip() for o in ops)
            unused = declared - names - set(
                o for o in declared if is_literal(o))
            undeclared = names - declared
            if undeclared:
                problems.append(
                    "expression uses names that are not declared operands: %s"
                    % sorted(undeclared))
            if unused:
                problems.append(
                    "operands declared but not used by the expression: %s"
                    % sorted(unused))
    if prov is not Provenance.DERIVED and expr:
        problems.append(
            "expression is only meaningful for DERIVED; %s carries one"
            % prov.value)

    for o in ops:
        o = str(o).strip()
        if is_literal(o):
            continue
        if parse_ref(o, str(d["sim"])) is None:
            problems.append("operand is neither a literal nor a reference: %r"
                            % o)
    return problems


def load_records(path: str) -> Tuple[List[ClaimRecord], List[Tuple[str, str]]]:
    """Every record under a directory tree. Returns (records, intake failures).

    An intake failure is a result. Nothing here raises on a bad file.
    """
    records: List[ClaimRecord] = []
    failures: List[Tuple[str, str]] = []
    if not os.path.isdir(path):
        return records, failures
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [x for x in dirnames if not x.startswith((".", "__"))]
        for fn in sorted(filenames):
            if not fn.endswith(".json"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, path)
            try:
                raw = json.loads(open(full, encoding="utf-8").read())
            except (ValueError, OSError) as e:
                failures.append((rel, "unreadable: %s" % e))
                continue
            items = raw if isinstance(raw, list) else [raw]
            for i, d in enumerate(items):
                if not isinstance(d, dict):
                    failures.append(("%s[%d]" % (rel, i), "not an object"))
                    continue
                problems = validate(d)
                if problems:
                    for p in problems:
                        failures.append(
                            ("%s[%d] %s" % (rel, i, d.get("claim_id", "?")), p))
                    continue
                rec = ClaimRecord.from_dict(d)
                rec.source = rel
                records.append(rec)
    return records, failures
