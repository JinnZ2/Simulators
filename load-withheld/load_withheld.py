"""
load_withheld.py -- record schema for demand deliberately kept off shared systems.
CC0. Co-authored. Stdlib only, parses under Python 3.9.

Every field is optional. An unfilled field is None and is never dropped: it
survives to_dict / to_json / from_json as None. None means UNKNOWN, not zero
and not False.

  python3 load_withheld.py              # print the seed cases as JSON
  python3 load_withheld.py FILE.json    # load and validate a case file

Checks: python3 test_load_withheld.py
"""
import json
import sys
from dataclasses import dataclass, fields, asdict
from typing import List, Optional

STATUS_TAGS = ("OBSERVED", "DERIVED", "PROPOSED")


@dataclass
class WithheldCase:
    case_id: Optional[str] = None
    date: Optional[str] = None
    region: Optional[str] = None
    shared_system: Optional[str] = None
    service_avoided: Optional[str] = None
    skill_or_tool_used: Optional[str] = None
    peak_condition: Optional[str] = None       # e.g. cold morning, outage
    withheld_by_choice: Optional[bool] = None
    eligible: Optional[bool] = None
    reason_stated: Optional[str] = None
    scope_limit: Optional[str] = None          # what would trigger asking for help
    fallback_if_fails: Optional[str] = None
    est_load_units: Optional[float] = None
    est_method: Optional[str] = None
    status_tag: Optional[str] = None           # OBSERVED | DERIVED | PROPOSED
    coupled_systems: Optional[List[str]] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.status_tag is not None and self.status_tag not in STATUS_TAGS:
            raise ValueError(f"status_tag {self.status_tag!r} not in {STATUS_TAGS}")
        for name in ("withheld_by_choice", "eligible"):
            v = getattr(self, name)
            if v is not None and not isinstance(v, bool):
                raise ValueError(f"{name} must be bool or None, got {v!r}")
        if self.est_load_units is not None and (
                isinstance(self.est_load_units, bool) or not isinstance(self.est_load_units, (int, float))):
            raise ValueError(f"est_load_units must be a number or None, got {self.est_load_units!r}")
        if self.est_load_units is not None and self.est_method is None:
            raise ValueError("est_load_units given without est_method")
        if self.coupled_systems is not None and not isinstance(self.coupled_systems, list):
            raise ValueError("coupled_systems must be a list or None")

    def to_dict(self):
        return asdict(self)      # every field, None kept

    @classmethod
    def from_dict(cls, d):
        known = {f.name for f in fields(cls)}
        extra = set(d) - known
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        return cls(**d)


FIELD_NAMES = tuple(f.name for f in fields(WithheldCase))


def to_json(cases):
    return json.dumps([c.to_dict() for c in cases], indent=1, ensure_ascii=True)


def from_json(text):
    return [WithheldCase.from_dict(d) for d in json.loads(text)]


def unfilled(case):
    """names of fields left None (UNKNOWN), in schema order"""
    return [n for n in FIELD_NAMES if getattr(case, n) is None]


# Seed cases: generic, no personal identifiers. All PROPOSED (not observed data).
SEED_CASES = [
    WithheldCase(
        case_id="seed-1", shared_system="truck yard tools",
        service_avoided="shared yard torch for frozen trailer landing gear",
        skill_or_tool_used="own mallet and torch",
        peak_condition="-40 morning; shared yard torches saturated",
        withheld_by_choice=True,
        scope_limit="gear still frozen after own tools; damage to the gear",
        fallback_if_fails="queue for a yard torch or call yard maintenance",
        status_tag="PROPOSED", coupled_systems=["yard maintenance", "dispatch schedule"]),
    WithheldCase(
        case_id="seed-2", shared_system="EMS",
        service_avoided="ambulance call for a minor hand injury",
        skill_or_tool_used="first aid treatment in place",
        withheld_by_choice=True,
        scope_limit="injury beyond first-aid scope (bleeding not controlled, function lost)",
        fallback_if_fails="self-transport to care",
        status_tag="PROPOSED", coupled_systems=["911 dispatch", "emergency department"]),
    WithheldCase(
        case_id="seed-3", shared_system="public benefits",
        service_avoided="benefit claim",
        skill_or_tool_used="adapted household practice",
        withheld_by_choice=True, eligible=True,
        status_tag="PROPOSED", coupled_systems=["take-up statistics"]),
    WithheldCase(
        case_id="seed-4", shared_system="GPS / ELD vendor support line",
        service_avoided="support call during a GPS or ELD outage",
        skill_or_tool_used="paper map and paper logs carried",
        peak_condition="vendor outage",
        withheld_by_choice=True,
        fallback_if_fails="call the support line",
        status_tag="PROPOSED", coupled_systems=["ELD vendor", "carrier compliance"]),
]


def main(argv):
    if "--selftest" in argv:
        print("load_withheld.py has no selftest; run: python3 test_load_withheld.py")
        return 2
    if argv:
        with open(argv[0], encoding="utf-8") as fh:
            cases = from_json(fh.read())
        for c in cases:
            print(f"{c.case_id}: {c.status_tag}  unfilled={len(unfilled(c))}/{len(FIELD_NAMES)}")
        return 0
    print(to_json(SEED_CASES))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
