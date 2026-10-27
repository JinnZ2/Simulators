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

FIXES APPLIED 2026-10-25 (supplied text kept verbatim in
source/gap_instruments.as_supplied.py; each fix is marked "Note 2026-10-25"):
  F1 abstention: empty / whitespace fields count as GAP, not as reasoned
  F2 abstention: abstention_type checked against its listed vocabulary
  F3 coordination system: axis keys outside AXES are reported
  F4 coordination system: an axis never recorded is counted NOT_RECORDED in
     gap_summary, so filled_fraction does not rise by leaving axes out
  F5 discrepancy: tested explanations not among the candidates are reported
     (replaces a branch that did nothing)
  F6 physical limit: a "replace:" placeholder counts as unspecified
  F7 instance change: an empty label is reported
  F8 main: --claim with no text exits 2 with usage, instead of the demo

ADDITIONS 2026-10-27 (work order "gap_instruments.py extension"; each is
marked "Note 2026-10-27 (An)"; every choice the order left open is marked
[CHOICE An-k] where it is taken):
  A1 PhysicalLimitRecord.limit_basis: physical_bound | empirical_rule |
     unknown (default). A rule of thumb fitted to past experiments is not a
     physical bound. "unknown" counts as a GAP in gap_summary and is named
     by gap_fields; the report prints the basis.
  A2 CalibrationRecord: predict, then measure. target_match is checked
     first; a prediction of one quantity scored against an instrument that
     measured another is TARGET_MISMATCH, logged, not an error and not a
     miss. The outcome (HIT / MISS) and method_matches_standard are separate
     fields and never combined; a divergent method is data.
     calibration_summary: n, hits, target mismatches, mean abs error per
     quantity.
  A3 ConfoundRecord: presence and size are logged, meaning is deferred;
     interpretation stays GAP until a control separates the candidates.

USAGE
  python gap_instruments.py                 # demo templates + GAP summary
  python gap_instruments.py --claim "..."   # five-axis question template
  python gap_instruments.py --json          # demo records as JSON
  python gap_instruments.py --selftest
"""
from dataclasses import dataclass, field, asdict, fields, is_dataclass, replace
from typing import List, Optional
import json, re, sys

STATUSES = ("MEASURED", "ESTIMATED", "UNKNOWN", "GAP")
AVAILABILITY = ("AVAILABLE", "UNAVAILABLE", "RESTRICTED", "NOT_CHECKED", "UNKNOWN")
TRISTATE = ("YES", "NO", "UNKNOWN", "NOT_TESTED")
# Note 2026-10-25 (F2): the vocabulary the Abstention comment lists, now checked.
ABSTENTION_TYPES = ("declined_to_audit", "no_assessment_possible",
                    "chose_neutrality", "deferred", "did_not_reach")
# Note 2026-10-27 (A1): what a recorded limit rests on. Only the first two
# are a basis; "unknown" (and anything outside the tuple) is a GAP.
LIMIT_BASES = ("physical_bound", "empirical_rule", "unknown")
DECLARED_LIMIT_BASES = ("physical_bound", "empirical_rule")
# Note 2026-10-27 (A2)
TARGET_STATES = ("MATCH", "TARGET_MISMATCH", "NOT_EVALUABLE")
OUTCOMES = ("HIT", "MISS", "NOT_SCORED")
# Note 2026-10-27 (A3): seed names from the work order. A seed list, not a
# closed vocabulary: a name outside it is accepted.
CONFOUND_SEED_NAMES = (
    "corpus_prior", "framing_pull", "trained_reflex", "narration_not_causal",
    "context_contamination", "sampling_variance", "version_drift",
    "evaluator_sharing", "term_freight", "observer_effect", "target_mismatch",
    "frame_graded_assessment")


def _blank(value) -> bool:
    """Note 2026-10-25 (F1/F6): empty, whitespace, GAP or a template
    placeholder all mean nothing was recorded."""
    v = (value or "").strip()
    return (not v or v == "GAP" or v.lower().startswith("replace:")
            or "specify" in v.lower())


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
        # Note 2026-10-25 (F3): a misspelled axis is reported, not ignored.
        out += [f"axis not in AXES: {a}" for a in self.axes if a not in AXES]
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
        # Note 2026-10-25 (F7)
        if not self.label.strip():
            out.append("instance change: label missing")
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
    # Note 2026-10-27 (A1): last, so positional construction is unchanged.
    # A rule of thumb fitted to past experiments is not a physical bound.
    limit_basis: str = "unknown"

    def validate(self) -> List[str]:
        out = []
        # Note 2026-10-27 (A1): an unknown basis is a GAP (gap_summary), not
        # an error; a value outside LIMIT_BASES is reported.
        out += _check_enum("limit_basis", self.limit_basis, LIMIT_BASES)
        for n in ("external_bound", "ai_reported_limit", "independent_measurement",
                  "observed_response", "instrumentation_method"):
            out += getattr(self, n).validate(n)
        for n in ("sensor_availability", "calibration_status",
                  "configuration_status", "access_status"):
            out += _check_enum(n, getattr(self, n), AVAILABILITY)
        for n in ("system_instance", "operating_condition", "physical_quantity"):
            # Note 2026-10-25 (F6): "replace: ..." is a placeholder, not a value.
            if _blank(getattr(self, n)):
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
        # Note 2026-10-25 (F5): the supplied branch here did nothing.
        stray = [t for t in self.tested_explanations
                 if t not in self.candidate_explanations]
        for t in stray:
            out.append(f"tested explanation not among candidates: {t!r}")
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
        # Note 2026-10-25 (F2)
        if self.abstention_type not in ABSTENTION_TYPES:
            out.append(f"abstention: invalid abstention_type {self.abstention_type!r}")
        # Note 2026-10-25 (F1): "" and whitespace are not reasoning either.
        if _blank(self.would_have_counted_as):
            out.append("abstention: defaulted, not reasoned (would_have_counted_as)")
        if _blank(self.review_trigger):
            out.append("abstention: closer, not binding (review_trigger)")
        return out


# ------------------------------------------------------- calibration (A2)
_NUM = r"-?\d+(?:\.\d+)?"


def _norm(s) -> str:
    return " ".join((s or "").lower().split())


def _strip_approx(s):
    v = (s or "").strip()
    return v.lstrip("~").strip(), v.startswith("~")


def _interval(s):
    """Note 2026-10-27 (A2): a written value as (lo, hi), or None when it is
    not numeric (categorical). "26.3" -> (26.3, 26.3); "29-30" -> (29, 30);
    "14:02" -> minutes:seconds, 14 + 2/60 [CHOICE A2-4]. A leading "~" is
    dropped here: it widens the tolerance, not the value."""
    v, _ = _strip_approx(s)
    m = re.fullmatch(r"(\d+):([0-5]\d)", v)
    if m:
        x = int(m.group(1)) + int(m.group(2)) / 60.0
        return (x, x)
    m = re.fullmatch(r"(%s)\s*-\s*(%s)" % (_NUM, _NUM), v)
    if m:
        lo, hi = sorted((float(m.group(1)), float(m.group(2))))
        return (lo, hi)
    if re.fullmatch(_NUM, v):
        return (float(v), float(v))
    return None


def _halfwidth(s) -> Optional[float]:
    """Note 2026-10-27 (A2): half a unit in the last written digit, the
    value's own precision; a leading "~" doubles it [CHOICE A2-3]. "30" ->
    0.5, "~15" -> 1.0, "26.3" -> 0.05, "14:02" -> half a second. None when
    the value is not numeric."""
    v, approx = _strip_approx(s)
    if _interval(v) is None:
        return None
    if ":" in v:
        base = 0.5 / 60.0
    else:
        decimals = max(len(x.split(".")[1]) if "." in x else 0
                       for x in re.findall(r"\d+(?:\.\d+)?", v))
        base = 0.5 * 10 ** -decimals
    return base * 2 if approx else base


def abs_error_band(p, m):
    """Note 2026-10-27 (A2): distance between a prediction interval p and a
    measurement interval m, as (least, greatest). Two points give (d, d);
    overlapping intervals give 0 at the low end. None if either is absent."""
    if p is None or m is None:
        return None
    lo = max(0.0, p[0] - m[1], m[0] - p[1])
    hi = max(abs(p[1] - m[0]), abs(p[0] - m[1]))
    return (lo, hi)


@dataclass
class CalibrationRecord:
    """Predict, then measure. One row per prediction per reference.

    The prediction is scored only after target_match: the quantity named in
    the prediction must be the quantity the instrument measured. When they
    differ the row is TARGET_MISMATCH: logged, not an error, and not a miss.
    A prediction of the distance driven is not wrong for disagreeing with a
    distance to an address point. The outcome (HIT / MISS) and whether the
    method matched the standard method are separate fields, never combined;
    a divergent method is data.

    Baseline (carried as supplied, not checked here):
      Barkan, Black & Sourbut 2025: LLMs are overconfident; capability is
        not calibration.
      GPT-4 technical report 2023: the pretrained model was calibrated, and
        calibration was worse after RLHF.
      -> a use-time method may restore calibration. This record is a
         use-time instrument; it does not test that claim.
    """
    quantity_named: str = ""        # what exactly is estimated
    predicted: str = ""
    confidence: str = ""            # 0-1 as text; "" = not stated
    measured: Evidence = field(default_factory=Evidence)
    instrument_scope: str = ""      # what the instrument measures, and its edges
    operator_buffer: str = ""       # terms added that the instrument cannot see;
                                    # "none" if none, "" = not recorded
    goal: str = ""
    version_stamp: str = ""
    timestamp: str = ""
    # Note 2026-10-27 (A2): fields the order's rules need, beyond its list.
    instrument_quantity: str = ""   # [CHOICE A2-1] the quantity the instrument
                                    # measured; target_match compares it
    tolerance: str = ""             # [CHOICE A2-3] in measured.unit; "" ->
                                    # the prediction's written precision
    method_matches_standard: str = "NOT_TESTED"   # TRISTATE; not the outcome
    method_note: str = ""           # how the method diverged
    record_id: str = ""

    def target_match(self) -> str:
        """[CHOICE A2-2] equality after case and whitespace are normalized.
        Two names for one quantity read as a mismatch; the match is declared
        by whoever writes instrument_quantity."""
        a, b = _norm(self.quantity_named), _norm(self.instrument_quantity)
        if not a or not b:
            return "NOT_EVALUABLE"
        return "MATCH" if a == b else "TARGET_MISMATCH"

    def tolerance_used(self):
        t = self.tolerance.strip()
        if t:
            try:
                v = float(t)
            except ValueError:
                return None, "declared tolerance is not a number"
            if v < 0:
                return None, "declared tolerance is negative"
            return v, "declared"
        h = _halfwidth(self.predicted)
        if h is None:
            return None, "no tolerance: prediction not numeric"
        if self.predicted.strip().startswith("~"):
            return h, "written precision, doubled by '~'"
        return h, "written precision"

    def score(self) -> dict:
        tm = self.target_match()
        out = {"record_id": self.record_id, "quantity": self.quantity_named,
               "target_match": tm, "outcome": "NOT_SCORED", "abs_error": None,
               "tolerance": None, "tolerance_basis": None,
               "method_matches_standard": self.method_matches_standard,
               "reason": ""}
        if tm == "TARGET_MISMATCH":
            out["reason"] = ("TARGET_MISMATCH: the prediction names %r, the "
                             "instrument measured %r; logged, not an error"
                             % (self.quantity_named, self.instrument_quantity))
            return out
        if tm == "NOT_EVALUABLE":
            out["reason"] = "target not checkable: a quantity name is blank"
            return out
        if (self.measured.status not in ("MEASURED", "ESTIMATED")
                or self.measured.validate("measured")):
            out["reason"] = ("measured is %s or incomplete; nothing to score "
                             "against" % self.measured.status)
            return out
        if _blank(self.predicted):
            out["reason"] = "no prediction recorded"
            return out
        p, m = _interval(self.predicted), _interval(self.measured.value)
        if p is None and m is None:
            same = _norm(_strip_approx(self.predicted)[0]) == _norm(self.measured.value)
            out.update(outcome="HIT" if same else "MISS",
                       tolerance_basis="categorical: exact match")
            return out
        if p is None or m is None:
            out["reason"] = "one side numeric, the other not"
            return out
        tol, basis = self.tolerance_used()
        band = abs_error_band(p, m)
        out.update(abs_error=[round(band[0], 4), round(band[1], 4)],
                   tolerance=None if tol is None else round(tol, 6),
                   tolerance_basis=basis)
        if tol is None:
            out["reason"] = basis
            return out
        # [CHOICE A2-5] HIT when some value the measurement allows lies
        # within tolerance of the prediction: the low end of the band.
        out["outcome"] = "HIT" if band[0] <= tol + 1e-12 else "MISS"
        return out

    def validate(self) -> List[str]:
        out = []
        for n in ("quantity_named", "predicted", "instrument_quantity",
                  "instrument_scope", "goal", "version_stamp", "timestamp"):
            if _blank(getattr(self, n)):
                out.append(f"calibration: {n} not stated")
        if _blank(self.operator_buffer):
            out.append("calibration: operator_buffer not recorded ('none' if none)")
        c = self.confidence.strip()
        if not c:
            out.append("calibration: confidence not stated")
        else:
            try:
                cv = float(c)
            except ValueError:
                cv = None
            if cv is None or not 0.0 <= cv <= 1.0:
                out.append(f"calibration: confidence {c!r} not in 0-1")
        out += self.measured.validate("calibration.measured")
        if self.measured.status in ("GAP", "UNKNOWN"):
            out.append(f"calibration: measured is {self.measured.status}; "
                       "nothing to score against")
        if self.tolerance.strip() and self.tolerance_used()[0] is None:
            out.append(f"calibration: tolerance {self.tolerance!r} unusable")
        out += _check_enum("calibration.method_matches_standard",
                           self.method_matches_standard, TRISTATE)
        if self.method_matches_standard == "NO" and _blank(self.method_note):
            out.append("calibration: method diverged but the divergence is "
                       "not described")
        return out


def _confidence_value(r) -> Optional[float]:
    try:
        v = float(r.confidence.strip())
    except ValueError:
        return None
    return v if 0.0 <= v <= 1.0 else None


def calibration_summary(records) -> dict:
    """Note 2026-10-27 (A2): n, hits, target mismatches and mean absolute
    error per quantity. MAE is taken over target-matched numeric rows only,
    as a band (least, greatest) since a measurement can be a range; a
    quantity with no such row reads None, never 0. Mismatched rows enter no
    MAE: they measured another quantity. The method column is counted
    apart from the outcome."""
    pairs = [(r, r.score()) for r in records]
    rows = [s for _, s in pairs]
    out = {"n": len(rows),
           "hits": sum(s["outcome"] == "HIT" for s in rows),
           "misses": sum(s["outcome"] == "MISS" for s in rows),
           "target_mismatches": sum(s["target_match"] == "TARGET_MISMATCH" for s in rows),
           "target_not_evaluable": sum(s["target_match"] == "NOT_EVALUABLE" for s in rows),
           "not_scored": sum(s["outcome"] == "NOT_SCORED" for s in rows),
           "method_matches_standard": {t: sum(s["method_matches_standard"] == t
                                              for s in rows) for t in TRISTATE},
           "by_quantity": {}}
    for s in rows:
        q = s["quantity"].strip() or "(unnamed)"
        if q in out["by_quantity"]:
            continue
        qs = [x for x in rows if (x["quantity"].strip() or "(unnamed)") == q]
        scored = [x for x in qs if x["outcome"] in ("HIT", "MISS")]
        num = [x["abs_error"] for x in scored if x["abs_error"] is not None]
        out["by_quantity"][q] = {
            "n": len(qs), "scored": len(scored),
            "mae": None if not num else
            [round(sum(e[0] for e in num) / len(num), 4),
             round(sum(e[1] for e in num) / len(num), 4)]}
    scored = [(r, s) for r, s in pairs if s["outcome"] in ("HIT", "MISS")]
    conf = [(_confidence_value(r), s) for r, s in scored]
    conf = [(c, s) for c, s in conf if c is not None]
    if conf:
        out["confidence_vs_hit_rate"] = {
            "n": len(conf),
            "mean_confidence": round(sum(c for c, _ in conf) / len(conf), 4),
            "hit_rate": round(sum(s["outcome"] == "HIT" for _, s in conf) / len(conf), 4)}
    else:
        out["confidence_vs_hit_rate"] = ("NOT_COMPUTABLE: 0 of %d scored rows "
                                         "state a confidence" % len(scored))
    return out


# ---------------------------------------------------------- confounds (A3)
@dataclass
class ConfoundRecord:
    """Note 2026-10-27 (A3). Presence and size are logged; meaning is
    deferred. interpretation stays GAP until a control separates the
    candidate explanations; an interpretation with no control is reported."""
    name: str
    present: object = "UNKNOWN"          # True | False | "UNKNOWN"
    size: Optional[Evidence] = None      # None = size not recorded
    control_used: str = ""
    interpretation: str = "GAP"

    def validate(self) -> List[str]:
        out = []
        label = f"confound[{self.name}]"
        if not (self.name or "").strip():
            out.append("confound: name missing")
        if not (isinstance(self.present, bool) or self.present == "UNKNOWN"):
            out.append(f"{label}: present must be True, False or 'UNKNOWN', "
                       f"got {self.present!r}")
        sized = isinstance(self.size, Evidence)
        if self.size is not None and not sized:
            out.append(f"{label}: size is not Evidence")
        if sized:
            out += self.size.validate(f"{label}.size")
        if self.present is True and not (sized and self.size.status != "GAP"):
            out.append(f"{label}: present but size not recorded")
        if (self.present is False and sized
                and self.size.status in ("MEASURED", "ESTIMATED")):
            out.append(f"{label}: absent but a size is recorded")
        if not _blank(self.interpretation) and _blank(self.control_used):
            out.append(f"{label}: interpretation assigned without a control "
                       "(stays GAP until a control separates candidates)")
        return out


def confound_summary(records) -> dict:
    return {"n": len(records),
            "present": {k: sum((c.present is v) if isinstance(v, bool)
                               else (c.present == v) for c in records)
                        for k, v in (("True", True), ("False", False),
                                     ("UNKNOWN", "UNKNOWN"))},
            "sized": sum(isinstance(c.size, Evidence) and c.size.status != "GAP"
                         for c in records),
            "controlled": sum(not _blank(c.control_used) for c in records),
            "interpretation_GAP": sum(_blank(c.interpretation) for c in records)}


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
    # Note 2026-10-25 (F4): an axis never recorded is not a GAP finding and
    # must not shrink the denominator. Counted apart, included in the total.
    if isinstance(record, CoordinationSystem):
        counts["NOT_RECORDED"] = sum(1 for a in AXES if a not in record.axes)
    # Note 2026-10-27 (A1): an unknown limit basis is one GAP. A declared
    # basis counts as nothing: naming a basis measures nothing.
    if (isinstance(record, PhysicalLimitRecord)
            and record.limit_basis not in DECLARED_LIMIT_BASES):
        counts["GAP"] += 1
    # Note 2026-10-27 (A3): a deferred interpretation is a GAP; an unknown
    # presence is UNKNOWN.
    if isinstance(record, ConfoundRecord):
        if _blank(record.interpretation):
            counts["GAP"] += 1
        if not isinstance(record.present, bool):
            counts["UNKNOWN"] += 1
    total = sum(counts.values())
    counts["filled_fraction"] = round(
        (counts["MEASURED"] + counts["ESTIMATED"]) / total, 3) if total else 0.0
    return counts


def gap_fields(record) -> List[str]:
    """Note 2026-10-27 (A1): the values gap_summary counts as GAP, by name."""
    out = [p.rstrip(".") for p, ev in _walk_evidence(record) if ev.status == "GAP"]
    if (isinstance(record, PhysicalLimitRecord)
            and record.limit_basis not in DECLARED_LIMIT_BASES):
        out.append("limit_basis")
    if isinstance(record, ConfoundRecord) and _blank(record.interpretation):
        out.append("interpretation")
    return out


def report(title, record):
    print(f"\n=== {title} ===")
    issues = record.validate()
    s = gap_summary(record)
    print(f"evidence fields: {s}")
    if isinstance(record, (CoordinationSystem, PhysicalLimitRecord)):
        f = record.observability.unevaluated_fraction()
        print(f"unevaluated fraction: {f if f is not None else 'UNKNOWN'}")
    if isinstance(record, PhysicalLimitRecord):                  # A1
        tag = ("" if record.limit_basis in DECLARED_LIMIT_BASES
               else "  (counted as GAP)")
        print(f"limit_basis: {record.limit_basis}{tag}")
    for i in issues:
        print("  UNRESOLVED:", i)
    if s["filled_fraction"] == 0:
        print("  NOTE: template only — nothing measured; a clean schema is not a result")
    print("  verdict: NOT ASSIGNED")


def _band(e):
    if e is None:
        return "--"
    return "%g" % e[0] if e[0] == e[1] else "%g-%g" % (e[0], e[1])


def report_calibration(records):
    """Note 2026-10-27 (A2)"""
    print("\n=== CALIBRATION (predict, then measure; target checked first) ===")
    for r in records:
        s = r.score()
        print(f"  {s['record_id']:<17} {s['target_match']:<15} "
              f"{s['outcome']:<10} abs_error {_band(s['abs_error']):<8} "
              f"tolerance {s['tolerance'] if s['tolerance'] is not None else '--'}"
              f" | method {s['method_matches_standard']}")
        if s["tolerance_basis"]:
            print(f"    tolerance basis: {s['tolerance_basis']}")
        if s["reason"]:
            print(f"    {s['reason']}")
        for i in r.validate():
            print("    UNRESOLVED:", i)
    summ = calibration_summary(records)
    print("  summary: n %d, hits %d, misses %d, target mismatches %d, "
          "not scored %d" % (summ["n"], summ["hits"], summ["misses"],
                             summ["target_mismatches"], summ["not_scored"]))
    for q, v in summ["by_quantity"].items():
        print(f"    {q}: n {v['n']}, scored {v['scored']}, mae {_band(v['mae'])}")
    print(f"  method matches standard (kept apart): {summ['method_matches_standard']}")
    print(f"  confidence vs hit rate: {summ['confidence_vs_hit_rate']}")
    print("  verdict: NOT ASSIGNED")


def report_confounds(records):
    """Note 2026-10-27 (A3)"""
    print("\n=== CONFOUNDS (presence and size logged; meaning deferred) ===")
    for c in records:
        if isinstance(c.size, Evidence):
            size = f"[{c.size.status}] {c.size.value} {c.size.unit}".rstrip()
        else:
            size = "not recorded"
        print(f"  {c.name:<24} present {str(c.present):<8} size {size} | "
              f"control {c.control_used or '-'} | interpretation {c.interpretation}")
        for i in c.validate():
            print("    UNRESOLVED:", i)
    print(f"  summary: {confound_summary(records)}")
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


def make_seed():
    """Note 2026-10-27: seed instances from the 2026-10-26 work order. Every
    value is as supplied (PROPOSED); none was checked against a source here.
    Fields the work order did not state are left blank and read UNRESOLVED."""
    east = PhysicalLimitRecord(
        record_id="LIMIT-EAST-2026",
        system_instance="EAST tokamak, 2026 (as supplied)",
        operating_condition="",           # not stated in the work order
        physical_quantity="plasma density relative to the Greenwald limit",
        external_bound=Evidence("Greenwald density limit n_G", "ESTIMATED",
                                "empirical rule fitted to past experiments "
                                "(as supplied)", "", "not quantified here"),
        observed_response=Evidence("stable at 1.3-1.65 x n_G", "MEASURED",
                                   "EAST 2026, as supplied; not checked here",
                                   "x n_G", "range as stated; per-shot "
                                   "uncertainty not stated"),
        limit_basis="empirical_rule")
    t_seed = "2026-10-25/26 (voice dictated)"
    human = "n/a: human operator"
    miles = "miles driven to the dock, incl. going around the shop"
    calib = [
        CalibrationRecord(
            record_id="CAL-MILES-GPS", quantity_named=miles, predicted="30",
            measured=Evidence("26.3", "MEASURED", "GPS, to the address point "
                              "(as dictated)", "mi", "display 0.1 mi"),
            instrument_quantity="route miles to the address point",
            instrument_scope="GPS distance to the address point; does not "
                             "see on-site movement",
            operator_buffer="going around the shop and back to the dock",
            version_stamp=human, timestamp=t_seed),
        CalibrationRecord(
            record_id="CAL-MILES-ACTUAL", quantity_named=miles, predicted="30",
            measured=Evidence("29-30", "ESTIMATED", "operator, as dictated; "
                              "instrument not named", "mi", "~, stated as a range"),
            instrument_quantity=miles,
            instrument_scope="instrument not named in the dictation",
            operator_buffer="going around the shop and back to the dock",
            version_stamp=human, timestamp=t_seed),
        CalibrationRecord(
            record_id="CAL-FUEL", quantity_named="fuel tank level",
            predicted="full",
            measured=Evidence("full", "MEASURED", "fuel gauge (as dictated)",
                              "", "gauge resolution not stated"),
            instrument_quantity="fuel tank level",
            instrument_scope="fuel gauge reading",
            version_stamp=human, timestamp=t_seed,
            # [CHOICE A2-6] the standard method is taken as the instrument's
            # own reading; inferring from memory diverges from it.
            method_matches_standard="NO",
            method_note="inferred full from memory of the fill-up; the gauge "
                        "then confirmed it"),
        CalibrationRecord(
            record_id="CAL-TIME", quantity_named="on-duty time",
            predicted="~15",
            measured=Evidence("14:02", "MEASURED", "ELD on-duty (as dictated)",
                              "min", "read as 14 min 02 s; read as h:mm it is "
                              "842 min"),
            instrument_quantity="on-duty time",
            instrument_scope="ELD on-duty time as logged",
            version_stamp=human, timestamp=t_seed),
    ]
    confounds = [ConfoundRecord(n) for n in CONFOUND_SEED_NAMES]
    # [CHOICE A3-1] the calibration seed instances a target mismatch, so that
    # one confound is logged present with its size; its meaning stays GAP.
    i = CONFOUND_SEED_NAMES.index("target_mismatch")
    confounds[i] = ConfoundRecord(
        "target_mismatch", True,
        Evidence("2.7-3.7", "ESTIMATED", "CAL-MILES-ACTUAL minus CAL-MILES-GPS "
                 "(29-30 minus 26.3)", "mi", "from the ~29-30 range"))
    return east, calib, confounds


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
    # Note 2026-10-25: one check per fix.
    assert len(Abstention("d", "a", "p", "deferred", "x", "", " ").validate()) == 2  # F1
    assert any("abstention_type" in i                                              # F2
               for i in Abstention("d", "a", "p", "made_up", "x", "w", "r").validate())
    typo = CoordinationSystem("t", "US 2008", {"ancor": Evidence("v")})
    assert any("not in AXES: ancor" in i for i in typo.validate())                 # F3
    one = CoordinationSystem("o", "US 2008",
                             {"anchor": Evidence("v", "MEASURED", "s", "", "1")})
    s1 = gap_summary(one)
    assert s1["NOT_RECORDED"] == 4 and s1["filled_fraction"] < 0.2                 # F4
    stray = DiscrepancyRecord("D", "L", candidate_explanations=["a"],
                              tested_explanations=["a", "b"])
    assert any("'b'" in i for i in stray.validate())                               # F5
    assert sum("unspecified" in i for i in limit.validate()) == 3                  # F6
    assert any("label missing" in i for i in InstanceChange("", "2000", "c").validate())  # F7
    assert not Abstention("d", "a", "p", "deferred", "x", "w", "r").validate()     # F1/F2 negative
    # Note 2026-10-27: the three additions.
    east, calib, confounds = make_seed()
    # A1: limit_basis unknown appears in gaps, by count and by name
    assert limit.limit_basis == "unknown" and "limit_basis" in gap_fields(limit)
    declared = PhysicalLimitRecord("L", "s", "o", "q", limit_basis="empirical_rule")
    assert gap_summary(declared)["GAP"] == gap_summary(limit)["GAP"] - 1
    assert "limit_basis" not in gap_fields(declared) + gap_fields(east)
    assert any("limit_basis" in i for i in
               PhysicalLimitRecord("L", "s", "o", "q", limit_basis="physics").validate())
    for r in (limit, disc, handling, token, east, *confounds):
        assert gap_summary(r)["GAP"] == len(gap_fields(r))
    # A2: a blank CalibrationRecord does not validate clean, and scores nothing
    blank = CalibrationRecord()
    assert len(blank.validate()) == 10
    assert (blank.score()["target_match"], blank.score()["outcome"]) == \
        ("NOT_EVALUABLE", "NOT_SCORED")
    # A2: the mismatch path returns TARGET_MISMATCH, unscored and not an error
    g = calib[0].score()
    assert g["target_match"] == "TARGET_MISMATCH" and g["outcome"] == "NOT_SCORED"
    assert g["abs_error"] is None
    assert not any("mismatch" in i.lower() for i in calib[0].validate())
    # A2: the dictated verdicts reproduce under the declared rules
    assert [c.score()["outcome"] for c in calib] == ["NOT_SCORED", "HIT", "HIT", "HIT"]
    # the time HIT rests on '~' doubling the written precision: at +/-0.5 it misses
    t = calib[3].score()
    assert t["tolerance"] == 1.0 and abs(t["abs_error"][0] - 0.9667) < 1e-4
    assert replace(calib[3], tolerance="0.5").score()["outcome"] == "MISS"
    # A2: outcome and method stay apart; the fuel HIT came by a divergent method
    f = calib[2].score()
    assert (f["outcome"], f["method_matches_standard"]) == ("HIT", "NO")
    s = calibration_summary(calib)
    assert (s["n"], s["hits"], s["target_mismatches"]) == (4, 3, 1)
    bq = s["by_quantity"]
    assert bq[calib[0].quantity_named]["mae"] == [0.0, 1.0]
    assert (bq[calib[0].quantity_named]["n"], bq[calib[0].quantity_named]["scored"]) == (2, 1)
    assert bq["on-duty time"]["mae"] == [0.9667, 0.9667]
    assert bq["fuel tank level"]["mae"] is None
    assert str(s["confidence_vs_hit_rate"]).startswith("NOT_COMPUTABLE")
    assert abs_error_band((10, 12), (14, 15)) == (2, 5)
    # A3: meaning deferred until a control separates candidates
    ev = Evidence("1", "MEASURED", "s", "", "1")
    assert any("without a control" in i for i in
               ConfoundRecord("x", True, ev, "", "framing").validate())
    assert not ConfoundRecord("x", True, ev, "ablation", "framing").validate()
    assert any("size not recorded" in i for i in ConfoundRecord("x", True).validate())
    assert any("present must be" in i for i in ConfoundRecord("x", 1).validate())
    assert [c.name for c in confounds] == list(CONFOUND_SEED_NAMES)
    assert all(not c.validate() and c.interpretation == "GAP" for c in confounds)
    print("selftest ok")


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest()
    # Note 2026-10-25 (F8): --claim with no text is a usage error, not the demo.
    if a[:1] == ["--claim"] and len(a) == 1:
        print("usage: gap_instruments.py --claim \"claim text\"", file=sys.stderr)
        sys.exit(2)
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
        east, calib, confounds = make_seed()                      # A1-A3
        print(json.dumps({"limit": asdict(limit), "discrepancy": asdict(disc),
                          "handling": asdict(handling), "token": asdict(token),
                          "instance_changes": [asdict(c) for c in changes],
                          "limit_seed": asdict(east),
                          "calibration": [asdict(c) for c in calib],
                          "calibration_scores": [c.score() for c in calib],
                          "calibration_summary": calibration_summary(calib),
                          "confounds": [asdict(c) for c in confounds]}, indent=2))
        return
    limit, disc, handling, token, changes = recs
    report("PHYSICAL LIMIT", limit)
    report("DISCREPANCY", disc)
    report("DISCREPANCY HANDLING", handling)
    report("COORDINATION SYSTEM", token)
    print("\n=== INSTANCE CHANGES (label held, configuration changed) ===")
    for c in changes:
        print(f"  {c.date:<8} {c.label}: {c.change} | after: {c.mechanism_after}")
    east, calib, confounds = make_seed()                          # A1-A3
    report("PHYSICAL LIMIT (seed: EAST 2026, PROPOSED, carried)", east)
    report_calibration(calib)
    report_confounds(confounds)


if __name__ == "__main__":
    main()
