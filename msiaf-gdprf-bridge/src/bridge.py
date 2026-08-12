"""MSIAF x GDPRF bridge — run an MSIAF case file through the GDPRF engine.

Each pathway link (D4->D2 etc.) is a GDPRF claim; investigation evidence is
proxy instruments; the systemic determination aggregates link posteriors.
"""
from __future__ import annotations
import copy, json, math, os, sys

_GDPRF_SRC = os.environ.get(
    "GDPRF_SRC",
    os.path.join(os.path.dirname(__file__), "..", "..", "gdprf-framework", "src"))
sys.path.insert(0, os.path.abspath(_GDPRF_SRC))

from gdprf.engine import (calibrate_fidelity, cascade_fidelity, gradient_update,
                          identification_gate)
from gdprf.provenance import ProvenanceLedger, ProvenanceRecord
from gdprf.decisions import DecisionPolicy, evaluate, Action

ENGINE = "msiaf-gdprf-bridge 1.0.0 / gdprf-engine 2.1.0"


class Investigation:
    def __init__(self, case: dict):
        self.case = copy.deepcopy(case)  # never mutate the caller's case file
        self.ledger = ProvenanceLedger()
        self._n = 0
        self.link_results = []

    def rec(self, entity, activity, inputs, outputs):
        self._n += 1
        return self.ledger.append(ProvenanceRecord(
            record_id=f"inv-{self._n:04d}", entity=entity, activity=activity,
            agent=ENGINE, inputs=inputs, outputs=outputs))

    def run_link(self, link: dict) -> dict:
        claim = link["claim"]
        cid = claim["claim_id"]
        evidences = []
        for p in link["proxies"]:
            fid, was_cal = calibrate_fidelity(p)
            src = p["metrology"]["provenance"]
            self.rec(p["proxy_id"], "evidence_ingestion",
                     {"phase_evidence": p["observable_metric"],
                      "provenance": {k: v for k, v in src.items() if k.endswith("_source")}},
                     {"instrument": p["metrology"]["sensor_type"]})
            self.rec(p["proxy_id"], "calibration",
                     {"raw_fidelity": p["fidelity_gradient"],
                      "method": p["calibration"]["method"]},
                     {"effective_fidelity": round(fid, 4), "was_calibrated": was_cal})
            evidences.append(fid)
        casc = cascade_fidelity(evidences)
        coupling = link["edge"]["coupling_strength"]
        prior = claim["confidence_gradient"]
        posterior = gradient_update(prior, [(casc, coupling)])
        claim["confidence_gradient"] = round(posterior, 4)
        self.rec(cid, "gradient_update",
                 {"pathway": link["pathway"], "prior": prior,
                  "cascade_fidelity": round(casc, 4), "coupling": coupling},
                 {"posterior": claim["confidence_gradient"]})
        gate = identification_gate(claim)
        self.rec(cid, "gate_decision",
                 {"triggered": claim["hidden_variable_search"]["triggered"]},
                 {"status": gate.status, "action": gate.action})
        result = {"link_id": link["link_id"], "pathway": link["pathway"],
                  "claim_id": cid, "posterior": claim["confidence_gradient"],
                  "uvr": claim["unknown_variable_risk_score"],
                  "gate": gate.status, "cascade_fidelity": round(casc, 4),
                  "claim": claim, "proxies": link["proxies"]}
        self.link_results.append(result)
        return result

    def aggregate(self) -> dict:
        """Systemic determination: chain (conjunctive) and weakest-link bounds."""
        posts = [r["posterior"] for r in self.link_results]
        chain = math.prod(posts)
        weakest = min(posts)
        divergence = weakest - chain
        triggered = divergence > 0.35  # residual variance between bounds
        agg = {
            "claim_id": self.case["case_id"] + "-determination",
            "confidence_gradient": round(chain, 4),
            "weakest_link_bound": round(weakest, 4),
            "bound_divergence": round(divergence, 4),
            "unknown_variable_risk_score": round(
                max(r["uvr"] for r in self.link_results), 4),
            "assigned_proxies": [p["proxy_id"] for r in self.link_results
                                 for p in r["proxies"]],
            "hidden_variable_search": {
                "triggered": triggered,
                "residual_variance_observed": round(divergence, 4),
                "threshold": 0.35,
                "identification_gate": {
                    "status": "failed" if triggered else "not_triggered",
                    "method": "bound-divergence analysis" if triggered else None,
                    "assumptions": ["link posteriors are conditionally independent given their proxies"] if triggered else []}}}
        self.rec(agg["claim_id"], "cascade_assembly",
                 {"link_posteriors": {r["pathway"]: r["posterior"] for r in self.link_results}},
                 {"chain": agg["confidence_gradient"],
                  "weakest_link": agg["weakest_link_bound"],
                  "residual_trigger": triggered})
        return agg

    def decide(self, agg: dict) -> object:
        policy = DecisionPolicy(deploy_confidence=0.70,
                                max_unknown_risk_for_deploy=0.35,
                                escalate_unknown_risk=0.45)
        all_proxies = [p for r in self.link_results for p in r["proxies"]]
        dp = evaluate(agg, all_proxies, [], policy)
        self.rec(agg["claim_id"], "decision_point",
                 {"chain_confidence": dp.confidence, "uvr": dp.unknown_variable_risk,
                  "policy": {"deploy_confidence": policy.deploy_confidence,
                             "escalate_unknown_risk": policy.escalate_unknown_risk}},
                 {"action": dp.action.value, "rationale": dp.rationale})
        return dp
