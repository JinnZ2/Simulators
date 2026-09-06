#!/usr/bin/env python3
"""PART 2 -- substrate-neutral labor schema. Base layer records units of
work performed, substrate-agnostic; the framework goes in the READ layer,
not the collection layer. The invariants the work order calls load-bearing
are enforced in code, not just described:

  - exposure units are DECLARED per substrate class and NEVER converted
    across classes (conversion imports a valuation) -> convert_exposure raises
  - efficiency is TWO numbers (output_per_joule, output_per_exposure_hour),
    never collapsed to one -> combined_efficiency raises
  - capital stays OUT of the instrument (money is denominated in money, not
    in work performed) -> balance_on_capital raises
  - the allocation model (augmentation / substitution / oversight-limited)
    is a DECLARED field, never a design default; a record that omits it is
    flagged, not silently assumed augmentation

The joule denominator (metabolic / electrical / insolation) crosses all
classes with no convention, so output_per_joule is cross-class comparable;
output_per_exposure_hour is per-class only. Stdlib only, parses under 3.9.
"""

import sys
from dataclasses import dataclass, field
from typing import Optional

# exposure unit declared per class -- NOT universal, NOT convertible
EXPOSURE_UNIT = {
    "human": "person-hours",
    "machine": "substrate-hours",       # unit-hours under load
    "compute": "substrate-hours",
    "biological": "area-time-or-biomass-time",
    "animal": "animal-hours",
}
# the joule denominator type per class -- all are joules, so cross-class
JOULE_TYPE = {
    "human": "metabolic", "animal": "metabolic",
    "machine": "electrical", "compute": "electrical",
    "biological": "insolation-captured", "plant": "insolation-captured",
}
ALLOCATION_MODELS = ("augmentation", "substitution", "oversight-limited")


class ExposureConversion(Exception):
    """Raised on any attempt to convert exposure across substrate classes --
    it imports a valuation the instrument refuses to make."""


class CapitalImport(Exception):
    """Raised on any attempt to balance the instrument on capital -- money is
    denominated in money, not in work performed."""


class EfficiencyCollapse(Exception):
    """Raised on any attempt to collapse the two efficiency numbers into one."""


@dataclass
class WorkRecord:
    unit_identity: str
    substrate_class: str
    exposure: float                     # in the class's own unit
    load_factor: float
    task_class: str
    output_delivered: float
    joules_in: float
    error_rate_under_load: Optional[float] = None   # substrate fatigue signature
    allocation_model: Optional[str] = None          # DECLARED, never defaulted

    def exposure_unit(self):
        return EXPOSURE_UNIT.get(self.substrate_class, "UNDECLARED")

    def joule_type(self):
        return JOULE_TYPE.get(self.substrate_class, "UNDECLARED")


def output_per_joule(rec):
    """Cross-class comparable: joules are the substrate-neutral denominator."""
    if rec.joules_in <= 0:
        return None
    return rec.output_delivered / rec.joules_in


def output_per_exposure_hour(rec):
    """PER-CLASS ONLY -- the exposure unit is declared, not convertible, so
    this number does not compare across substrate classes."""
    if rec.exposure <= 0:
        return None
    return rec.output_delivered / rec.exposure


def efficiency(rec):
    """The two numbers, reported separately. There is no third, combined
    number: see combined_efficiency, which refuses."""
    return {"output_per_joule": output_per_joule(rec),
            "output_per_exposure_hour": output_per_exposure_hour(rec),
            "exposure_unit": rec.exposure_unit(), "joule_type": rec.joule_type()}


def combined_efficiency(rec):
    raise EfficiencyCollapse(
        "efficiency is two numbers (output_per_joule crosses classes; "
        "output_per_exposure_hour is per-class) and is never collapsed to one; "
        "combining them imports a conversion between a joule and an exposure hour")


def convert_exposure(rec, to_class):
    raise ExposureConversion(
        "exposure is declared in %r (%s) and is not convertible to %r (%s); "
        "conversion between exposure units imports a valuation"
        % (rec.substrate_class, rec.exposure_unit(), to_class,
           EXPOSURE_UNIT.get(to_class, "?")))


def balance_on_capital(*_a, **_k):
    raise CapitalImport(
        "capital stays out of the instrument; money is denominated in money "
        "(price levels, depreciation schedules, book vs market), none of which "
        "is about work performed")


def allocation_declared(rec):
    """A record's allocation model must be declared; None is flagged, never
    defaulted to augmentation. An instrument that assumes augmentation cannot
    detect substitution, and vice versa."""
    return rec.allocation_model in ALLOCATION_MODELS


def money_vs_joule_rank(operations):
    """DEMONSTRATION on constructed operations (not real hyperaccumulator
    data -- that is GAP 2). Each op: {name, output, joules_in, hours, price}.
    A money index prices free diffuse input (insolation) at zero and prices
    time, so it can rank an operation opposite to a joule index. Returns both
    rankings so the flip is visible; the denominator does the work."""
    money = sorted(operations, key=lambda o: o["output"] / o["price"], reverse=True)
    joule = sorted(operations, key=lambda o: o["output"] / o["joules_in"], reverse=True)
    return {"by_money": [o["name"] for o in money],
            "by_joule": [o["name"] for o in joule]}


def complementarity(records, task_class):
    """READ-LAYER query the instrument is built for: for a task_class, does
    COMBINED output-per-joule beat either substrate alone? Records tagged
    substrate_class 'combined' are the joint operation. Returns the per-class
    output_per_joule and whether combined beats the max of the singles -- the
    joule column separates genuine complementarity from one substrate
    subsidizing another's inefficiency. No theory attached."""
    rows = [r for r in records if r.task_class == task_class]
    per_class = {}
    for r in rows:
        opj = output_per_joule(r)
        if opj is not None:
            per_class[r.substrate_class] = opj
    combined = per_class.get("combined")
    singles = {k: v for k, v in per_class.items() if k != "combined"}
    beats = (combined is not None and singles
             and combined > max(singles.values()))
    return {"task_class": task_class, "per_class_output_per_joule": per_class,
            "combined_beats_either_alone": bool(beats),
            "best_single": max(singles.values()) if singles else None,
            "combined": combined}


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("labor_schema has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("PART 2 substrate-neutral labor schema -- import WorkRecord and the "
          "read-layer queries. Run selftest.py for the checks.", file=sys.stderr)
    sys.exit(2)
