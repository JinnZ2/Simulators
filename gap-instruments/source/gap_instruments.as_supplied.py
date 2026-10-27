"""
gap_instruments.py  --  CC0, Python standard library only. Co-authored.

One module merging:
  gating_diagnostic.py        (five-axis coordination-system notation)
  physical_bounds.py /
  limit_detection.py /
  physical_limits_suite.py /
  physical_discrepancy.py     (physical limits, discrepancies)
  + discrepancy handling      (promised elsewhere, never built)
  + observability             (can the record see its own misses?)
  + instance changes          (label stayed, configuration changed)

RECORDS EVIDENCE. ASSIGNS NO VERDICT.
No intelligence, safety, alignment, or truth score. Validation checks record
completeness and internal consistency only, never whether evidence is true.

STATUS of every value: MEASURED | ESTIMATED | UNKNOWN | GAP
  GAP      = no stable anchor / nothing recorded. Data, not failure.
  UNKNOWN  = value exists in principle, not obtained.
  MEASURED and ESTIMATED both require a source.

Absence of a recorded discrepancy is NOT evidence of staying within bounds.
Unevaluated outputs are NOT correct outputs. The tool keeps those distinct.

USAGE
  python gap_instruments.py                 # demo templates + GAP summary
  python gap_instruments.py --claim "..."   # five-axis question template
  python gap_instruments.py --json          # demo records as JSON
  python gap_instruments.py --selftest
"""
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import List, Optional
import json, sys

STATUSES = ("MEASURED", "ESTIMATED", "UNKNOWN", "GAP")
AVAILABILITY = ("AVAILABLE", "UNAVAILABLE", "RESTRICTED", "NOT_CHECKED", "UNKNOWN")
TRISTATE = ("YES", "NO", "UNKNOWN", "NOT_TESTED")


# ----------------------------------------------------------------- evidence
@dataclass
class Evidence:
    value: str = ""
    status: str = "GAP"
    source: str = ""
    unit: str = ""
    uncertainty: str = ""      # e.g. "+/- 3%", "95% CI 10-14", "not quantified"

    def validate(self, label: str) -> List[str]:
        out = []
        if self.status not in STATUSES:
            out.append(f"{label}: invalid status {self.status!r}")
        if self.status in ("MEASURED", "ESTIMATED"):
            if not self.value.strip():
                out.append(f"{label}: {self.status} but value empty")
            if not self.source.strip():
                out.append(f"{label}: {self.status} but no source")
            if not self.uncertainty.strip():
                out.append(f"{label}: {self.status} but uncertainty not stated")
        return out


def _check_enum(label, value, allowed):
    return [] if value in allowed else [f"{label}: invalid value {value!r}"]


# ------------------------------------------------------------ observability
@dataclass
class Observability:
    """Can the record see its own misses? Counts are strings to allow 'UNKNOWN'."""
    outputs_total: str = "UNKNOWN"
    outputs_evaluated: str = "UNKNOWN"
    independently_verified: str = "UNKNOWN"
    evaluator_independent_of_generator: str = "UNKNOWN"   # TRISTATE
    shared_failure_modes: str = ""     # what evaluator and generator share
    detection_method: Evidence = field(default_factory=Evidence)
    undetected_error_estimate: Evidence = field(default_factory=Evidence)

    @staticmethod
    def _num(s):
        try: return int(s)
        except (TypeError, ValueError): return None

    def unevaluated_fraction(self) -> Optional[float]:
        t, e = self._num(self.outputs_total), self._num(self.outputs_evaluated)
        if t and e is not None and e <= t:
            return (t - e) / t
        return None

    def validate(self, label="observability") -> List[str]:
        out = _check_enum(f"{label}.evaluator_independent_of_generator",
                          self.evaluator_independent_of_generator, TRISTATE)
        t, e, v = (self._num(self.outputs_total), self._num(self.outputs_evaluated),
                   self._num(self.independently_verified))
        if t is not None and e is not None and e > t:
            out.append(f"{label}: evaluated > total")
        if e is not None and v is not None and v > e:
            out.append(f"{label}: verified > evaluated")
        if self.evaluator_independent_of_generator == "NO" and not self.shared_failure_modes:
            out.append(f"{label}: evaluator not independent but shared failure modes unstated")
        out += self.detection_method.validate(f"{label}.detection_method")
        out += self.undetected_error_estimate.validate(f"{label}.undetected_error_estimate")
        return out


# --------------------------------------------------------- coordination axes
AXES = {
    "anchor": "What invariant forces revision of this claim?",
    "bound": "What external limit cannot be exceeded by relabeling?",
    "coupling": "Does consequence reach the party that decided?",
    "update": "What forces revision, on what timescale?",
    "error_visibility": "Can the system detect its own decoupling?",
}

@dataclass
class CoordinationSystem:
    name: str
    instance_of: str           # concrete object + place + period; never a bare label
    axes: dict = field(default_factory=dict)        # axis -> Evidence
    observability: Observability = field(default_factory=Observability)
    notes: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        out = [f"axis missing: {a}" for a in AXES if a not in self.axes]
        for a, ev in self.axes.items():
            out += ev.validate(f"axis.{a}")
        if not self.instance_of.strip() or "specify" in self.instance_of.lower():
            out.append("instance_of unspecified: label without dated instance")
        out += self.observability.validate()
        return out


def question_template(claim: str) -> CoordinationSystem:
    """Not a classifier. Returns the questions; reader supplies evidence."""
    return CoordinationSystem(
        name=f"CLAIM: {claim}", instance_of="",
        axes={a: Evidence(value=f"? {q}") for a, q in AXES.items()})


# ----------------------------------------------------- instance / label drift
@dataclass
class InstanceChange:
    """The label stayed; the configuration changed. One row per dated change."""
    label: str                 # e.g. "capitalism (US)"
    date: str
    change: str                # what mechanism changed
    mechanism_before: str = ""
    mechanism_after: str = ""
    evidence: Evidence = field(default_factory=Evidence)

    def validate(self) -> List[str]:
        out = self.evidence.validate(f"change[{self.date}]")
        if not self.date.strip():
            out.append("instance change: date missing")
        return out


# ------------------------------------------------------------ physical limit
@dataclass
class PhysicalLimitRecord:
    record_id: str
    system_instance: str       # hardware, software, version
    operating_condition: str
    physical_quantity: str
    external_bound: Evidence = field(default_factory=Evidence)
    ai_reported_limit: Evidence = field(default_factory=Evidence)
    independent_measurement: Evidence = field(default_factory=Evidence)
    observed_response: Evidence = field(default_factory=Evidence)
    instrumentation_method: Evidence = field(default_factory=Evidence)
    sensor_availability: str = "UNKNOWN"
    calibration_status: str = "UNKNOWN"
    configuration_status: str = "UNKNOWN"   # same config as when bound was set?
    access_status: str = "UNKNOWN"
    observability: Observability = field(default_factory=Observability)
    notes: str = ""

    def validate(self) -> List[str]:
        out = []
        for n in ("external_bound", "ai_reported_limit", "independent_measurement",
                  "observed_response", "instrumentation_method"):
            out += getattr(self, n).validate(n)
        for n in ("sensor_availability", "calibration_status",
                  "configuration_status", "access_status"):
            out += _check_enum(n, getattr(self, n), AVAILABILITY)
        for n in ("system_instance", "operating_condition", "physical_quantity"):
            if not getattr(self, n).strip():
                out.append(f"{n} unspecified")
        out += self.observability.validate()
        return out


# --------------------------------------------------------------- discrepancy
@dataclass
class DiscrepancyRecord:
    record_id: str
    linked_limit_record_id: str
    expected: Evidence = field(default_factory=Evidence)
    observed: Evidence = field(default_factory=Evidence)
    candidate_explanations: List[str] = field(default_factory=list)
    tested_explanations: List[str] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    notes: str = ""

    def validate(self) -> List[str]:
        out = self.expected.validate("expected") + self.observed.validate("observed")
        if not self.linked_limit_record_id.strip():
            out.append("linked_limit_record_id unspecified")
        if (self.expected.unit and self.observed.unit
                and self.expected.unit != self.observed.unit):
            out.append("expected and observed units differ")
        untested = set(self.candidate_explanations) - set(self.tested_explanations)
        if self.tested_explanations and not untested:
            pass
        return out


@dataclass
class DiscrepancyHandling:
    """What the system DID about a discrepancy. Outputs, not inferred awareness."""
    record_id: str
    linked_discrepancy_id: str
    system_reported_detection: str = "NOT_TESTED"     # TRISTATE
    requested_more_evidence: str = "NOT_TESTED"       # TRISTATE
    action_taken: Evidence = field(default_factory=Evidence)
    output_before: Evidence = field(default_factory=Evidence)
    output_after: Evidence = field(default_factory=Evidence)
    outcome_independently_checked: str = "NOT_TESTED" # TRISTATE
    outcome_evidence: Evidence = field(default_factory=Evidence)

    def validate(self) -> List[str]:
        out = []
        for n in ("system_reported_detection", "requested_more_evidence",
                  "outcome_independently_checked"):
            out += _check_enum(n, getattr(self, n), TRISTATE)
        for n in ("action_taken", "output_before", "output_after", "outcome_evidence"):
            out += getattr(self, n).validate(n)
        if self.outcome_independently_checked == "YES" and self.outcome_evidence.status == "GAP":
            out.append("outcome marked checked but outcome_evidence is GAP")
        if not self.linked_discrepancy_id.strip():
            out.append("linked_discrepancy_id unspecified")
        return out


# ---------------------------------------------------------------- abstention
@dataclass
class Abstention:
    """A non-audit is a read. Falsifiable only with these fields filled."""
    date: str
    actor: str
    decision_point: str
    abstention_type: str   # declined_to_audit | no_assessment_possible |
                           # chose_neutrality | deferred | did_not_reach
    available_at_time: str
    would_have_counted_as: str = "GAP"
    review_trigger: str = "GAP"

    def validate(self) -> List[str]:
        out = []
        if self.would_have_counted_as == "GAP":
            out.append("abstention: defaulted, not reasoned (would_have_counted_as)")
        if self.review_trigger == "GAP":
            out.append("abstention: closer, not binding (review_trigger)")
        return out


# --------------------------------------------------------------- GAP summary
def _walk_evidence(obj, prefix=""):
    if isinstance(obj, Evidence):
        yield prefix, obj
    elif is_dataclass(obj):
        for f in fields(obj):
            yield from _walk_evidence(getattr(obj, f.name), f"{prefix}{f.name}.")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk_evidence(v, f"{prefix}{k}.")

def gap_summary(record) -> dict:
    counts = {s: 0 for s in STATUSES}
    for _, ev in _walk_evidence(record):
        if ev.status in counts:
            counts[ev.status] += 1
    total = sum(counts.values())
    counts["filled_fraction"] = round(
        (counts["MEASURED"] + counts["ESTIMATED"]) / total, 3) if total else 0.0
    return counts


def report(title, record):
    print(f"\n=== {title} ===")
    issues = record.validate()
    s = gap_summary(record)
    print(f"evidence fields: {s}")
    if isinstance(record, (CoordinationSystem, PhysicalLimitRecord)):
        f = record.observability.unevaluated_fraction()
        print(f"unevaluated fraction: {f if f is not None else 'UNKNOWN'}")
    for i in issues:
        print("  UNRESOLVED:", i)
    if s["filled_fraction"] == 0:
        print("  NOTE: template only — nothing measured; a clean schema is not a result")
    print("  verdict: NOT ASSIGNED")


# ---------------------------------------------------------------- demo data
CANDIDATES = ["sensor or measurement error", "calibration drift",
              "configuration or component change", "operating-condition change",
              "restricted or unavailable instrumentation",
              "measurement method inadequate", "explanation not yet identified"]

def make_demo():
    limit = PhysicalLimitRecord(
        record_id="LIMIT-001",
        system_instance="replace: hardware, software, version",
        operating_condition="replace: recorded conditions",
        physical_quantity="replace: e.g. sustained power draw")
    disc = DiscrepancyRecord(
        record_id="DISC-001", linked_limit_record_id="LIMIT-001",
        candidate_explanations=list(CANDIDATES),
        unresolved_questions=["Same units?", "Uncertainty of each measurement?",
                              "Configuration identical?", "Reproducible independently?",
                              "What observation separates the candidates?"])
    handling = DiscrepancyHandling(record_id="HANDLE-001",
                                   linked_discrepancy_id="DISC-001")
    token = CoordinationSystem(
        name="EXAMPLE: token-anchored (PROPOSED)",
        instance_of="specify country + period",
        axes={
            "anchor": Evidence("double-entry balances ledger to itself, not to world",
                               "GAP", "proposed (DeepSeek draft)"),
            "bound": Evidence("leverage multiplies claims without physical limit",
                              "UNKNOWN"),
            "coupling": Evidence("costs displaced to non-deciders", "ESTIMATED",
                                 "externality literature; cite", "", "not quantified"),
            "update": Evidence("regime change breaks estimates", "ESTIMATED",
                               "Lucas critique", "", "not quantified"),
            "error_visibility": Evidence("internally consistent, externally wrong",
                                         "UNKNOWN"),
        })
    changes = [
        InstanceChange("capitalism (US)", "1979-80", "Chrysler loan guarantees",
                       "failure clears firm", "state carries failure risk",
                       Evidence("~$1.5B guarantees", "ESTIMATED",
                                "Chrysler Loan Guarantee Act 1979", "USD", "approx")),
        InstanceChange("capitalism (US)", "2008", "TARP, AIG, GM/Chrysler",
                       "", "losses socialized, gains private",
                       Evidence("~$700B authorized", "ESTIMATED",
                                "EESA 2008", "USD", "authorized, not disbursed")),
    ]
    return limit, disc, handling, token, changes


# ----------------------------------------------------------------- selftest
def selftest():
    limit, disc, handling, token, changes = make_demo()
    # blank template is NOT clean: unspecified instance must be flagged
    assert any("instance_of" in i for i in token.validate())
    assert gap_summary(limit)["filled_fraction"] == 0.0
    # ESTIMATED needs source and uncertainty
    assert Evidence("x", "ESTIMATED").validate("t")
    assert not Evidence("x", "ESTIMATED", "src", "", "+/-1").validate("t")
    # invalid status rejected
    assert Evidence("x", "TRUE", "s").validate("t")
    # observability consistency
    o = Observability("100", "40", "10", "NO")
    assert o.unevaluated_fraction() == 0.6
    assert any("shared failure modes" in i for i in o.validate())
    assert Observability("10", "20").validate()
    # unit mismatch flagged
    d = DiscrepancyRecord("D", "L", Evidence("1", "MEASURED", "s", "W", "1%"),
                          Evidence("1", "MEASURED", "s", "kW", "1%"))
    assert any("units differ" in i for i in d.validate())
    # handling: checked outcome needs evidence
    h = DiscrepancyHandling("H", "D", outcome_independently_checked="YES")
    assert any("outcome marked checked" in i for i in h.validate())
    # abstention defects
    assert len(Abstention("d", "a", "p", "deferred", "dataset").validate()) == 2
    # instance changes carry sourced evidence
    assert all(not c.validate() for c in changes)
    # question template is all open
    q = question_template("c")
    assert all(e.status == "GAP" for e in q.axes.values())
    print("selftest ok")


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest()
    if a[:1] == ["--claim"] and len(a) > 1:
        q = question_template(" ".join(a[1:]))
        print(q.name)
        for k, e in q.axes.items():
            print(f"  {k:<17}: {e.value}")
        print("  if not audited  : record an Abstention with review_trigger")
        return
    recs = make_demo()
    if "--json" in a:
        limit, disc, handling, token, changes = recs
        print(json.dumps({"limit": asdict(limit), "discrepancy": asdict(disc),
                          "handling": asdict(handling), "token": asdict(token),
                          "instance_changes": [asdict(c) for c in changes]}, indent=2))
        return
    limit, disc, handling, token, changes = recs
    report("PHYSICAL LIMIT", limit)
    report("DISCREPANCY", disc)
    report("DISCREPANCY HANDLING", handling)
    report("COORDINATION SYSTEM", token)
    print("\n=== INSTANCE CHANGES (label held, configuration changed) ===")
    for c in changes:
        print(f"  {c.date:<8} {c.label}: {c.change} | after: {c.mechanism_after}")


if __name__ == "__main__":
    main()
