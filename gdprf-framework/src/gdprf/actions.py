"""Action Proposal Engine — turn epistemic limitations into upgrade tasks.

Phase 7 identifies what is ungrounded; this engine makes the agent *act* on it:
propose sensor placements, calibration scheduling, inter-instrument
triangulation calls, or experiments — each tied to the specific aspect and
grounding gap it would close.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum


class ActionType(Enum):
    SCHEDULE_CALIBRATION = "schedule_calibration"
    REQUEST_SENSOR_PLACEMENT = "request_sensor_placement"
    TRIANGULATION_CALL = "triangulation_call"        # inter-instrument agreement check
    COMMISSION_EXPERIMENT = "commission_experiment"   # named study / benchmark
    HUMAN_REVIEW = "human_review"


@dataclass
class ActionProposal:
    action_type: ActionType
    target_aspect: str          # what is ungrounded
    rationale: str
    expected_upgrade: str       # e.g. "assumed -> estimated"
    priority: int               # 1 = highest
    cost_class: str = "medium"  # low | medium | high


def propose_actions(proxy: dict, claim: dict | None = None) -> list[ActionProposal]:
    """Generate upgrade tasks from a proxy's grounding gaps."""
    proposals: list[ActionProposal] = []
    prio = 0

    # 1. Traceability gaps -> calibration scheduling
    trace = proxy.get("traceability_pyramid", {})
    status = trace.get("calibration_chain_status", "intact")
    if status in ("expired", "broken"):
        prio += 1
        proposals.append(ActionProposal(
            ActionType.SCHEDULE_CALIBRATION, "traceability_pyramid",
            f"calibration chain is {status}; fidelity is penalized until restored",
            "restore trace factor to 1.0 (measured)", prio, "medium"))
    elif status == "convention_only":
        prio += 1
        proposals.append(ActionProposal(
            ActionType.COMMISSION_EXPERIMENT, "traceability_pyramid",
            "no primary standard; chain terminates at convention/inter-lab comparison",
            "estimated -> measured (requires standards infrastructure)", prio, "high"))

    # 2. Calibration gaps -> validation-set commissioning
    cal = proxy.get("calibration", {})
    if cal.get("method", "none") == "none":
        prio += 1
        proposals.append(ActionProposal(
            ActionType.COMMISSION_EXPERIMENT, "calibration",
            "proxy is uncalibrated; evidence is shrunk toward the prior",
            "uncalibrated -> calibrated_fidelity (ECE-tracked)", prio, "medium"))

    # 3. Blindness gaps -> triangulation and placement
    blind = proxy.get("blindness_map", {})
    if blind.get("null_states") or blind.get("gate_cutoffs"):
        prio += 1
        proposals.append(ActionProposal(
            ActionType.TRIANGULATION_CALL, "blindness_map",
            "null/gate states make absence uninterpretable; cross-check with a "
            "physically distinct instrument",
            "epistemic_mask_score reduction via triangulation", prio, "medium"))
    if blind.get("frame_biases"):
        prio += 1
        proposals.append(ActionProposal(
            ActionType.REQUEST_SENSOR_PLACEMENT, "frame_biases",
            "sampling frame structurally excludes domain space: "
            + "; ".join(blind["frame_biases"][:2]),
            "frame bias closed by new placements", prio, "high"))

    # 4. Assumed transduction links -> targeted experiments
    assumed = [l["stage"] for l in proxy.get("transduction_chain", [])
               if l.get("grade") == "assumed"]
    if assumed:
        prio += 1
        proposals.append(ActionProposal(
            ActionType.COMMISSION_EXPERIMENT, "transduction_chain",
            "assumed links: " + "; ".join(assumed),
            "assumed -> estimated/measured per link", prio, "medium"))

    # 5. High unknown-variable risk -> human review
    if claim and claim.get("unknown_variable_risk_score", 0) > 0.45:
        prio += 1
        proposals.append(ActionProposal(
            ActionType.HUMAN_REVIEW, "unknown_variable_risk_score",
            "risk score above 0.45; automated upgrades exhausted",
            "human adjudication of unexplained ignorance", prio, "low"))

    return proposals


def proposals_to_json(proposals: list[ActionProposal]) -> list[dict]:
    return [{**asdict(p), "action_type": p.action_type.value} for p in proposals]
