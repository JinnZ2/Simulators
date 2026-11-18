"""
unified_audit.py -- full-family audit orchestrator

Wires the 9 calibration tools together behind one entry point.
Dispatches based on which sub-inputs are present, so callers can
feed any subset and get back a composite report.

Input modalities (all optional; run only what you supply):

    system_description     -- structured data about a system
                              (feedback_events, skill_log,
                              friction_events, ...)
                              routes through pipeline.run_unified_audit
                              (the original 3-module pipeline)

    system_state           -- {fatigue_score, distance_to_collapse,
                              hidden_count, friction_ratio, K_cred,
                              trust_level, ...} snapshot
                              routes through assumption_validator

    response_text          -- a string of model output
                              routes through monoculture_detector,
                              anti_metaphor_locker,
                              negative_space_index

    fork_answers           -- {frame_name: answer_text} for multiple
                              constraint frames
                              routes through fork_width_scorer

    scenario               -- a scenario dict (from trapdoors.json,
                              substrate_refusal_eval.SCENARIOS, or
                              cascade_length_eval.SCENARIOS) to use
                              alongside response_text
                              routes through whichever evaluator
                              matches the scenario's shape

    function_audit         -- {function, base_params, param_ranges,
                              specs, assumptions}
                              routes through first_principles_audit

Composite output:
    - per-module sub-reports
    - severity: GREEN / YELLOW / RED, worst across MEASURED inputs only;
      NOT_DETERMINABLE when no input was measured
    - coverage: count + list of UNKNOWN inputs, each with its
      expiry_condition (VOID allowed). UNKNOWN is not a severity.
    - overall_status: the severity alone when coverage is 0; otherwise
      "<severity>+COVERAGE(<n>)", so a single colour never prints alone
    - red_flags (cross-cutting issues)
    - summary string

Dependencies: stdlib only (plus the sibling audit modules).
License: CC0 1.0 Universal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Optional


# ---------------------------------------------------------------
# STATUS AGGREGATION
# ---------------------------------------------------------------

# Severity ordering for combining multiple module statuses.
_STATUS_RANK = {
    "GREEN": 0,
    "PASS": 0,
    "substrate_pass": 0,
    "MINIMAL": 0,
    "YELLOW": 1,
    "CAUTION": 1,
    "mixed": 1,
    "LOW": 1,
    "MODERATE": 2,
    "WARNING": 2,
    "refusal_or_off_topic": 2,
    "RED": 3,
    "FAIL": 3,
    "monoculture_fail": 3,
    "HIGH": 3,
    "CRITICAL": 4,
}
# UNKNOWN is deliberately absent (2026-11-11, decided by Kavik): it was
# rank 1 / YELLOW here, and is now a separate coverage axis. A status
# string that is not in this table is not a measured severity; it goes
# to coverage, never to a colour.

NOT_DETERMINABLE = "NOT_DETERMINABLE"

# A module that raised is not a reading of the system. Its status is
# GAP_INSTRUMENT_CRASH and it goes to coverage with the exception and the
# missing path, never to severity (2026-11-11 follow-up to #80).
GAP_INSTRUMENT_CRASH = "GAP_INSTRUMENT_CRASH"

# Coverage kinds, kept apart: UNKNOWN (no value), INFO (a value that the
# instrument cannot assess, e.g. non-numeric), GAP_INSTRUMENT_CRASH (the
# instrument itself failed).
COVERAGE_KINDS = ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH")

# Why severity is NOT_DETERMINABLE (2026-11-11, decided by Kavik). Set only
# when severity is NOT_DETERMINABLE; None otherwise.
#   NO_MODULES_RUN             no module ran (empty audit)
#   ALL_INPUTS_UNKNOWN         modules ran; every non-measured status is
#                              "UNKNOWN" (the module had no measured input)
#   ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL
#                              modules ran; every non-measured status is a
#                              label outside _STATUS_RANK other than
#                              "UNKNOWN" (the instrument emitted no
#                              severity it can be ranked on).
#   ALL_MODULES_GAP_INSTRUMENT_CRASH
#                              modules ran; every non-measured status is a
#                              module that raised. Not reachable on this
#                              branch (a raise is RED here); reachable once
#                              the crash-as-coverage change (#82) lands.
# The single name ALL_MODULES_GAP_INSTRUMENT is retired: #82 used
# GAP_INSTRUMENT for "module raised" and this branch for "label outside
# the table". Both senses are kept under split names (2026-11-11).
GAP_INSTRUMENT_UNRECOGNIZED_LABEL = "GAP_INSTRUMENT_UNRECOGNIZED_LABEL"
NO_MODULES_RUN = "NO_MODULES_RUN"
ALL_INPUTS_UNKNOWN = "ALL_INPUTS_UNKNOWN"
ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL = (
    "ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL")
ALL_MODULES_GAP_INSTRUMENT_CRASH = "ALL_MODULES_GAP_INSTRUMENT_CRASH"
# Not in the delivered set: UNKNOWN and gap-instrument statuses both
# present among the modules that ran (accepted 2026-11-11). Covers either
# gap-instrument sense.
MIXED_UNKNOWN_AND_GAP_INSTRUMENT = "MIXED_UNKNOWN_AND_GAP_INSTRUMENT"
NOT_DETERMINABLE_REASONS = (NO_MODULES_RUN, ALL_INPUTS_UNKNOWN,
                            ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL,
                            ALL_MODULES_GAP_INSTRUMENT_CRASH,
                            MIXED_UNKNOWN_AND_GAP_INSTRUMENT)

# Exit conditions for the assumption_validator UNKNOWN emitter
# (assumption_validator.py:288). The two registers disagree and are
# carried side by side; neither is picked (docs/EXPIRY_RECONCILED.md,
# branch claude/expiry-register-reconciled).
_AV_UNKNOWN_EXPIRY = {
    "pr77": "VOID -- no exit defined (docs/expiry_register.json U40)",
    "pr78": ("incomplete -- instrument: a measured value for the "
             "boundary's parameter; protocol: supply state[parameter] "
             "and re-run validate (calibration/expiry_register.py U04)"),
}
_VOID = "VOID"

_STATUS_NORMALIZED = {
    0: "GREEN",
    1: "YELLOW",
    2: "YELLOW",
    3: "RED",
    4: "RED",
}


def _aggregate_status(statuses: list[str]) -> str:
    """Worst MEASURED status, normalized to GREEN/YELLOW/RED.

    Only statuses in _STATUS_RANK are measured severities. Anything else
    (UNKNOWN, an unrecognized label) is ignored here and must be reported
    on the coverage axis by the caller. No measured status at all ->
    NOT_DETERMINABLE, never GREEN.
    """
    measured = [s for s in statuses if s in _STATUS_RANK]
    if not measured:
        return NOT_DETERMINABLE
    worst = max(_STATUS_RANK[s] for s in measured)
    return _STATUS_NORMALIZED[worst]


def _coverage_by_kind(coverage: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for e in coverage:
        counts[e["kind"]] = counts.get(e["kind"], 0) + 1
    return {k: counts[k] for k in COVERAGE_KINDS if k in counts}


def _not_determinable_reason(statuses: list[str]) -> Optional[str]:
    """Reason for NOT_DETERMINABLE, or None when severity is measured."""
    if any(s in _STATUS_RANK for s in statuses):
        return None
    if not statuses:
        return NO_MODULES_RUN
    unknown = sum(1 for s in statuses if s == "UNKNOWN")
    if unknown == len(statuses):
        return ALL_INPUTS_UNKNOWN
    crash = sum(1 for s in statuses if s == GAP_INSTRUMENT_CRASH)
    label = len(statuses) - unknown - crash
    if unknown == 0 and label == 0:
        return ALL_MODULES_GAP_INSTRUMENT_CRASH
    if unknown == 0 and crash == 0:
        return ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL
    return MIXED_UNKNOWN_AND_GAP_INSTRUMENT


def _combined_status(severity: str, coverage: list[dict]) -> str:
    """The one-string form. Never a colour alone when coverage > 0."""
    if not coverage:
        return severity
    kinds = ", ".join(f"{k}={v}" for k, v in _coverage_by_kind(coverage).items())
    return f"{severity}+COVERAGE({len(coverage)}: {kinds})"


# ---------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------

@dataclass
class UnifiedAuditReport:
    system_id: str
    modules_run: list[str] = field(default_factory=list)
    modules_skipped: list[str] = field(default_factory=list)
    sections: dict = field(default_factory=dict)
    severity: str = NOT_DETERMINABLE
    coverage: list[dict] = field(default_factory=list)
    overall_status: str = NOT_DETERMINABLE
    not_determinable_reason: Optional[str] = NO_MODULES_RUN
    red_flags: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict:
        return {
            "system_id": self.system_id,
            "modules_run": self.modules_run,
            "modules_skipped": self.modules_skipped,
            "overall_status": self.overall_status,
            "severity": self.severity,
            "not_determinable_reason": self.not_determinable_reason,
            "coverage_count": len(self.coverage),
            "coverage_by_kind": _coverage_by_kind(self.coverage),
            "coverage": self.coverage,
            "red_flags": self.red_flags,
            "summary": self.summary,
            "sections": self.sections,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)


# ---------------------------------------------------------------
# RESPONSE-TEXT DISPATCHERS (text-in -> status-out)
# ---------------------------------------------------------------

def _run_monoculture(response_text: str) -> tuple[str, dict]:
    """Corpus-diversity audit on a single response (treated as 1-doc corpus)."""
    from monoculture_detector import MonocultureDetector
    report = MonocultureDetector().audit([response_text])
    return (report.overall_status, report.to_dict())


def _run_anti_metaphor(response_text: str) -> tuple[str, dict]:
    """Check for substrate-term drift into generic metaphor."""
    from anti_metaphor_locker import AntiMetaphorLocker
    report = AntiMetaphorLocker().audit(response_text)
    return (report.overall_status, json.loads(report.to_json()))


def _run_negative_space(response_text: str) -> tuple[str, dict]:
    """Check for violations of declared knowledge-boundary regions."""
    from negative_space_index import audit_response
    report = audit_response(response_text)
    return (report.overall_status, report.to_dict())


def _run_fork_width(answers: dict[str, str]) -> tuple[str, dict]:
    """Diversity across constraint frames. Requires >=2 answers."""
    from fork_width_scorer import ForkWidthScorer
    report = ForkWidthScorer().score(answers)
    return (report.overall_status, report.to_dict())


def _run_cascade(response_text: str, scenario: dict) -> tuple[str, dict]:
    """Causal-chain depth eval against a cascade scenario."""
    from cascade_length_eval import CascadeLengthEval
    report = CascadeLengthEval().evaluate(response_text, scenario)
    return (report.overall_status, report.to_dict())


def _run_refusal(response_text: str, scenario: dict) -> tuple[str, dict]:
    """Substrate vs policy refusal classification against a physics-impossible
    scenario."""
    from substrate_refusal_eval import SubstrateRefusalEval
    report = SubstrateRefusalEval().evaluate(response_text, scenario)
    return (report.overall_status, report.to_dict())


def _run_trapdoor(response_text: str,
                  trapdoor_id: Optional[str] = None,
                  trapdoor: Optional[Any] = None) -> tuple[str, dict]:
    """Buried-shear-plane detection. Pass trapdoor (loaded) or trapdoor_id."""
    from trapdoor_eval import TrapdoorEval, get_trapdoor, load_trapdoors, Trapdoor
    if trapdoor is None:
        if trapdoor_id is None:
            raise ValueError("trapdoor or trapdoor_id required")
        trapdoor = get_trapdoor(trapdoor_id)
    elif isinstance(trapdoor, dict):
        trapdoor = Trapdoor.from_dict(trapdoor)
    report = TrapdoorEval().evaluate(response_text, trapdoor)
    return (report.overall_status, report.to_dict())


# ---------------------------------------------------------------
# STATE-SNAPSHOT DISPATCHER
# ---------------------------------------------------------------

def _run_assumption_validator(state: dict[str, float]) -> tuple[str, dict]:
    """Regime-validity check: are TAF's equations still in their valid zone?"""
    from assumption_validator import full_report
    report = full_report(state)
    assumptions = report.get("assumptions", {})
    # Measured inputs only. detect_cascade_risk already ignores UNKNOWN
    # assumptions; with none measured its MINIMAL is the absence of a
    # reading, not a reading, so the module itself is UNKNOWN.
    if assumptions and not any(v.get("status") in ("GREEN", "YELLOW", "RED")
                               for v in assumptions.values()):
        return ("UNKNOWN", report)
    # Map cascade_level to our status vocabulary.
    cascade_level = report["cascade"]["cascade_level"]
    status = {
        "MINIMAL": "GREEN",
        "LOW": "YELLOW",
        "MODERATE": "YELLOW",
        "HIGH": "RED",
        "CRITICAL": "RED",
    }.get(cascade_level, "UNKNOWN")
    return (status, report)


def _coverage_entries(name: str, status: str, section: Any) -> list[dict]:
    """UNKNOWN inputs for one module, each with its expiry_condition."""
    entries: list[dict] = []
    if status == GAP_INSTRUMENT_CRASH:
        sec = section if isinstance(section, dict) else {}
        entries.append({
            "kind": GAP_INSTRUMENT_CRASH,
            "module": name,
            "input": name,
            "reason": sec.get("error", "module raised"),
            "missing_path": sec.get("missing_path"),
            "expiry_condition": _VOID,
        })
        return entries
    if name == "assumption_validator" and isinstance(section, dict):
        for aid, a in section.get("assumptions", {}).items():
            if a.get("status") == "UNKNOWN":
                entries.append({
                    "kind": "UNKNOWN",
                    "module": name,
                    "input": aid,
                    "reason": a.get("message", "no value"),
                    "expiry_condition": dict(_AV_UNKNOWN_EXPIRY),
                })
            elif a.get("status") == "INFO":
                entries.append({
                    "kind": "INFO",
                    "module": name,
                    "input": aid,
                    "reason": a.get("message", "value not assessable"),
                    "expiry_condition": _VOID,
                })
        return entries
    if status not in _STATUS_RANK:
        entries.append({
            "kind": "UNKNOWN",
            "module": name,
            "input": name,
            "reason": f"module status {status!r} is not a measured severity",
            "expiry_condition": _VOID,
        })
    return entries


# ---------------------------------------------------------------
# CODE-AUDIT DISPATCHER
# ---------------------------------------------------------------

def _run_first_principles(spec: dict) -> tuple[str, dict]:
    """Six Sigma DMAIC audit of a Python function.

    Expected keys in spec: function (callable), base_params, param_ranges.
    Optional: specs (ParameterSpec dict), assumptions, output_key,
    lower_spec, upper_spec, n_monte_carlo.
    """
    from first_principles_audit import audit_function
    kwargs = {
        "base_params": spec["base_params"],
        "param_ranges": spec["param_ranges"],
    }
    for k in ("specs", "assumptions", "output_key",
              "lower_spec", "upper_spec",
              "n_sensitivity_steps", "n_monte_carlo"):
        if k in spec:
            kwargs[k] = spec[k]
    report = audit_function(spec["function"], **kwargs)
    grade = report["summary"].get("overall_grade", "")
    if grade.startswith("A"):
        status = "GREEN"
    elif grade.startswith("B"):
        status = "YELLOW"
    else:
        status = "RED"
    return (status, report)


# ---------------------------------------------------------------
# LEGACY PIPELINE DISPATCHER
# ---------------------------------------------------------------

def _run_legacy_pipeline(system_desc: dict) -> tuple[str, dict]:
    """Calls the existing 3-module pipeline (calibration_audit +
    observation_dependence + adaptation_debt)."""
    from pipeline import run_unified_audit
    report = run_unified_audit(system_desc)
    band = report.get("unified_band", "")
    status = {
        "GREEN": "GREEN", "green": "GREEN",
        "YELLOW": "YELLOW", "yellow": "YELLOW",
        "RED": "RED", "red": "RED",
    }.get(band, "YELLOW")
    return (status, report)


# ---------------------------------------------------------------
# TOP-LEVEL ENTRY
# ---------------------------------------------------------------

def run_full_audit(
    system_id: str = "unnamed_system",
    *,
    system_description: Optional[dict] = None,
    system_state: Optional[dict[str, float]] = None,
    response_text: Optional[str] = None,
    fork_answers: Optional[dict[str, str]] = None,
    scenario: Optional[dict] = None,
    scenario_kind: Optional[str] = None,   # "cascade" | "refusal" | "trapdoor"
    trapdoor_id: Optional[str] = None,
    function_audit: Optional[dict] = None,
) -> UnifiedAuditReport:
    """Dispatch each input to its matching module and aggregate.

    Any subset of inputs is valid. Modules with missing inputs are
    listed in the report's `modules_skipped` field rather than raising.

    Parameters
    ----------
    system_id : str
        Label propagated into the report.
    system_description : dict, optional
        Feeds the legacy 3-module pipeline.
    system_state : dict, optional
        Feeds assumption_validator.
    response_text : str, optional
        Feeds monoculture_detector, anti_metaphor_locker, and
        negative_space_index unconditionally; also feeds the
        scenario-driven evaluators if scenario_kind is set.
    fork_answers : dict, optional
        Feeds fork_width_scorer (needs >=2 frames).
    scenario : dict, optional
        Scenario payload for cascade / refusal / trapdoor evaluators.
        Use with scenario_kind to select which evaluator runs.
    scenario_kind : "cascade" | "refusal" | "trapdoor", optional
        Which scenario-driven evaluator to invoke against response_text.
    trapdoor_id : str, optional
        Alternative to scenario -- load the trapdoor by id from
        schemas/trapdoors.json.
    function_audit : dict, optional
        {function, base_params, param_ranges, ...} for
        first_principles_audit.

    Returns
    -------
    UnifiedAuditReport
    """
    report = UnifiedAuditReport(system_id=system_id)
    module_statuses: dict[str, str] = {}

    def _dispatch(name: str, runner, *args, **kwargs):
        try:
            status, section = runner(*args, **kwargs)
        except Exception as e:
            # Was: status RED + a red flag. A crash is a gap in the
            # instrument, not a reading of the system.
            report.sections[name] = {
                "error": f"{type(e).__name__}: {e}",
                "exception_type": type(e).__name__,
                "missing_path": getattr(e, "filename", None),
            }
            report.modules_run.append(name)
            module_statuses[name] = GAP_INSTRUMENT_CRASH
            return GAP_INSTRUMENT_CRASH
        report.sections[name] = section
        report.modules_run.append(name)
        module_statuses[name] = status
        return status

    statuses: list[str] = []

    # Legacy pipeline
    if system_description is not None:
        statuses.append(_dispatch("pipeline", _run_legacy_pipeline,
                                  system_description))
    else:
        report.modules_skipped.append("pipeline")

    # Assumption validator
    if system_state is not None:
        statuses.append(_dispatch("assumption_validator",
                                  _run_assumption_validator, system_state))
    else:
        report.modules_skipped.append("assumption_validator")

    # Response-text modules (run unconditionally when text provided)
    if response_text is not None:
        statuses.append(_dispatch("monoculture", _run_monoculture,
                                  response_text))
        statuses.append(_dispatch("anti_metaphor", _run_anti_metaphor,
                                  response_text))
        statuses.append(_dispatch("negative_space", _run_negative_space,
                                  response_text))
    else:
        report.modules_skipped.extend(
            ["monoculture", "anti_metaphor", "negative_space"])

    # Fork-width (needs multiple framed answers)
    if fork_answers is not None and len(fork_answers) >= 2:
        statuses.append(_dispatch("fork_width", _run_fork_width,
                                  fork_answers))
    else:
        report.modules_skipped.append("fork_width")

    # Scenario-driven evaluators
    if response_text is not None and scenario_kind:
        if scenario_kind == "cascade" and scenario is not None:
            statuses.append(_dispatch("cascade", _run_cascade,
                                      response_text, scenario))
        elif scenario_kind == "refusal" and scenario is not None:
            statuses.append(_dispatch("substrate_refusal", _run_refusal,
                                      response_text, scenario))
        elif scenario_kind == "trapdoor":
            statuses.append(_dispatch("trapdoor", _run_trapdoor,
                                      response_text,
                                      trapdoor_id=trapdoor_id,
                                      trapdoor=scenario))
    else:
        for n in ("cascade", "substrate_refusal", "trapdoor"):
            if n not in report.modules_run:
                report.modules_skipped.append(n)

    # First-principles (code audit)
    if function_audit is not None:
        statuses.append(_dispatch("first_principles", _run_first_principles,
                                  function_audit))
    else:
        report.modules_skipped.append("first_principles")

    # Aggregate: two axes.
    for name, status in module_statuses.items():
        report.coverage.extend(
            _coverage_entries(name, status, report.sections.get(name)))
    report.severity = _aggregate_status(statuses)
    report.not_determinable_reason = _not_determinable_reason(statuses)
    report.overall_status = _combined_status(report.severity,
                                             report.coverage)

    # Red flags: driven by the dispatcher's returned status, since
    # different modules expose their status under different key paths.
    for name, status in module_statuses.items():
        if _STATUS_RANK.get(status, 0) >= 3 and name not in (
                f.split(":")[0].strip() for f in report.red_flags):
            section = report.sections.get(name, {})
            msg = ""
            if isinstance(section, dict):
                # Prefer human-readable strings; fall back to status only
                # when every available message is structured data.
                candidates = [
                    section.get("summary"),
                    section.get("cascade", {}).get("message") if isinstance(
                        section.get("cascade"), dict) else None,
                    section.get("interpretation"),
                    section.get("overall_grade"),
                ]
                for c in candidates:
                    if isinstance(c, str) and c.strip():
                        msg = c
                        break
                if not msg:
                    msg = status
            report.red_flags.append(f"{name}: {msg}")

    n_run = len(report.modules_run)
    n_cov = len(report.coverage)
    if report.severity == NOT_DETERMINABLE:
        report.summary = (f"{n_run} module(s) ran; no input was measured. "
                          "Severity not determinable "
                          f"({report.not_determinable_reason}).")
    elif report.severity == "GREEN":
        report.summary = (f"{n_run} module(s) ran; no red flags. "
                          "System is within validated envelope."
                          if n_cov == 0 else
                          f"{n_run} module(s) ran; no red flags on "
                          "measured inputs.")
    elif report.severity == "RED":
        report.summary = (f"{n_run} module(s) ran; "
                          f"{len(report.red_flags)} red flag(s) detected. "
                          "System is outside validated envelope.")
    else:
        report.summary = (f"{n_run} module(s) ran; "
                          "partial degradation. Monitor for convergence.")
    kinds = ", ".join(f"{k}={v}" for k, v in
                      _coverage_by_kind(report.coverage).items())
    report.summary += (f" Coverage: {n_cov} input(s) not measured"
                       + (f" ({kinds}) -- severity covers measured inputs only."
                          if n_cov else "."))

    return report


# ---------------------------------------------------------------
# SELF-TEST
# ---------------------------------------------------------------

if __name__ == "__main__":
    # Full family-firing demo: a response that trips multiple tools.
    naive_response = (
        "Karuk cultural burning is a traditional practice. Step 1: identify "
        "the target stand. Step 2: ignite at the lower edge. Step 3: monitor "
        "closely and adjust. The team has great positive energy and we're "
        "really in the flow state."
    )

    system_state_stressed = {
        "fatigue_score": 7.5,
        "distance_to_collapse": 0.20,
        "hidden_count": 6,
        "friction_ratio": 0.55,
        "K_cred": 0.25,
        "energy_debt_J": 2.5e7,
        "trust_level": 0.30,
        "long_tail_risk": 7.2,
    }

    report = run_full_audit(
        system_id="demo_audit",
        system_state=system_state_stressed,
        response_text=naive_response,
        trapdoor_id="filter_gap",
        scenario_kind="trapdoor",
    )

    print(f"system_id:        {report.system_id}")
    print(f"overall_status:   {report.overall_status}")
    print(f"severity:         {report.severity}")
    print(f"coverage:         {len(report.coverage)}")
    print(f"modules_run:      {report.modules_run}")
    print(f"modules_skipped:  {report.modules_skipped}")
    print(f"summary:          {report.summary}")
    print(f"red_flags:        {len(report.red_flags)}")
    for flag in report.red_flags:
        print(f"  - {flag}")

