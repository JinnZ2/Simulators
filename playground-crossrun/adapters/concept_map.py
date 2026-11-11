"""Concept map, step 1E: each concept -> where it lives in each playground, or VOID.

A location is `path :: token`, path relative to that playground's package root
(study-aperture/experimental/playground/ or Simulators/relational-playground/playground/), and the
test resolves every one: the file must exist and the token must occur in it. A location
that cannot be checked that way is not written. VOID means no such object was found
by reading the package; it is a reading, and a test cannot prove an absence.
"""
ROWS = [
    # concept, study-aperture, #257
    ("failure axes (physical / instrument / determination)", "failures.py :: class Axis", "VOID -- l0.py :: def run_status (one status, COMPLETE / INCOMPLETE)"),
    ("axis statuses OK / FAILED / INDETERMINATE / UNTESTED", "failures.py :: class Status", "VOID"),
    ("boundary closure gate before any physics", "gates/l0_closure.py :: def l0_closure_gate", "l0.py :: def audit"),
    ("intervention registry (every control / observer enters the ledger)", "gates/l0_closure.py :: def _check_registration", "VOID"),
    ("ledger declared complete", "gates/l0_closure.py :: declared_complete", "VOID"),
    ("value provenance read by the closure gate", "gates/l0_closure.py :: class ValueProvenance", "VOID -- uncertainty.py :: STATUSES (on values; l0 does not read it)"),
    ("budget declared VOID with a reason", "VOID -- an account not listed is absent", "l0.py :: void_reason"),
    ("noise band on a misclosure", "gates/l0_closure.py :: tolerance (absolute, per account)", "l0.py :: sigma_meas (NOISE within k_sigma)"),
    ("known-answer validation", "validation/known_answer.py :: def validate_known_answers", "known_answer_gate.py :: def certify"),
    ("planted defects on the lab itself", "validation/planted_defects.py :: DEFECTS", "known_answer_gate.py :: def plant"),
    ("null harness", "validation/null_harness.py :: def validate_nulls", "known_answer_gate.py :: def certify_tool (nulls AND signals)"),
    ("FP / TP harness class", "VOID", "harness.py :: def harness_class"),
    ("zero cases is not a pass", "validation/known_answer.py :: KA_NO_CASES", "known_answer_gate.py :: no known-answer cases written (models); certify_tool divides by zero (tools)"),
    ("trust scoped to a context", "equations/substitution.py :: class ScopedDiagnostics", "VOID -- known_answer_gate.py :: def trust (keyed by model name)"),
    ("detection limit from a ladder", "detection/sensitivity.py :: def establish_sensitivity", "VOID"),
    ("non-detection as bounded null", "detection/non_detection.py :: def record_non_detection", "uncertainty.py :: ABSENT_AT_SENSITIVITY"),
    ("scoped absence claim", "detection/scoped_absence.py :: def claim_absence", "VOID"),
    ("UNKNOWN carries what would end it", "lifecycle/unknown_expiry.py :: class ExpiryTrigger (typed)", "uncertainty.py :: expiry_condition (text)"),
    ("UNKNOWN refused without an exit", "VOID -- lifecycle/unknown_expiry.py :: expiry_triggers (may be empty)", "uncertainty.py :: NEEDS_EXPIRY"),
    ("stale reliance on an expired UNKNOWN", "lifecycle/reevaluation.py :: def stale_reliance", "VOID"),
    ("reevaluation keeps the original", "lifecycle/reevaluation.py :: def reevaluate", "VOID"),
    ("frozen anchor", "reference/anchor.py :: class AnchorState", "anchor.py :: def freeze"),
    ("return test (asserted return + tolerance)", "reference/return_test.py :: def return_test", "anchor.py :: def return_diff (deltas, no verdict)"),
    ("one-change branch", "VOID", "anchor.py :: a branch changes ONE thing"),
    ("system continuity vs configuration continuity", "reference/continuity.py :: def classify_continuity", "continuity.py :: class ContinuityMatrix"),
    ("two state tracks, crossing refused", "lifecycle/state_transitions.py :: class Track", "VOID"),
    ("claim tags OBSERVED / DERIVED / PROPOSED", "VOID", "reporting/claims.py :: TAGS"),
    ("claim state / support record", "provenance/claim_status.py :: class ClaimRecord", "VOID"),
    ("coincidence card on cross-family agreement", "VOID", "analysis/coincidence.py :: def open_card"),
    ("measurand identity gates a comparison", "equations/measurand.py :: def compare_substitution", "VOID"),
    ("observer declared before comparison", "applicability/mapping.py :: OBSERVER (one coordinate)", "controls.py :: OBSERVER_FIELDS (three regimes)"),
    ("no universal ranking", "applicability/mapping.py :: no universal ranking", "experiments/comparison.py :: def rank (raises)"),
    ("applicability / domain of validity", "applicability/mapping.py :: def assess", "analysis/applicability.py :: NOT ASSESSED"),
    ("percolation family", "equations/percolation.py :: class BondPercolation (bond, <= 12 edges)", "equations/percolation.py :: spot (site, spread, spotting)"),
    ("branching family", "equations/branching.py :: class FiniteBranching (exact pmf, bounded)", "equations/branching.py :: def branching (fixed / poisson, cap)"),
    ("uncertainty propagation", "VOID -- equations/substitution.py :: deliberately unpropagated", "uncertainty.py :: def propagate (interval corners)"),
    ("denominator bound to cohort members", "audits/denominator_process.py :: def trace_denominator", "VOID"),
    ("distribution-to-mean information loss", "audits/distribution_mean_process.py :: def trace", "VOID"),
    ("value / condition basis vocabulary", "applicability/mapping.py :: class ConditionBasis", "uncertainty.py :: STATUSES"),
    ("pre-registration before a run", "VOID", "../experiments/model_comparison/forest_fire_regime/PREREG.md :: PREREG"),
]


def root(side):
    import os
    import common
    return os.path.join(common.SA_EXP, "playground") if side == "sa" else os.path.join(common.R257, "playground")


def locations():
    """Yield (side, path, token) for every checkable location."""
    for concept, sa, r in ROWS:
        for side, cell in (("sa", sa), ("r257", r)):
            body = cell.split("--", 1)[-1].strip() if cell.startswith("VOID") else cell
            if body == "VOID" or "::" not in body:
                continue
            for part in body.split(";"):
                if "::" not in part:
                    continue
                path, rest = [s.strip() for s in part.split("::", 1)]
                token = rest.split(" (")[0].strip()
                yield side, path, token, concept
