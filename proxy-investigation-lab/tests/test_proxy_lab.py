"""Proxy lab test suite. Run: python3 -m pytest tests/ -q"""
import json, os, sys, subprocess
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from proxy_lab.grounding import ChainLink, GroundingChain
from proxy_lab.instruments import Instrument
from proxy_lab.synthetic import make_world, estimate_instrument, recovery_score
from proxy_lab.calibration import calibrate, expected_calibration_error, platt_fit, platt_predict
from proxy_lab.coverage import coverage_report

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")

def test_chain_fidelity_multiplicative():
    c = GroundingChain([ChainLink("a", "m", 0.8, "measured"),
                        ChainLink("b", "m", 0.5, "assumed")])
    assert abs(c.chain_fidelity() - 0.4) < 1e-9
    assert c.weakest_link().name == "b"

def test_instrument_snr():
    i = Instrument("t", 0.9, 0.15, 0.0)
    assert i.snr(0.45) == 3.0

def test_synthetic_recovery_passes_on_known_world():
    w = make_world(n=3000, true_bias=0.07, true_noise=0.11, seed=3)
    est = estimate_instrument(w)
    assert recovery_score(w, est)["passed"]

def test_synthetic_estimator_sees_no_truth():
    w = make_world(n=500, seed=5)
    est = estimate_instrument(w)
    assert "bias" not in est and "estimated_bias" in est  # reads estimates, not answer key

def test_isotonic_calibration_improves_ece():
    rng = np.random.default_rng(0)
    latent = rng.beta(2, 2, 3000)
    raw = np.clip(latent + rng.normal(0.15, 0.2, 3000), 0, 1)  # overconfident
    y = (latent > 0.6).astype(float)
    cal = calibrate(raw, y, method="isotonic")
    assert cal["improved"] and cal["ece_after"] < 0.1

def test_platt_calibration_improves_ece():
    rng = np.random.default_rng(1)
    latent = rng.beta(2, 2, 3000)
    raw = np.clip(latent + rng.normal(0.1, 0.2, 3000), 0, 1)
    y = (latent > 0.6).astype(float)
    cal = calibrate(raw, y, method="platt")
    assert cal["improved"] and cal["ece_after"] < 0.1

def test_ece_perfect_calibration_near_zero():
    conf = np.array([0.9]*100 + [0.1]*100)
    out = np.array([1.0]*90 + [0.0]*10 + [0.0]*90 + [1.0]*10)
    assert expected_calibration_error(conf, out, bins=2) < 0.05

def test_coverage_fraction_and_verdict():
    cov = coverage_report([
        {"aspect": "a", "grade": "measured", "grounding_level": "G1", "upgrade_path": "-"},
        {"aspect": "b", "grade": "assumed", "grounding_level": "G5", "upgrade_path": "run exp"}])
    assert cov["grounded_fraction"] == 0.5 and cov["weakest_aspects"][0] == "b"

def test_investigation_records_validate():
    import jsonschema
    inv_schema = json.load(open(os.path.join(ROOT, "schemas", "investigation.schema.json")))
    exp_schema = json.load(open(os.path.join(ROOT, "schemas", "experiment.schema.json")))
    for f in ["burnout-latency.investigation.json", "port-dwell-time.investigation.json"]:
        p = os.path.join(ROOT, "outputs", f)
        if os.path.exists(p):
            jsonschema.validate(json.load(open(p)), inv_schema)
    p = os.path.join(ROOT, "outputs", "burnout-synth.experiment.json")
    if os.path.exists(p):
        jsonschema.validate(json.load(open(p)), exp_schema)

def test_both_experiments_run_clean():
    for exp in ["burnout_latency", "port_dwell_time"]:
        r = subprocess.run(f"python3 experiments/{exp}/run.py", shell=True,
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0 and "RECOVERY PASS" in r.stdout and "IMPROVED" in r.stdout

def test_goodhart_redteam_detects_collapse():
    from proxy_lab.goodhart import red_team
    res = red_team()
    assert res.fidelity_collapse > 0.05          # gaming measurably decouples proxy
    assert res.gamed_correlation < res.baseline_correlation
    assert "slope" in res.detection_surface["interpretation"]

def test_batch_grades_whole_catalog():
    from proxy_lab.catalog import CATALOG
    from proxy_lab.batch import run_batch
    results = run_batch(CATALOG)
    assert len(results) == len(CATALOG)
    assert results[0]["grounded_fraction"] >= results[-1]["grounded_fraction"]
    assert all(0 <= r["chain_fidelity"] <= 1 for r in results)

def test_wim_experiment_grounds_high():
    r = subprocess.run("python3 experiments/wim_pavement/run.py", shell=True,
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0 and "well grounded" in r.stdout and "RECOVERY PASS" in r.stdout
