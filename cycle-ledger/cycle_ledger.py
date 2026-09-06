# SPDX-License-Identifier: CC0-1.0
"""
DELIVERABLE 1 -- cycle_ledger.py.

Input: a cycle described as ordered elements. Output: the ledger, the
classification, and the unclosed set -- an instrument any party can run
against their OWN operation and get a number out.

The marker's finding is that almost nothing in the cycle is bound by decision
latency, so a faster decision layer cannot move it. The instrument reports
that as a number (the fraction of elements where `decision_latency_binds` is
TRUE) and carries the NULL: if a user's own cycle returns a nonzero AHEAD
count, the marker's reading is wrong for that operation and the tool says so
without hedging -- it can return "the claim holds here."

Seed data is ONE operator's corridor (Upper Midwest), marked so a user
REPLACES it rather than inherits it. Every classification is a reading carried
from the marker, not verified; no vendor API or map source is read (none is
available). Nothing here is a result about any other operation.

Output is plain text, readable without a terminal wider than 60 columns.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

HARDWARE = "HARDWARE"
TERMINAL = "TERMINAL"
COUNTERPARTY = "COUNTERPARTY"
ADMINISTRATIVE = "ADMINISTRATIVE"
SPATIAL = "SPATIAL"
DECISION = "DECISION"
RATE_SETTERS = (HARDWARE, TERMINAL, COUNTERPARTY, ADMINISTRATIVE, SPATIAL,
                DECISION)
TIED_SETTERS = (HARDWARE, TERMINAL, COUNTERPARTY, ADMINISTRATIVE, SPATIAL)

OPERATOR = "OPERATOR"
ABSORBERS = (OPERATOR, COUNTERPARTY, "NONE")


class BadElement(Exception):
    pass


@dataclass
class Element:
    element_id: str
    description: str
    rate_setter: str
    decision_latency_binds: bool = False
    currently_absorbed_by: str = "NONE"
    notated: bool = False
    parallel_with: Optional[str] = None
    relocation_target: Optional[str] = None
    fault_alternates: int = 0
    # required by outputs 3 and 2 respectively, beyond the record list:
    safety_relevant: bool = False
    recovery_leaving_vehicle: bool = False

    def is_tied(self) -> bool:
        return self.rate_setter in TIED_SETTERS

    def is_behind(self) -> bool:
        return (self.parallel_with is not None or self.fault_alternates > 0
                or self.recovery_leaving_vehicle)

    def is_ahead(self) -> bool:
        return self.decision_latency_binds


def validate_element(e: Element) -> None:
    if e.rate_setter not in RATE_SETTERS:
        raise BadElement("%s: rate_setter must be one of %r; got %r"
                         % (e.element_id, RATE_SETTERS, e.rate_setter))
    if e.currently_absorbed_by not in ABSORBERS:
        raise BadElement("%s: currently_absorbed_by must be one of %r; got %r"
                         % (e.element_id, ABSORBERS, e.currently_absorbed_by))
    # the record's own rule: decision_latency_binds TRUE only if DECISION
    if e.decision_latency_binds and e.rate_setter != DECISION:
        raise BadElement(
            "%s: decision_latency_binds is TRUE but rate_setter is %r, not "
            "DECISION" % (e.element_id, e.rate_setter))


# ---- Output 1: rate-setter histogram --------------------------------------

def rate_setter_histogram(elements: List[Element]) -> Dict[str, object]:
    counts = {s: 0 for s in RATE_SETTERS}
    for e in elements:
        counts[e.rate_setter] += 1
    n = len(elements)
    binds = sum(1 for e in elements if e.decision_latency_binds)
    return {"counts": counts, "n": n,
            "decision_binds_fraction": (binds / n) if n else None,
            "decision_binds_count": binds}


# ---- Output 2: TIED / BEHIND / AHEAD, and the NULL ------------------------

def classify(elements: List[Element]) -> Dict[str, object]:
    tied = sum(1 for e in elements if e.is_tied())
    behind = sum(1 for e in elements if e.is_behind())
    ahead = sum(1 for e in elements if e.is_ahead())
    return {"tied": tied, "behind": behind, "ahead": ahead,
            # the NULL: a nonzero AHEAD count means the claim holds HERE
            "claim_holds_here": ahead > 0}


# ---- Output 3: unnotated work register ------------------------------------

def unnotated_register(elements: List[Element]) -> Dict[str, object]:
    un = [e for e in elements if not e.notated]
    return {"elements": un, "total": len(un),
            "safety_relevant": [e.element_id for e in un if e.safety_relevant],
            "safety_count": sum(1 for e in un if e.safety_relevant)}


# ---- Output 4: relocation ledger ------------------------------------------

def relocation_ledger(elements: List[Element]) -> Dict[str, object]:
    """For every element absorbed by OPERATOR, group its relocation_target
    into standing functions. What leaves the sheet (wage lines) vs what
    arrives on it (standing functions)."""
    groups: Dict[str, List[str]] = {}
    wage_lines = []
    for e in elements:
        if e.currently_absorbed_by != OPERATOR:
            continue
        wage_lines.append(e.element_id)
        target = e.relocation_target or "UNASSIGNED"
        groups.setdefault(target, []).append(e.element_id)
    return {"wage_lines_leaving": wage_lines,
            "standing_functions_arriving": groups}


# ---- Output 5: serial-interface condition ---------------------------------

def serial_interface_condition(elements: List[Element]) -> Dict[str, object]:
    terminals = [e for e in elements if e.rate_setter == TERMINAL]
    conditions = [(e.element_id,
                   "rebuild %s as a parallel interface" % e.element_id)
                  for e in terminals]
    return {"terminals": [e.element_id for e in terminals],
            "conditions": conditions,
            "precondition": ("the saving claim requires %d serial interface(s) "
                             "rebuilt as parallel" % len(terminals))}


# --------------------------------------------------------------------------
# SEED -- ONE operator's corridor, Upper Midwest. REPLACE, do not inherit.
# decision_latency_binds is FALSE throughout: the marker's reading is that
# nothing in this cycle is decision-bound, so AHEAD == 0 here.
# --------------------------------------------------------------------------

def _seed() -> List[Element]:
    E = Element
    return [
        E("fuel_terminal", "fuel island serial terminal, per-field accept",
          TERMINAL, currently_absorbed_by=OPERATOR, notated=False,
          relocation_target="fueling operations"),
        E("gate", "gate guard check-in and door assignment",
          COUNTERPARTY, currently_absorbed_by=COUNTERPARTY, notated=False,
          relocation_target="gate / security operations"),
        E("yard_transit", "yard transit, clearance-bound",
          SPATIAL, currently_absorbed_by=OPERATOR, notated=True,
          relocation_target="yard movement operations"),
        E("backing", "backing to dock, single attempt, no retry margin",
          SPATIAL, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True, relocation_target="spotter / yard automation"),
        E("landing_gear", "landing gear crank, load transfer",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          relocation_target="coupling / mechanic operations"),
        E("airlines", "brake airline connect, air",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True,
          relocation_target="coupling / mechanic operations"),
        E("fifth_wheel", "fifth wheel couple, load transfer",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True,
          relocation_target="coupling / mechanic operations"),
        E("dock_approach", "dock approach assessment, clearance-bound",
          SPATIAL, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True, relocation_target="spotter / yard automation"),
        E("tire_inspection", "tire condition inspection",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True, relocation_target="inspection / maintenance"),
        E("lamp_crosscheck", "lamp cross-validation",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True, relocation_target="inspection / maintenance"),
        E("receiving_buzzer", "receiving buzzer wait, receiver-bound",
          COUNTERPARTY, currently_absorbed_by=COUNTERPARTY, notated=False,
          relocation_target="receiving / dock operations"),
        E("paperwork", "paperwork, per-field accept cycle",
          TERMINAL, currently_absorbed_by=OPERATOR, notated=True,
          relocation_target="documentation operations"),
        E("dead_wait_recovery", "dead-wait recovery, leaves the vehicle",
          COUNTERPARTY, currently_absorbed_by=OPERATOR, notated=False,
          recovery_leaving_vehicle=True,
          relocation_target="dispatch / recovery operations"),
        E("close_out_overlap", "close-out done inside the paperwork window",
          TERMINAL, currently_absorbed_by=OPERATOR, notated=False,
          parallel_with="paperwork",
          relocation_target="documentation operations"),
        E("fault_workarounds", "held workarounds for known failure modes",
          HARDWARE, currently_absorbed_by=OPERATOR, notated=False,
          fault_alternates=3, relocation_target="maintenance operations"),
        E("kingpin_verification", "kingpin verification, 5 swaps/day",
          SPATIAL, currently_absorbed_by=OPERATOR, notated=False,
          safety_relevant=True,
          relocation_target="coupling / mechanic operations"),
    ]


SEED = _seed()
SEED_NOTE = ("SEED = ONE operator's corridor, Upper Midwest. Replace it with "
             "your own cycle; do not inherit it.")


def _wrap(s: str, width: int = 57) -> List[str]:
    # 57 so a 3-space-indented wrapped line lands at <= 60 columns.
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def render(elements: List[Element]) -> str:
    """Plain text, every line <= 60 columns."""
    L = ["CYCLE LEDGER  (columns <= 60)", "=" * 30, ""]
    for s in _wrap(SEED_NOTE):
        L.append(s)
    L.append("")
    h = rate_setter_histogram(elements)
    L.append("1. RATE-SETTER HISTOGRAM")
    for s in RATE_SETTERS:
        L.append("   %-14s %d" % (s, h["counts"][s]))
    frac = h["decision_binds_fraction"]
    L.append("   decision-latency-binds: %d/%d = %s"
             % (h["decision_binds_count"], h["n"],
                "--" if frac is None else "%.2f" % frac))
    if frac == 0.0:
        for s in _wrap("KEY READOUT: fraction ~0, so a faster decision "
                       "layer cannot move this cycle."):
            L.append("   " + s)
    L.append("")
    c = classify(elements)
    L.append("2. TIED / BEHIND / AHEAD")
    L.append("   TIED   %d" % c["tied"])
    L.append("   BEHIND %d" % c["behind"])
    L.append("   AHEAD  %d" % c["ahead"])
    if c["ahead"] == 0:
        L.append("   AHEAD is empty: the claim's required support")
        L.append("   is absent for this cycle.")
    else:
        L.append("   AHEAD nonzero: the claim holds here.")
    L.append("")
    u = unnotated_register(elements)
    L.append("3. UNNOTATED WORK  (total %d, safety %d)"
             % (u["total"], u["safety_count"]))
    for e in u["elements"]:
        mark = " *safety" if e.safety_relevant else ""
        L.append("   %-20s%s" % (e.element_id, mark))
    L.append("")
    r = relocation_ledger(elements)
    L.append("4. RELOCATION LEDGER")
    L.append("   wage lines leaving: %d" % len(r["wage_lines_leaving"]))
    L.append("   standing functions arriving:")
    for fn in sorted(r["standing_functions_arriving"]):
        L.append("   - %s (%d)"
                 % (fn[:40], len(r["standing_functions_arriving"][fn])))
    L.append("")
    si = serial_interface_condition(elements)
    L.append("5. SERIAL-INTERFACE CONDITION")
    for eid, cond in si["conditions"]:
        for s in _wrap("%s: %s" % (eid, cond)):
            L.append("   " + s)
    for s in _wrap(si["precondition"]):
        L.append("   " + s)
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("cycle_ledger.py runs; its checks live in "
                         "cycle-ledger/selftest_cll.py.\n")
        sys.exit(2)
    print(render(SEED))
