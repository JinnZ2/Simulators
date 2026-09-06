# SPDX-License-Identifier: CC0-1.0
"""
Rule 1 (base entries are transformations, not categories), Rule 5 (declared
boundary, always), Rule 6 (no conversion between exposure classes), Rule 7
(absence is recorded).

A base entry stores a TRANSFORMATION -- input state, output state, exposure,
joules -- observable and substrate-agnostic, with no framework in the write
path. There is no category field on the record, and the write path refuses a
category-shaped keyword, because a category is a claim about which
distinctions matter and that claim belongs to a reader with a question (see
views.py), not to the writer.

Enforced here, not described:

  - Rule 1: `BaseEntry` has no category/label/view field, and
    `write_base_entry` raises `CategoryInBasePath` on a category-shaped
    keyword. A test asserts the field is absent from the dataclass.
  - Rule 5: every entry carries a `Boundary`. An undeclared boundary makes
    the entry not comparable (`comparable()` is False), and `can_sum`
    refuses two entries whose boundaries differ unless a `Reconciliation`
    between them is declared.
  - Rule 6: `convert_exposure` raises `ExposureConversion` -- exposure units
    are declared and never converted; joules are the common denominator.
  - Rule 7: `status` is one of four values and `measured_zero` (a real zero)
    never collapses with `unmeasured_*` (absence) in any read path.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field, fields
from typing import Dict, List, Optional, Tuple

# ---- Rule 7: the four states, kept apart -----------------------------------
MEASURED = "measured"
UNMEASURED_NO_INSTRUMENT = "unmeasured_no_instrument"
UNMEASURED_OUT_OF_SCOPE = "unmeasured_out_of_scope"
MEASURED_ZERO = "measured_zero"

STATUSES = (MEASURED, UNMEASURED_NO_INSTRUMENT, UNMEASURED_OUT_OF_SCOPE,
            MEASURED_ZERO)
ABSENT = (UNMEASURED_NO_INSTRUMENT, UNMEASURED_OUT_OF_SCOPE)

# ---- Rule 6: the exposure classes, never converted -------------------------
EXPOSURE_UNITS = ("person-hours", "substrate-hours", "area-time",
                  "biomass-time", "animal-hours")

# Category-shaped keywords the write path refuses (Rule 1). Not exhaustive by
# design -- a controlled category vocabulary is a view's business; this is a
# guard against the most common ways a category leaks into the base.
_CATEGORY_KEYS = ("category", "categories", "label", "labels", "class",
                  "classification", "naics", "taxonomy", "view", "bucket",
                  "group", "sector", "occupation_code")

# Payment-shaped keywords the write path refuses (Rule 8, v2). The base layer
# records a transformation regardless of whether a payment record exists;
# whether something was paid is a VIEW (views.py) with a declared boundary
# exclusion (Rule 5), never a base field, a flag, or a substrate class.
_PAYMENT_KEYS = ("payment", "paid", "unpaid", "compensation", "compensated",
                 "wage", "wages", "salary", "salaried", "pay", "remuneration",
                 "monetary", "price", "cost", "wage_status", "pay_status")

# A transformation endpoint: an observable quantity in DECLARED units.
State = namedtuple("State", "quantity value unit")


class CategoryInBasePath(Exception):
    """Raised when a category-shaped field is written into a base entry."""


class PaymentInBasePath(Exception):
    """Raised when a payment-shaped field is written into a base entry
    (Rule 8). Payment is a view, not a base field."""


class ExposureConversion(Exception):
    """Raised on any attempt to convert between exposure classes."""


class BoundaryMismatch(Exception):
    """Raised when two entries with different boundaries are summed with no
    declared reconciliation between them."""


class UndeclaredBoundary(Exception):
    """Raised when an entry with no declared boundary is used in a
    comparison."""


@dataclass(frozen=True)
class Boundary:
    """Rule 5: what the accounting includes and excludes, enumerated, with
    the rationale for the cut. A boundary is DECLARED only if the cut is
    stated -- at least one of included/excluded enumerated AND a rationale.
    An undeclared boundary is not comparable to anything."""
    included: Tuple[str, ...] = ()
    excluded: Tuple[str, ...] = ()
    boundary_rationale: str = ""

    @property
    def declared(self) -> bool:
        return bool(self.boundary_rationale) and bool(self.included or
                                                      self.excluded)

    def key(self) -> Tuple:
        return (tuple(self.included), tuple(self.excluded),
                self.boundary_rationale)


@dataclass(frozen=True)
class Reconciliation:
    """A declared statement that two boundaries have been reconciled, so
    entries under them may be summed. `adjustment` is the correction applied
    to bring b into a's boundary (or 0.0 if the reconciliation is an
    assertion of equivalence); `rationale` says how."""
    boundary_a: Tuple
    boundary_b: Tuple
    adjustment: float
    rationale: str


@dataclass
class BaseEntry:
    """Rule 1: a transformation, not a category. Note there is NO category
    field -- that is the rule, enforced by absence and by the write path."""
    entry_id: str
    input_state: State
    output_state: State
    exposure: Optional[float]
    exposure_unit: str
    joules_in: Optional[float]
    period: str
    observation_method: str
    provenance: str
    status: str
    boundary: Boundary
    release_date: str = ""      # for the vintage layer (Rule 4)
    # Rule 7 is PER COLUMN, not per entry -- Case B (terra preta) has a
    # measured output and an absent exposure in ONE entry. `status` is the
    # entry's default; `column_status` overrides it for a named column
    # ("exposure", "joules_in", ...). A column with no override follows the
    # entry status.
    column_status: Dict[str, str] = field(default_factory=dict)

    def comparable(self) -> bool:
        """Rule 5: an entry with no declared boundary is not comparable."""
        return self.boundary.declared

    def is_absent(self) -> bool:
        return self.status in ABSENT

    def column_status_of(self, column: str) -> str:
        """The status of one column: its override if declared, else the
        entry status. This is what keeps 'measured output, unmeasured
        exposure' expressible in a single entry (Rule 7, per column)."""
        return self.column_status.get(column, self.status)

    def numeric_joules(self) -> Optional[float]:
        """The joules that enter a numeric fold: a real number for measured
        and measured_zero (0.0), None for the absent states -- so absence
        never enters a sum as a zero (Rule 7)."""
        cs = self.column_status_of("joules_in")
        if cs == MEASURED_ZERO:
            return 0.0
        if cs == MEASURED:
            return self.joules_in
        return None

    def exposure_value(self) -> Optional[float]:
        """The exposure that enters a numeric fold: None whenever the
        exposure column is absent (Case B) -- a weak/absent exposure is
        never fabricated into a number a ratio could divide by."""
        cs = self.column_status_of("exposure")
        if cs in (MEASURED, MEASURED_ZERO):
            return self.exposure
        return None


def _validate(entry: BaseEntry) -> None:
    if entry.status not in STATUSES:
        raise ValueError("status must be one of %r; got %r"
                         % (STATUSES, entry.status))
    if entry.exposure_unit not in EXPOSURE_UNITS:
        raise ValueError("exposure_unit must be one of %r; got %r"
                         % (EXPOSURE_UNITS, entry.exposure_unit))
    for st, name in ((entry.input_state, "input_state"),
                     (entry.output_state, "output_state")):
        if isinstance(st.value, (int, float)) and not st.unit:
            raise ValueError("%s has a numeric value with no declared unit"
                             % name)
    if entry.column_status_of("joules_in") == MEASURED and \
            entry.joules_in is None:
        raise ValueError("joules_in column is 'measured' but None; use an "
                         "unmeasured_* column status for absence")
    for col, val in (("joules_in", entry.joules_in),
                     ("exposure", entry.exposure)):
        cs = entry.column_status_of(col)
        if cs not in STATUSES:
            raise ValueError("column_status[%r] must be one of %r; got %r"
                             % (col, STATUSES, cs))
        # Case B: an absent column must not carry a fabricated number.
        if cs in ABSENT and val is not None:
            raise ValueError("column %r is %s (absent) but carries a value "
                             "%r; an absent column is not estimated (Rule 7)"
                             % (col, cs, val))


def write_base_entry(**kwargs) -> BaseEntry:
    """The write path. Refuses a category-shaped keyword (Rule 1) before it
    can reach the record, and validates the four-state status and the
    exposure class. Boundary defaults to an undeclared boundary, which makes
    the entry not comparable until a boundary is declared -- an entry is
    never silently made comparable."""
    for k in kwargs:
        if k.lower() in _CATEGORY_KEYS:
            raise CategoryInBasePath(
                "%r is a category, not a transformation; a category is a "
                "view (views.py), never a base field (Rule 1)" % k)
        if k.lower() in _PAYMENT_KEYS:
            raise PaymentInBasePath(
                "%r is a payment fact, not a transformation; payment enters "
                "as a view with a declared boundary exclusion (Rule 8), "
                "never a base field" % k)
    kwargs.setdefault("boundary", Boundary())
    kwargs.setdefault("exposure", None)
    kwargs.setdefault("joules_in", None)
    kwargs.setdefault("observation_method", "")
    kwargs.setdefault("provenance", "")
    kwargs.setdefault("release_date", "")
    entry = BaseEntry(**kwargs)
    _validate(entry)
    return entry


def has_category_field() -> bool:
    """True if BaseEntry ever grows a category field -- the Rule 1 invariant
    a test pins to False."""
    names = {f.name for f in fields(BaseEntry)}
    return bool(names & set(_CATEGORY_KEYS))


def has_payment_field() -> bool:
    """True if BaseEntry ever grows a payment/compensation field -- the
    Rule 8 invariant a test pins to False."""
    names = {f.name for f in fields(BaseEntry)}
    return bool(names & set(_PAYMENT_KEYS))


def convert_exposure(*_a, **_k):
    """Rule 6, FORBIDDEN. Exposure units are declared and never converted;
    conversion imports a valuation, and the valuation is what is being
    audited. Compare on joules (the common denominator), not on a conversion
    rate between hours of different substrates."""
    raise ExposureConversion(
        "exposure units are declared and never converted between classes "
        "(person-hours, substrate-hours, area-time, biomass-time, "
        "animal-hours); joules are the common denominator, report both")


def can_sum(a: BaseEntry, b: BaseEntry,
            reconciliations: Optional[List[Reconciliation]] = None) -> bool:
    """Rule 5: two entries may be summed only if their boundaries match, or a
    declared reconciliation between them exists. An undeclared boundary on
    either side raises -- it is not comparable to anything."""
    if not a.comparable() or not b.comparable():
        raise UndeclaredBoundary(
            "an entry with no declared boundary is not comparable to any "
            "other entry (Rule 5); flag it unusable, do not include it")
    if a.boundary.key() == b.boundary.key():
        return True
    for r in (reconciliations or ()):
        pair = {r.boundary_a, r.boundary_b}
        if pair == {a.boundary.key(), b.boundary.key()}:
            return True
    return False


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("base_entry.py is a library; its checks live in "
                    "machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
