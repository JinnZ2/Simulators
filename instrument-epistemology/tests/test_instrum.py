"""Instrument epistemology test suite. Run: python3 -m pytest tests/ -q"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from instrum.measurand import MeasurandDecomposition
from instrum.transduction import TransductionLink, TransductionChain
from instrum.traceability import TraceabilityChain
from instrum.blindness import BlindSpot, BlindnessMap
from instrum.simulation import inject_and_recover
from instrum.coverage import coverage_report

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")

def test_measurand_rung_uncertainty():
    d = MeasurandDecomposition("a", "b", "c", "M3")
    assert "inverse" in d.dominant_uncertainty()

def test_chain_multiplicative_and_weakest():
    c = TransductionChain([TransductionLink("x", "p", 0.9, "measured"),
                           TransductionLink("y", "p", 0.5, "assumed")])
    assert abs(c.chain_fidelity() - 0.45) < 1e-9 and c.weakest_link().name == "y"

def test_traceability_grades():
    ok = TraceabilityChain([{"level": "a", "status": "ok"}])
    broken = TraceabilityChain([{"level": "instrument", "status": "ok"},
                                {"level": "working_standard", "status": "ok"},
                                {"level": "reference_standard", "status": "broken", "note": "n/a"}])
    none = TraceabilityChain([{"level": "instrument", "status": "broken", "note": "dead"}])
    assert ok.unbroken() and ok.grade() == "measured"
    assert broken.grade() == "estimated" and "reference_standard" in broken.highest_break()
    assert none.grade() == "assumed"

def test_blindness_absence_rule():
    gated = BlindnessMap([BlindSpot("gate", "d", "c")])
    clear = BlindnessMap([BlindSpot("alias_state", "d", "c")])
    assert not gated.absence_interpretable()          # gates make 'absence' uninterpretable
    assert clear.absence_interpretable()

def test_simulation_catches_unmodelled_bias():
    sim = inject_and_recover(100.0, chain_fidelity=0.5, noise=1.0, model_bias=5.0, tol=0.1)
    assert not sim.passed and sim.recovery_error > 0.3  # ideal-model pipeline badly wrong
    sim2 = inject_and_recover(100.0, chain_fidelity=0.99, noise=1.0, model_bias=0.0, tol=0.1)
    assert sim2.passed

def test_coverage_verdicts():
    assert coverage_report([{"aspect": "a", "grade": "measured"}])["verdict"] == "well grounded"
    assert coverage_report([{"aspect": "a", "grade": "assumed"}])["verdict"].startswith("mostly assumed")

def test_records_validate_against_schema():
    import jsonschema
    schema = json.load(open(os.path.join(ROOT, "schemas", "instrument.schema.json")))
    for f in ["lidar-biomass.instrument.json", "edna-biodiversity.instrument.json",
              "camera-trap-density.instrument.json"]:
        p = os.path.join(ROOT, "outputs", f)
        if os.path.exists(p):
            jsonschema.validate(json.load(open(p)), schema)

def test_all_experiments_run():
    for exp in ["lidar_biomass", "edna_biodiversity", "camera_trap_density",
                "satellite_sst", "isotope_diet", "seismometer"]:
        r = subprocess.run(f"python3 experiments/{exp}/run.py", shell=True,
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0 and "PHASE 7" in r.stdout

def test_comparative_report_runs_and_ranks():
    r = subprocess.run("python3 experiments/comparative_report/run.py", shell=True,
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0 and "seismometer" in r.stdout
    lines = [l for l in r.stdout.splitlines() if l.startswith("|") and "Instrument" not in l and "---" not in l]
    grounded = [float(l.split("|")[7]) for l in lines]
    assert grounded == sorted(grounded, reverse=True)  # sorted by grounded fraction
