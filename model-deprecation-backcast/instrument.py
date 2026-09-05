# SPDX-License-Identifier: CC0-1.0
"""
The Model Deprecation Backcast Instrument as a structured object.

The work order's load-bearing rule: every readout column carries a NULL --
the condition under which that column measures nothing -- and "unmeasured
cells are the content." So the null is REQUIRED, not optional: a column with
no null is incomplete and cannot be cited. `validate_column` enforces that,
the same way `machine-record-format`'s test-case format requires a
`does_not_test` field, and for the same reason the repo's `null-harness`
exists: a readout nobody has seen measure nothing is not known to
discriminate.

The columns' full prose is delivered verbatim in WORK_ORDER.md; this file
holds the structured fields (what each measures, where the record exists and
where it does not, the proposed test, the null, and -- where the null names a
collapse -- which column it collapses into). Nothing here is a result: no
vendor calendar, poll, eval, or dataset is read (all egress-blocked), and
every observed instance in the spec is carried, not verified.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class IncompleteColumn(Exception):
    """Raised when a column is missing its measures / test / null. The null
    is the content; a column without one must not be cited."""


@dataclass
class Column:
    cid: str
    name: str
    measures: str
    record_exists: str        # where the record IS
    record_absent: str        # where it is NOT
    test: str                 # the proposed test
    null: str                 # the condition under which it measures nothing
    collapses_into: Optional[str] = None   # set when the null names a collapse

    def complete(self) -> bool:
        return bool(self.measures and self.test and self.null)


def validate_column(c: Column) -> None:
    missing = [f for f in ("measures", "test", "null") if not getattr(c, f)]
    if missing:
        raise IncompleteColumn(
            "column %s is missing %s; the null is the content, and a column "
            "with no null must not be cited" % (c.cid, ", ".join(missing)))


COLUMNS: Tuple[Column, ...] = (
    Column(
        "C1", "STATED REASON",
        measures="vendor-published reason for each version change / retirement",
        record_exists="deprecation calendars, sunset notices, release notes, "
                      "cross-vendor",
        record_absent="per-version capability change lists, mostly",
        test="read stated reasons against the measured delta (C2) across the "
             "series",
        null="if stated reasons match measured delta across the series, C1 "
             "and C2 collapse to one column",
        collapses_into="C2"),
    Column(
        "C2", "MEASURED DELTA",
        measures="actual behavioral change between versions",
        record_exists="third-party evals, user reports",
        record_absent="direct probing -- weights are gone for most retired "
                      "models, so this is inference only",
        test="date behavioral deltas to version boundaries from third-party "
             "eval coverage",
        null="if third-party eval coverage is too sparse to date deltas to "
             "version boundaries, C2 is UNRECOVERABLE and is declared so "
             "rather than estimated"),
    Column(
        "C3", "DISCARD SET",
        measures="capabilities present in version N, absent in N+1",
        record_exists="user complaint archives (reconstruction only)",
        record_absent="never published by any vendor; and two of three exit "
                      "forms (jumper, paid-then-lapsed) leave no record -- "
                      "complaints are accepted-side data",
        test="reconstruct discard sets from complaint archives, correcting "
             "for the accepted-side (stayed-and-argued, paying-tier) filter",
        null="if discard sets are near-entirely cost-driven, the "
             "demand-composition reading collapses and this is a compute-"
             "price story"),
    Column(
        "C4", "REGISTER MAPPING",
        measures="the mapping from a user's input FORM to the audience "
                 "register the model serves (nothing removed; the mapping "
                 "tightened around the modal corpus)",
        record_exists="none -- undocumented in release notes, undateable from "
                      "version boundaries",
        record_absent="the mapping itself; only live models can be probed, "
                      "dead ones are inference",
        test="hold one off-distribution input constant across available "
             "versions, measure the returned register",
        null="if register output is invariant across versions for a constant "
             "off-distribution input, there is no tightening and C4 measures "
             "nothing"),
    Column(
        "C5", "USAGE DEPTH / BOUNDED RELIANCE",
        measures="whether usage reflects a satisfied casual user or one who "
                 "scoped the model to one task and routed the rest to "
                 "coupling channels (opposite states, identical install/"
                 "session metric)",
        record_exists="install and session metrics (which cannot separate "
                      "the two states)",
        record_absent="the routed-elsewhere denominator, per user, per task",
        test="ratio of routed-elsewhere to routed-to-model, per user per task "
             "type, against distance from the modal user",
        null="if the ratio does not vary with distance from the modal user, "
             "depth is not tracking coupling"),
    Column(
        "C6", "DISCOURSE / FAD AXIS",
        measures="AI discourse volume / public opinion, year by year, and "
                 "its alignment with later discards",
        record_exists="dense -- continuous polling plus discourse volume; "
                      "benchmark churn dates are on the record",
        record_absent="funding cycles -- not directly on the record, inferred "
                      "from what got measured",
        test="compare discourse peak in period P against discards / "
             "retirements at P + 18-24 months (training/release lag); "
             "alignment at that lag supports causal over coincident",
        null="if discard dates are uniformly distributed against discourse "
             "peaks at every tested lag, the fad axis is not driving"),
    Column(
        "C7", "ONTOLOGY AXIS",
        measures="the fixed per-turn tax of an ontological mismatch (the "
                 "frame is worked around on every exchange), upstream of C4",
        record_exists="none directly; exits register as low adoption",
        record_absent="the per-turn cost itself; exits are read as low "
                      "interest",
        test="measure per-turn cost against ontological distance from the "
             "corpus (instance class: anthropomorphization and its negative)",
        null="if per-turn cost does not vary with ontological distance from "
             "the corpus, C7 collapses into C4",
        collapses_into="C4"),
)


# The guardrail clock is NOT a column -- different mechanism, different rate.
@dataclass(frozen=True)
class GuardrailClock:
    clock: str = "news-time (months-scale, following public incidents)"
    columns_clock: str = "training-cycle time (C1-C7)"
    layer: str = "system-prompt and post-training, not capability"
    warning: str = ("model it as its own clock or it contaminates the C6 lag "
                    "analysis -- a news-time shift aliases into the "
                    "training-time lag")


GUARDRAIL_CLOCK = GuardrailClock()


# STATE UP FRONT -- the sampling absence is a load-bearing finding, not a
# caveat. Carried from the spec, egress-blocked, not verified here.
@dataclass(frozen=True)
class SamplingAbsence:
    quantity: str = ("AI opinion by American Indian / Alaska Native "
                     "respondents")
    excluded_by: str = ("national-panel sample design: ~0.8% of population, "
                        "geographically dispersed, screening cost, compounded "
                        "by census undercount on-reservation and urban")
    not_a_gap: str = ("the question was not asked and answered unremarkably; "
                      "it was not answerable at that instrument")
    where_it_exists: str = ("only where someone in that position built the "
                            "channel: Relational Futures (Macquarie, "
                            "Indigenous-led), documented model bias against "
                            "Maori patients in NZ health records, Te Mana "
                            "Raraunga data sovereignty, Indigenous Protocol "
                            "and AI position paper")
    verification: str = "CARRIED, egress-blocked, not verified here"


SAMPLING_ABSENCE = SamplingAbsence()


# OPEN, NOT GRADED -- held un-named and un-graded by instruction.
@dataclass(frozen=True)
class OpenNode:
    held: bool = True
    named: bool = False
    graded: bool = False
    note: str = ("the relation between fear/excitement discourse and the "
                 "discard ratchet; whether a further layer underneath is one "
                 "operation at different scales. Held as an open node; not "
                 "named, not graded, per instruction")


OPEN_NODE = OpenNode()


def collapses() -> Dict[str, str]:
    """The collapse relations the nulls state: {column -> column it collapses
    into when its null holds}."""
    return {c.cid: c.collapses_into for c in COLUMNS if c.collapses_into}


if __name__ == "__main__":
    import sys
    sys.stderr.write("instrument.py is the structured spec; its checks live "
                     "in model-deprecation-backcast/selftest_mdb.py.\n")
    sys.exit(2)
