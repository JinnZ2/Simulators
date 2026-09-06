# SPDX-License-Identifier: CC0-1.0
"""
The routing data-layer envelope as a structured object.

The marker states what the data layer must contain (R1-R10), the failure
classes observed in service (F1-F7), and a claim table (RDL-1..RDL-7) each
carrying a REFUTED-IF condition. This file encodes those as structured data
with two enforced rules:

  - every required content carries a RECORD STATE -- INCOMPLETE (a reporting
    chain exists and could be funded) or NEVER_CREATED (no originating record
    anywhere). R8 (per-door dock geometry) and R9 (per-field update latency)
    are NEVER_CREATED: paying to close them means paying to CREATE a record
    that has never existed. This is the `uninstrumented` / `generation-
    capacity` distinction -- an absence built into the instrument, not a gap.
  - every claim carries a refutation condition. `validate_claim` refuses a
    claim with no REFUTED-IF, the `falsifier-audit` discipline: a claim with
    no falsifier is a position, not a claim.

Nothing here is a result. No DOT feed, dock-geometry dataset, or routing
output is read (all egress-blocked); every failure-class instance is carried
from the marker, not verified.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

INCOMPLETE = "INCOMPLETE"          # a reporting chain exists; fundable
NEVER_CREATED = "NEVER_CREATED"    # no originating record anywhere
RECORD_STATES = (INCOMPLETE, NEVER_CREATED)


class IncompleteClaim(Exception):
    """Raised when a claim carries no refutation condition -- a claim with no
    falsifier is a position, not a claim."""


class BadRecordState(Exception):
    pass


@dataclass(frozen=True)
class Required:
    rid: str
    name: str
    record_state: str
    note: str = ""


REQUIRED: Tuple[Required, ...] = (
    Required("R1", "road existence and current geometry", INCOMPLETE),
    Required("R2", "structure existence and status (bridges, overpasses)",
             INCOMPLETE),
    Required("R3", "vertical clearance, per structure, current", INCOMPLETE),
    Required("R4", "weight limits, per segment, incl. seasonal variation",
             INCOMPLETE),
    Required("R5", "truck-route designation, per segment", INCOMPLETE),
    Required("R6", "exit / ramp existence and current closure state",
             INCOMPLETE),
    Required("R7", "active construction: closures, lane shifts, detours",
             INCOMPLETE),
    Required("R8", "dock geometry, per door: line offset, approach, surface",
             NEVER_CREATED,
             "no central record of per-door geometry exists"),
    Required("R9", "update latency per field, per jurisdiction",
             NEVER_CREATED,
             "no originating record of per-field latency"),
    Required("R10", "provenance and confidence per record", INCOMPLETE),
)


@dataclass(frozen=True)
class FailureClass:
    fid: str
    name: str
    instance: str            # carried from the marker, not verified


FAILURE_CLASSES: Tuple[FailureClass, ...] = (
    FailureClass("F1", "nonexistent infrastructure still routed over",
                 "bridge cases in the Minneapolis and Milwaukee metros"),
    FailureClass("F2", "closed segment shown open",
                 "Black Dog Road and Cliff Road shown open, not open"),
    FailureClass("F3", "nonexistent exit / ramp assigned",
                 "I-794, Milwaukee -- routed to an exit that does not exist"),
    FailureClass("F4", "non-truck-route assignment",
                 "segments not designated for commercial vehicles"),
    FailureClass("F5", "restriction not held",
                 "vertical / weight restrictions absent or stale"),
    FailureClass("F6", "independent systems disagree, both wrong",
                 "trucking nav and a shipper's mandated app returned "
                 "different routings, both wrong, errors in different "
                 "directions -- the load-bearing class"),
    FailureClass("F7", "per-dock geometry unavailable",
                 "painted dock line offsets ~2-3 in, asymmetric L vs R; no "
                 "central record"),
)


@dataclass(frozen=True)
class Claim:
    cid: str
    claim: str
    refuted_if: str

    def falsifiable(self) -> bool:
        return bool(self.refuted_if)


CLAIMS: Tuple[Claim, ...] = (
    Claim("RDL-1",
          "required layer (R1-R10) is not held complete by any party for the "
          "operating region",
          "a complete record is produced for any state in region"),
    Claim("RDL-2",
          "F1-F6 are not vendor maintenance defects; the source record is "
          "incomplete upstream of vendors",
          "a single-vendor fix closes F6 without new field survey"),
    Claim("RDL-3",
          "R8 has no record anywhere; it exists only as operator reading",
          "a per-door geometry dataset is located"),
    Claim("RDL-4",
          "update origination requires county and municipal reporting not "
          "funded or staffed at the rate road state changes",
          "a funded, staffed per-jurisdiction reporting function is "
          "demonstrated"),
    Claim("RDL-5",
          "the cost to close is STANDING, not capital: it recurs with each "
          "construction season and grows with network size",
          "a one-time survey holds accuracy across a full freeze-thaw and "
          "construction cycle"),
    Claim("RDL-6",
          "overhead sensing does not close the gap: it returns ground "
          "surface, not road STATE (closure, removal, coning, designation)",
          "canopy-penetrating sensing detects a removed structure at a "
          "stated error rate"),
    Claim("RDL-7",
          "the binding failure mode is NO LEGAL ACTION AVAILABLE, not wrong "
          "selection (committed lane, no shoulder, traffic behind)",
          "a safe action set at F1-F3 discovery is demonstrated in a dense "
          "urban committed-lane case"),
)


def validate_required(r: Required) -> None:
    if r.record_state not in RECORD_STATES:
        raise BadRecordState(
            "record_state of %s must be one of %r; got %r"
            % (r.rid, RECORD_STATES, r.record_state))


def validate_claim(c: Claim) -> None:
    if not c.falsifiable():
        raise IncompleteClaim(
            "claim %s carries no refutation condition; a claim with no "
            "falsifier is a position, not a claim" % c.cid)


def never_created() -> Tuple[str, ...]:
    """The contents absent by construction (paying to CREATE, not to fund an
    existing chain)."""
    return tuple(r.rid for r in REQUIRED if r.record_state == NEVER_CREATED)


if __name__ == "__main__":
    import sys
    sys.stderr.write("envelope.py is the structured spec; its checks live in "
                     "routing-data-layer/selftest_rdl.py.\n")
    sys.exit(2)
