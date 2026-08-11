"""v3.0 tests: blindness-adjusted updates, transduction fidelity, action engine.
Run: python3 -m pytest tests/test_engine_v3.py -q"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from gdprf.engine import (blindness_adjusted_evidence, gradient_update_masked,
                          gradient_update, transduction_chain_fidelity,
                          effective_fidelity_v3)
from gdprf.actions import propose_actions, ActionType

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
EX = json.load(open(os.path.join(ROOT, "examples", "biomass-claim.example.json")))
PROXY = EX["proxies"][0]

def test_blind_state_yields_zero_information_gain():
    prior, post_blind = 0.5, gradient_update_masked(0.5, [(0.9, 0.9, 1.0)])
    assert abs(post_blind - prior) < 1e-9          # fully blind: no update at all

def test_partial_blindness_scales_not_reverses():
    clear = gradient_update_masked(0.5, [(0.9, 0.9, 0.0)])
    masked = gradient_update_masked(0.5, [(0.9, 0.9, 0.5)])
    assert 0.5 < masked < clear                     # partial mask reduces gain, never reverses sign

def test_blindness_prevents_false_absence():
    # a "no signal" observation (negative coupling) from a blind proxy must NOT push posterior down
    post = gradient_update_masked(0.5, [(0.9, -0.9, 0.95)])
    unmasked = gradient_update(0.5, [(0.9, -0.9)])
    assert abs(post - 0.5) < 0.05                     # near-zero information gain
    assert post > unmasked                            # and far less downward than an unmasked reading

def test_transduction_chain_multiplicative():
    chain = [{"stage": "a", "fidelity": 0.9, "grade": "measured"},
             {"stage": "b", "fidelity": 0.5, "grade": "assumed"}]
    assert abs(transduction_chain_fidelity(chain) - 0.45) < 1e-9

def test_effective_fidelity_v3_composition():
    eff, detail = effective_fidelity_v3(PROXY)
    # calibrated 0.71 x chain(0.95*0.98*0.92*0.6=0.514) x convention_only(0.8) ~ 0.292
    assert detail["traceability_status"] == "convention_only"
    assert abs(eff - 0.71 * 0.514 * 0.8) < 0.01
    assert eff < detail["calibrated_fidelity"]      # chain + traceability penalties applied

def test_action_engine_proposes_upgrades():
    proposals = propose_actions(PROXY, EX["claim"])
    types = {p.action_type for p in proposals}
    assert ActionType.COMMISSION_EXPERIMENT in types        # convention_only + assumed links
    assert ActionType.TRIANGULATION_CALL in types           # null/gate states present
    assert ActionType.REQUEST_SENSOR_PLACEMENT in types     # frame biases present
    assert all(p.priority >= 1 for p in proposals)

def test_action_engine_clean_proxy_proposes_nothing_urgent():
    clean = {"traceability_pyramid": {"calibration_chain_status": "intact"},
             "calibration": {"method": "isotonic_regression"},
             "blindness_map": {"null_states": [], "gate_cutoffs": [], "frame_biases": []},
             "transduction_chain": [{"stage": "a", "fidelity": 0.9, "grade": "measured"}]}
    proposals = propose_actions(clean, {"unknown_variable_risk_score": 0.1})
    assert proposals == []

def test_expired_calibration_triggers_scheduling():
    expired = {"traceability_pyramid": {"calibration_chain_status": "expired"},
               "calibration": {"method": "platt_scaling"},
               "blindness_map": {"null_states": [], "gate_cutoffs": [], "frame_biases": []},
               "transduction_chain": []}
    proposals = propose_actions(expired)
    assert proposals[0].action_type == ActionType.SCHEDULE_CALIBRATION
    assert proposals[0].priority == 1

def test_v3_example_validates():
    import jsonschema
    for obj, sf in [(EX["claim"], "claim.schema.json")]:
        jsonschema.validate(obj, json.load(open(os.path.join(ROOT, "schemas", sf))))
    jsonschema.validate(PROXY, json.load(open(os.path.join(ROOT, "schemas", "proxy.schema.json"))))
