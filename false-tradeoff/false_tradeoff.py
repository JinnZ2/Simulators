# false_tradeoff.py
# CC0 1.0 Universal / public domain dedication.
#
# Diagnostic for apparent dilemmas. Stdlib only. No network. Python 3.
#
# MEASURAND
#   Given a problem stated as a tradeoff between side A and side B,
#   whether the tradeoff is a property of the system or an artifact of
#   how the problem was posed.
#
# THIS INSTRUMENT DOES NOT RESOLVE TRADEOFFS. IT CLASSIFIES THEM.
#   Nothing here weights, ranks, prefers or recommends a side. The
#   structural guarantee is stronger than the promise: swapping A and B
#   leaves the flag set identical, asserted in test_tradeoff.py over
#   every case. A reader wanting to know which side ought to win will
#   not find it here, and that is the specification.
#
# NOTHING IS INFERRED FROM PROSE
#   The statement string is carried and never read. Structure is
#   supplied. A field not supplied is None and the read degrades; it is
#   never guessed from the sentence.
#
# ABSENT IS NOT CLEAN
#   An unevaluable check reports NOT_EVALUABLE and contributes
#   INSUFFICIENT. It never reports a silent pass, because a check that
#   could not run and a check that ran and found nothing are different
#   results and only one of them is evidence.

from enum import Enum
from typing import NamedTuple, Optional


class Provenance(Enum):
    OBSERVED = "OBSERVED"
    STIPULATED = "STIPULATED"
    DERIVED = "DERIVED"


class ConstraintKind(Enum):
    PHYSICAL = "PHYSICAL"
    RULE = "RULE"
    UNSTATED = "UNSTATED"


class TradeoffRead(Enum):
    STIPULATED_OPTION_SET = "STIPULATED_OPTION_SET"
    RULE_BOUND = "RULE_BOUND"
    BOUNDARY_ARTIFACT = "BOUNDARY_ARTIFACT"
    DEFERRAL_ARTIFACT = "DEFERRAL_ARTIFACT"
    GENUINE_TRADEOFF = "GENUINE_TRADEOFF"
    INSUFFICIENT = "INSUFFICIENT"


NOT_EVALUABLE = "NOT_EVALUABLE"


# [CHOICE 1] Horizons arrive as an amount and a unit. The order writes
# them as prose ("one quarter", "ten years"), and prose cannot be
# ordered, so CHECK 4's "beyond horizon_A" has no meaning until the two
# are on one scale. Days, declared, with no unit resolved by assumption:
# an unregistered unit raises rather than defaulting.
UNIT_DAYS = {
    "day": 1.0,
    "week": 7.0,
    "month": 30.4375,
    "quarter": 91.3125,
    "year": 365.25,
}


class UnregisteredUnit(Exception):
    """A duration whose unit is not on the declared table."""


class Horizon(NamedTuple):
    amount: float
    unit: str

    def days(self):
        if self.unit not in UNIT_DAYS:
            raise UnregisteredUnit(
                "unit %r is not on the declared table %s; a duration is not "
                "ordered by assumption" % (self.unit, sorted(UNIT_DAYS))
            )
        return float(self.amount) * UNIT_DAYS[self.unit]


class Option(NamedTuple):
    label: str
    provenance: Provenance
    source: str


class Constraint(NamedTuple):
    kind: ConstraintKind
    text: str


class DeferredCost(NamedTuple):
    """A cost said to reappear at a stated time, on a stated side.

    [CHOICE 2] CHECK 4 asks whether "A's saving reappears as a cost
    inside A's own boundary beyond horizon_A", and §2 supplies no field
    carrying that. Two things the check needs are therefore declared per
    cost -- WHEN it lands and on WHICH entity -- so both halves of the
    test read supplied data and neither is inferred.
    """
    side: str          # "A" or "B"
    entity: str
    at_time: Horizon


class Dilemma(NamedTuple):
    statement: str
    options: Optional[list]
    side_a: Optional[str]
    side_b: Optional[str]
    constraints: Optional[list]
    boundary_a: Optional[frozenset]
    boundary_b: Optional[frozenset]
    # [CHOICE 3] CHECK 3 reads "the dependency set of BOTH sides", which
    # §2 does not supply. Reading the boundary as the dependency set
    # makes the check unable to fire at all -- see
    # boundary_as_dependency_is_silent() -- so the dependency set is a
    # separate declared field and an absent one is NOT_EVALUABLE.
    depends_a: Optional[frozenset] = None
    depends_b: Optional[frozenset] = None
    horizon_a: Optional[Horizon] = None
    horizon_b: Optional[Horizon] = None
    deferred_costs: Optional[list] = None
    # Carried and reported. NOT gated on -- see the note at
    # check_conserved_is_not_gated().
    conserved_quantity: Optional[str] = None


def dilemma(statement, options=None, side_a=None, side_b=None,
            constraints=None, boundary_a=None, boundary_b=None,
            depends_a=None, depends_b=None, horizon_a=None, horizon_b=None,
            deferred_costs=None, conserved_quantity=None):
    def fz(s):
        return None if s is None else frozenset(s)
    return Dilemma(statement, options, side_a, side_b, constraints,
                   fz(boundary_a), fz(boundary_b), fz(depends_a), fz(depends_b),
                   horizon_a, horizon_b, deferred_costs, conserved_quantity)


# --------------------------------------------- CHECK 1, option provenance

def check_option_provenance(d):
    """Every option STIPULATED and no OBSERVED option: the set was handed
    over, not found. The trolley case."""
    out = {"check": "option_set_provenance", "evaluable": False,
           "fired": False, "missing": []}
    if d.options is None:
        out["missing"].append("options")
        out["state"] = NOT_EVALUABLE
        return out
    if not d.options:
        # An empty option list is NOT_EVALUABLE where an empty constraint
        # list is evaluable-and-silent, and the asymmetry is deliberate:
        # a dilemma with no eliminating constraint is a coherent state
        # (nobody ruled anything out), a dilemma with no options is not a
        # stated tradeoff at all.
        out["missing"].append("options (empty list)")
        out["state"] = NOT_EVALUABLE
        return out
    out["evaluable"] = True
    kinds = [o.provenance for o in d.options]
    all_stipulated = all(k is Provenance.STIPULATED for k in kinds)
    no_observed = not any(k is Provenance.OBSERVED for k in kinds)
    out["all_stipulated"] = all_stipulated
    # Reported separately because the two clauses of CHECK 1 are not
    # independent: all-STIPULATED already entails no-OBSERVED. The second
    # clause carries information only on a mixed set containing DERIVED
    # and no OBSERVED, which does NOT fire as written. The count is here
    # so that state is visible without changing the rule.
    out["no_observed_option"] = no_observed
    out["provenance_counts"] = {p.name: sum(1 for k in kinds if k is p)
                                for p in Provenance}
    out["fired"] = all_stipulated and no_observed
    out["state"] = "FIRED" if out["fired"] else "SILENT"
    return out


# ------------------------------------------------- CHECK 2, branch back

def check_branch_back(d):
    """Type every eliminating constraint. All RULE: the dilemma is not
    about the world. Any UNSTATED: a defect, reported."""
    out = {"check": "branch_back", "evaluable": False, "fired": False,
           "defects": [], "missing": []}
    if d.constraints is None:
        out["missing"].append("constraints")
        out["state"] = NOT_EVALUABLE
        return out
    out["evaluable"] = True
    kinds = [c.kind for c in d.constraints]
    out["kind_counts"] = {k.name: sum(1 for x in kinds if x is k)
                          for k in ConstraintKind}
    out["defects"] = [c.text for c in d.constraints
                      if c.kind is ConstraintKind.UNSTATED]
    # An empty list is a supplied value: nobody named an eliminating
    # constraint. all([]) is True, so the unguarded rule would report a
    # dilemma held by nothing as held entirely by permission.
    out["no_constraints"] = (len(kinds) == 0)
    out["fired"] = bool(kinds) and all(k is ConstraintKind.RULE for k in kinds)
    out["state"] = "FIRED" if out["fired"] else "SILENT"
    return out


# ------------------------------------------------ CHECK 3, boundary cut

def check_boundary_cut(d):
    """An entity both sides depend on, counted in one ledger and not the
    other: the cut runs through one system."""
    out = {"check": "boundary_cut", "evaluable": False, "fired": False,
           "missing": []}
    for name in ("depends_a", "depends_b", "boundary_a", "boundary_b"):
        if getattr(d, name) is None:
            out["missing"].append(name)
    if out["missing"]:
        out["state"] = NOT_EVALUABLE
        return out
    out["evaluable"] = True
    shared = d.depends_a & d.depends_b
    through = sorted(e for e in shared
                     if (e in d.boundary_a) != (e in d.boundary_b))
    # Both sides depend on it and neither ledger counts it. CHECK 3 tests
    # the exclusive case only, so this set is reported and does not fire.
    neither = sorted(e for e in shared
                     if e not in d.boundary_a and e not in d.boundary_b)
    out["shared_dependencies"] = sorted(shared)
    out["cut_runs_through"] = through
    out["shared_in_neither_ledger"] = neither
    out["fired"] = bool(through)
    out["state"] = "FIRED" if out["fired"] else "SILENT"
    return out


def boundary_as_dependency_is_silent():
    """Why CHECK 3 needs a field §2 does not supply.

    Read the boundary as the dependency set and shared becomes
    boundary_a & boundary_b, so every shared entity is inside both by
    construction and the exclusive test is false for all of them. The
    check could then never fire at any input. Demonstrated rather than
    argued.
    """
    trials = [
        (frozenset("abc"), frozenset("bcd")),
        (frozenset(), frozenset("x")),
        (frozenset("qrs"), frozenset("qrs")),
        (frozenset("m"), frozenset("nop")),
    ]
    fired = 0
    for ba, bb in trials:
        shared = ba & bb
        if any((e in ba) != (e in bb) for e in shared):
            fired += 1
    return {"trials": len(trials), "ever_fired": fired,
            "reading": "boundary read as the dependency set",
            "note": "the check is silent at every input under this reading"}


# ------------------------------------------- CHECK 4, horizon / deferral

def check_horizon_deferral(d):
    """Mismatched horizons, and a saving that reappears as a cost inside
    the same side's own boundary beyond that side's horizon."""
    out = {"check": "horizon_deferral", "evaluable": False, "fired": False,
           "missing": []}
    for name in ("horizon_a", "horizon_b", "boundary_a", "boundary_b",
                 "deferred_costs"):
        if getattr(d, name) is None:
            out["missing"].append(name)
    if out["missing"]:
        out["state"] = NOT_EVALUABLE
        return out
    out["evaluable"] = True
    days_a, days_b = d.horizon_a.days(), d.horizon_b.days()
    mismatch = days_a != days_b
    out["horizon_days"] = {"A": days_a, "B": days_b}
    out["horizon_mismatch"] = mismatch

    horizon = {"A": days_a, "B": days_b}
    ledger = {"A": d.boundary_a, "B": d.boundary_b}
    relocated = []
    for c in d.deferred_costs:
        if c.side not in horizon:
            raise ValueError("deferred cost names side %r, not A or B" % c.side)
        beyond = c.at_time.days() > horizon[c.side]
        inside = c.entity in ledger[c.side]
        if beyond and inside:
            relocated.append({"side": c.side, "entity": c.entity,
                              "at_days": c.at_time.days(),
                              "horizon_days": horizon[c.side]})
    out["relocated_past_horizon"] = relocated
    # CHECK 4 is gated on the horizons differing. A cost relocated past
    # BOTH matched horizons is reported here and does not fire, because
    # the gate is on the mismatch and not on the relocation.
    out["relocated_under_matched_horizons"] = (
        [] if mismatch else list(relocated))
    out["fired"] = mismatch and bool(relocated)
    out["state"] = "FIRED" if out["fired"] else "SILENT"
    return out


CHECKS = (check_option_provenance, check_branch_back,
          check_boundary_cut, check_horizon_deferral)

FLAG_OF = {
    "option_set_provenance": TradeoffRead.STIPULATED_OPTION_SET,
    "branch_back": TradeoffRead.RULE_BOUND,
    "boundary_cut": TradeoffRead.BOUNDARY_ARTIFACT,
    "horizon_deferral": TradeoffRead.DEFERRAL_ARTIFACT,
}


def read(d):
    """Return the SET of flags, the per-check record, and the defects.

    No priority ordering. No winner. No number anywhere that stands in
    for the set.
    """
    checks = [fn(d) for fn in CHECKS]
    flags = set()
    missing = []
    defects = []
    for c in checks:
        if c["fired"]:
            flags.add(FLAG_OF[c["check"]])
        if not c["evaluable"]:
            missing.extend("%s.%s" % (c["check"], m) for m in c["missing"])
        defects.extend(c.get("defects", []))

    # [CHOICE 4] §2 says an unsupplied field degrades the read to
    # INSUFFICIENT, and §4 says multiple flags may fire and the return is
    # the set. Read together: INSUFFICIENT joins whatever did evaluate
    # rather than replacing it, so a check that ran is not discarded
    # because a different one could not. The exclusive reading is also
    # available from the record, since intake_missing is empty exactly
    # when every check ran.
    all_evaluable = all(c["evaluable"] for c in checks)
    if not all_evaluable:
        flags.add(TradeoffRead.INSUFFICIENT)
    elif not flags:
        # Complete intake, nothing fired. CHECK 1-4 are the whole
        # instrument, so this is the whole condition.
        flags.add(TradeoffRead.GENUINE_TRADEOFF)

    return {
        "statement": d.statement,
        "sides": {"A": d.side_a, "B": d.side_b},
        "flags": sorted(flags, key=lambda f: f.name),
        "checks": {c["check"]: c for c in checks},
        # The order calls an UNSTATED constraint a defect that must be
        # reported and not smoothed over, and the return enum has no
        # member for it. It is reported here, where a caller reading only
        # the flag set will not see it.
        "unstated_constraint_defects": defects,
        "intake_missing": sorted(missing),
        "conserved_quantity": d.conserved_quantity,
        "units": dict(UNIT_DAYS),
    }


def swap_sides(d):
    """A and B exchanged. The flag set must not move."""
    return d._replace(
        side_a=d.side_b, side_b=d.side_a,
        boundary_a=d.boundary_b, boundary_b=d.boundary_a,
        depends_a=d.depends_b, depends_b=d.depends_a,
        horizon_a=d.horizon_b, horizon_b=d.horizon_a,
        deferred_costs=(None if d.deferred_costs is None else
                        [c._replace(side=("B" if c.side == "A" else "A"))
                         for c in d.deferred_costs]),
    )


def check_conserved_is_not_gated():
    """GENUINE_TRADEOFF's own definition names a condition no check tests.

    §4 defines it as "conserved quantity, same horizon, boundary intact".
    Same horizon is CHECK 4 and boundary intact is CHECK 3; the conserved
    quantity is tested by nothing. It is not added as a fifth gate,
    because a dilemma failing it would then have no member to return --
    the enum has six and none of them says "not conserved". The field is
    carried, reported, and named here instead.
    """
    return {"gated": False, "reported": True,
            "reason": "no enum member could carry the failing case"}


DECLARATION = {
    "measurand": "whether a stated tradeoff is structural or posed",
    "axes": ["option_provenance", "constraint_kind",
             "boundary_overlap", "horizon_mismatch"],
    "returns": [m.name for m in TradeoffRead],
    "resolves_tradeoffs": False,
    "scalar_collapse": False,
    "unknown_states": ["INSUFFICIENT"],
}


def render(records):
    lines = []
    head = "%-26s %-34s %s" % ("dilemma", "flags", "defects")
    lines.append(head)
    lines.append("-" * len(head))
    for r in records:
        lines.append("%-26s %-34s %s" % (
            str(r["statement"])[:26],
            ", ".join(f.name for f in r["flags"])[:34],
            len(r["unstated_constraint_defects"]) or "",
        ))
    lines.append("")
    lines.append("flags are a SET. no ordering, no winner, no side preferred.")
    lines.append("an UNSTATED constraint is a defect with no enum member;")
    lines.append("it is counted in the last column and nowhere in the flags.")
    for r in records:
        for text in r["unstated_constraint_defects"]:
            lines.append("  DEFECT  %-18s %s" % (str(r["statement"])[:18], text))
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.stderr.write(
            "false_tradeoff.py has no selftest. The checks live in "
            "test_tradeoff.py; run: python3 test_tradeoff.py\n")
        sys.exit(2)
    # Imported by name, NOT used as __main__. Running this file as a
    # script binds it as __main__ while cases.py imports it as
    # false_tradeoff, which builds two copies of every Enum; a member
    # from one copy is not the member from the other, so every `is`
    # comparison in the checks reads False and CHECK 1 and CHECK 2 go
    # silent. Found by running: four cases read GENUINE_TRADEOFF, which
    # is the direction the order warns about. Pinned in test_tradeoff.py
    # by running this path in a subprocess.
    import false_tradeoff as ft
    import cases
    records = [ft.read(d) for d in cases.CASES]
    print(ft.render(records))
    print()
    print("CHECK 3 under the boundary-as-dependency-set reading:")
    print("  %s" % ft.boundary_as_dependency_is_silent())
