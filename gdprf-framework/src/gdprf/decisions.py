"""Decision points — turning belief state into governed action.

A confidence gradient is not a decision. Decision points are explicit thresholds
where the system must DO something: deploy, research further, hold, escalate to a
human, or abort. Bands combine the confidence gradient with the
unknown_variable_risk_score, so high confidence AND high ignorance does not
silently deploy — it escalates.

Policy bands are configuration, not constants: every deployment tunes them and
records the chosen policy in the provenance ledger.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Action(Enum):
    DEPLOY = "deploy"              # act on the claim (deployment-facing output)
    RESEARCH = "research"          # keep gathering evidence; research-mode only
    HOLD = "hold"                  # insufficient evidence either way
    ESCALATE = "escalate"          # human review required
    ABORT = "abort"                # governed proxy violation or failed gate — stop


@dataclass
class DecisionPolicy:
    """Thresholds are deployment configuration — tune per domain, record in ledger."""
    deploy_confidence: float = 0.80
    research_confidence: float = 0.55
    max_unknown_risk_for_deploy: float = 0.30
    max_ece_for_deploy: float = 0.10        # calibration quality floor
    escalate_unknown_risk: float = 0.45     # high confidence + high ignorance = human
    governance_enforced: bool = True


@dataclass
class DecisionPoint:
    """The record of a decision being made at a specific point."""
    claim_id: str
    action: Action
    rationale: str
    confidence: float
    unknown_variable_risk: float
    blocked_by: list[str] = field(default_factory=list)


def evaluate(claim: dict, proxies: list[dict], edges: list[dict],
             policy: Optional[DecisionPolicy] = None) -> DecisionPoint:
    """Evaluate a claim at its decision point.

    Checks, in order of precedence:
    1. Governance — any unsatisfied 'governs' edge on a deployment-bound proxy -> ABORT
    2. Gate — triggered hidden-variable search with failed gate -> ESCALATE
    3. Calibration — deploy requires calibrated proxies with acceptable ECE
    4. Bands — confidence vs. unknown-variable risk -> DEPLOY/RESEARCH/HOLD/ESCALATE
    """
    policy = policy or DecisionPolicy()
    conf = claim["confidence_gradient"]
    uvr = claim["unknown_variable_risk_score"]
    cid = claim["claim_id"]
    blocked = []

    # 1. Governance (Amendment 5)
    if policy.governance_enforced:
        governed_ids = {e["target_id"] for e in edges
                        if e.get("relationship_type") == "governs"}
        for p in proxies:
            if p["proxy_id"] in governed_ids and p["proxy_id"] in claim["assigned_proxies"]:
                blocked.append(f"proxy {p['proxy_id']} under unsatisfied governs edge")
        if blocked:
            return DecisionPoint(cid, Action.ABORT,
                                 "deployment blocked by governance constraint(s); "
                                 "research-mode inference unaffected", conf, uvr, blocked)

    # 2. Identification gate (Amendment 4)
    hvs = claim.get("hidden_variable_search", {})
    if hvs.get("triggered") and hvs.get("identification_gate", {}).get("status") in ("failed", "pending"):
        return DecisionPoint(cid, Action.ESCALATE,
                             "residual variance trigger with unpassed identification gate; "
                             "human must adjudicate unexplained ignorance", conf, uvr, blocked)

    # 3. Calibration floor (Amendment 1)
    uncalibrated = [p["proxy_id"] for p in proxies
                    if p.get("calibration", {}).get("method", "none") == "none"]
    bad_ece = [p["proxy_id"] for p in proxies
               if (p.get("calibration", {}).get("expected_calibration_error") or 0) > policy.max_ece_for_deploy]

    # 4. Bands
    if conf >= policy.deploy_confidence:
        if uvr > policy.escalate_unknown_risk:
            return DecisionPoint(cid, Action.ESCALATE,
                                 f"high confidence ({conf:.2f}) but unknown-variable risk "
                                 f"{uvr:.2f} exceeds {policy.escalate_unknown_risk} — "
                                 "confident AND ignorant requires human review", conf, uvr, blocked)
        if uvr > policy.max_unknown_risk_for_deploy or uncalibrated or bad_ece:
            reasons = ([f"uvr {uvr:.2f} > {policy.max_unknown_risk_for_deploy}"] if uvr > policy.max_unknown_risk_for_deploy else [])                       + ([f"uncalibrated: {uncalibrated}"] if uncalibrated else [])                       + ([f"ECE above floor: {bad_ece}"] if bad_ece else [])
            return DecisionPoint(cid, Action.RESEARCH,
                                 "confidence band met but deploy preconditions failed: " + "; ".join(reasons),
                                 conf, uvr, blocked)
        return DecisionPoint(cid, Action.DEPLOY,
                             f"confidence {conf:.2f} >= {policy.deploy_confidence}, "
                             f"uvr {uvr:.2f} within tolerance, calibration floor met",
                             conf, uvr, blocked)
    if conf >= policy.research_confidence:
        return DecisionPoint(cid, Action.RESEARCH,
                             f"confidence {conf:.2f} in research band "
                             f"[{policy.research_confidence}, {policy.deploy_confidence})",
                             conf, uvr, blocked)
    return DecisionPoint(cid, Action.HOLD,
                         f"confidence {conf:.2f} below research band — insufficient evidence",
                         conf, uvr, blocked)
