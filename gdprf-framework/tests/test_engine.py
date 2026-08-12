"""Test suite for the GDPRF reference engine. Run: python3 -m pytest tests/ -q"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from gdprf.engine import (calibrate_fidelity, cascade_fidelity, gradient_update,
                          identification_gate, bias_correction, metrology_weight,
                          snr_passes)
from gdprf.provenance import ProvenanceLedger, ProvenanceRecord
from gdprf.decisions import DecisionPolicy, evaluate, Action

P_CAL = {"proxy_id": "p1", "fidelity_gradient": 0.72,
         "calibration": {"method": "isotonic_regression", "calibrated_fidelity": 0.61,
                         "expected_calibration_error": 0.04}}
P_RAW = {"proxy_id": "p2", "fidelity_gradient": 0.9,
         "calibration": {"method": "none", "calibrated_fidelity": None}}

def test_provenance_weights():
    assert metrology_weight("measured") > metrology_weight("estimated") > metrology_weight("assumed")

def test_snr_filter():
    assert snr_passes(0.5, 0.15) and not snr_passes(0.2, 0.15)

def test_assumed_bias_leaves_residual():
    c1, r1 = bias_correction(0.35, 0.1, "measured")
    c2, r2 = bias_correction(0.35, 0.1, "assumed")
    assert r1 == 0 and r2 > 0 and abs(c1 - 0.25) < 1e-9 and c2 > c1

def test_calibration_uses_calibrated_value():
    fid, was = calibrate_fidelity(P_CAL)
    assert was and fid == 0.61

def test_uncalibrated_is_shrunk():
    fid, was = calibrate_fidelity(P_RAW)
    assert not was and abs(fid - 0.7) < 1e-9  # 0.5 + (0.9-0.5)*0.5

def test_cascade_multiplicative():
    assert abs(cascade_fidelity([0.8, 0.5]) - 0.4) < 1e-9

def test_gradient_update_direction_and_bounds():
    up = gradient_update(0.5, [(0.8, 0.9)])
    down = gradient_update(0.5, [(0.8, -0.9)])
    assert up > 0.5 > down and 0 < up < 1 and 0 < down < 1

def test_gate_freezes_when_failed():
    claim = {"hidden_variable_search": {"triggered": True,
             "identification_gate": {"status": "failed", "assumptions": []}}}
    g = identification_gate(claim)
    assert g.status == "failed" and "frozen" in g.action

def test_ledger_chain_verification_and_tamper_evidence():
    led = ProvenanceLedger()
    led.append(ProvenanceRecord("r1", "e", "a", "eng"))
    led.append(ProvenanceRecord("r2", "e", "b", "eng"))
    assert led.verify_chain()
    led.records[0].outputs["tampered"] = True
    assert not led.verify_chain()

def _claim(conf, uvr, triggered=False):
    return {"claim_id": "c", "confidence_gradient": conf,
            "unknown_variable_risk_score": uvr, "assigned_proxies": ["p1"],
            "hidden_variable_search": {"triggered": triggered,
              "identification_gate": {"status": "not_triggered" if not triggered else "failed"}}}

def test_decision_deploy():
    dp = evaluate(_claim(0.85, 0.2), [P_CAL], [], DecisionPolicy())
    assert dp.action == Action.DEPLOY

def test_decision_escalates_confident_but_ignorant():
    dp = evaluate(_claim(0.9, 0.5), [P_CAL], [], DecisionPolicy())
    assert dp.action == Action.ESCALATE

def test_decision_abort_on_governance():
    gov = [{"source_id": "policy", "target_id": "p1", "relationship_type": "governs"}]
    dp = evaluate(_claim(0.9, 0.1), [P_CAL], gov, DecisionPolicy())
    assert dp.action == Action.ABORT

def test_decision_escalate_on_failed_gate():
    dp = evaluate(_claim(0.9, 0.1, triggered=True), [P_CAL], [], DecisionPolicy())
    assert dp.action == Action.ESCALATE

def test_example_validates_and_runs():
    import subprocess
    r = subprocess.run("python3 src/run_example.py", shell=True,
                       cwd=os.path.join(os.path.dirname(__file__), ".."),
                       capture_output=True, text=True)
    assert r.returncode == 0 and "chain valid: True" in r.stdout
