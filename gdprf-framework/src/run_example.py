"""End-to-end run: burnout claim through engine + provenance + decision point.

Usage:  python3 src/run_example.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gdprf.engine import (calibrate_fidelity, cascade_fidelity, gradient_update,
                          identification_gate, bias_correction)
from gdprf.provenance import ProvenanceLedger, ProvenanceRecord
from gdprf.decisions import DecisionPolicy, evaluate

EX = json.load(open(os.path.join(os.path.dirname(__file__), "..", "examples",
                                 "burnout-claim.example.json")))
claim, proxies, edges = EX["claim"], EX["proxies"], EX["edges"]
ledger = ProvenanceLedger()
ENGINE = "gdprf-engine 2.1.0"
n = [0]
def rec(entity, activity, inputs, outputs):
    n[0] += 1
    return ledger.append(ProvenanceRecord(
        record_id=f"rec-{n[0]:04d}", entity=entity, activity=activity,
        agent=ENGINE, inputs=inputs, outputs=outputs))

# --- Step 3: metrological evaluation (provenance-weighted bias correction) ---
evidences = []
for p in proxies:
    m = p["metrology"]
    raw_signal = 0.35  # observed deviation from baseline, stand-in measurement
    corrected, resid = bias_correction(raw_signal, m["systematic_bias"],
                                       m["provenance"]["systematic_bias_source"])
    rec(p["proxy_id"], "evidence_ingestion",
        {"raw_signal": raw_signal, "systematic_bias": m["systematic_bias"],
         "bias_source": m["provenance"]["systematic_bias_source"]},
        {"corrected_signal": round(corrected, 4), "residual_bias_uncertainty": round(resid, 4)})

    # --- Step 3.5: calibration ---
    fid, was_cal = calibrate_fidelity(p)
    rec(p["proxy_id"], "calibration",
        {"raw_fidelity": p["fidelity_gradient"], "method": p["calibration"]["method"]},
        {"effective_fidelity": round(fid, 4), "was_calibrated": was_cal,
         "ece": p["calibration"].get("expected_calibration_error")})
    evidences.append(fid)

# cascade: claim <- P1 <- P2 ; effective fidelity of the chain
casc = cascade_fidelity(evidences[::-1])
edge_by_src = {e["source_id"]: e for e in edges if e["relationship_type"] == "proxy_of"}
coupling = edge_by_src[proxies[0]["proxy_id"]]["coupling_strength"]
rec(claim["claim_id"], "cascade_assembly",
    {"chain": [p["proxy_id"] for p in reversed(proxies)]},
    {"cascade_fidelity": round(casc, 4), "edge_coupling": coupling})

# --- Step 4: gradient update ---
prior = claim["confidence_gradient"]
posterior = gradient_update(prior, [(casc, coupling)])
rec(claim["claim_id"], "gradient_update",
    {"prior": prior, "evidence": [{"fidelity": round(casc, 4), "coupling": coupling}]},
    {"posterior": round(posterior, 4)})
claim["confidence_gradient"] = round(posterior, 4)

# --- Step 5: identification gate (not triggered here) ---
gate = identification_gate(claim)
rec(claim["claim_id"], "gate_decision",
    {"triggered": claim["hidden_variable_search"]["triggered"]},
    {"status": gate.status, "action": gate.action})

# --- Decision point ---
policy = DecisionPolicy()
dp = evaluate(claim, proxies, edges, policy)
rec(claim["claim_id"], "decision_point",
    {"confidence": dp.confidence, "uvr": dp.unknown_variable_risk,
     "policy": {"deploy_confidence": policy.deploy_confidence,
                "escalate_unknown_risk": policy.escalate_unknown_risk}},
    {"action": dp.action.value, "rationale": dp.rationale, "blocked_by": dp.blocked_by})

# --- Report ---
print(f"prior {prior} -> posterior {dp.confidence}")
print(f"cascade fidelity: {casc:.3f}")
print(f"gate: {gate.status} — {gate.action}")
print(f"DECISION: {dp.action.value.upper()} — {dp.rationale}")
if dp.blocked_by:
    print(f"blocked by: {dp.blocked_by}")
print(f"provenance ledger: {len(ledger.records)} records, chain valid: {ledger.verify_chain()}")
out = os.path.join(os.path.dirname(__file__), "..", "examples", "burnout-run-provenance.json")
json.dump(json.loads(ledger.to_json()), open(out, "w"), indent=2)
print(f"ledger written to {out}")
