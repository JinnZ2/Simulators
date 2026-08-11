"""Investigation: camera traps as an instrument for wildlife population density.

Ecology case: without individual ID, the instrument conflates 1 animal x 10
passes with 10 animals x 1 pass (alias), and density numbers are occupancy/detection
model outputs, not counts.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from instrum.measurand import MeasurandDecomposition
from instrum.transduction import TransductionLink, TransductionChain
from instrum.traceability import TraceabilityChain
from instrum.blindness import BlindSpot, BlindnessMap
from instrum.simulation import inject_and_recover
from instrum.coverage import coverage_report

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

dec = MeasurandDecomposition(
    measurand="Population density of a terrestrial mammal species (individuals/km2)",
    indication="Timestamped shutter-trigger events with images",
    bridge_model="Random encounter model / spatial capture-recapture with estimated detection probability",
    model_rung="M2")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("animal->trigger zone", "Animal must cross the PIR detection wedge",
                     fidelity=0.7, grade="estimated",
                     alias_states=["small/cold-bodied animals under-trigger; trails funnel movement"]),
    TransductionLink("trigger->image", "Shutter latency, exposure, false triggers",
                     fidelity=0.9, grade="measured",
                     alias_states=["vegetation heat flicker triggers empty frames"]),
    TransductionLink("image->species ID", "Human/ML classification",
                     fidelity=0.93, grade="estimated",
                     alias_states=["similar congeners confused at night"]),
    TransductionLink("events->density", "Encounter model with movement-speed & detection-radius parameters",
                     fidelity=0.5, grade="assumed",
                     alias_states=["1 animal x 10 passes ≡ 10 animals x 1 pass without individual ID"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "shutter/PIR timing factory-calibrated"},
    {"level": "working_standard", "status": "broken",
     "note": "no field standard for detection probability; estimated per-study"},
    {"level": "reference_standard", "status": "none", "note": "no reference population of known density"},
    {"level": "SI", "status": "none", "note": "'population density' not SI-realizable"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")

blind = BlindnessMap(spots=[
    BlindSpot("alias_state", "Without individual recognition, passes and individuals are confounded",
              "density estimates scale with animal behavior, not just abundance"),
    BlindSpot("null_state", "Arboreal, fossorial, and trap-shy individuals generate no events",
              "presence/absence and density biased toward bold terrestrial animals"),
    BlindSpot("frame", "Traps placed on trails/access routes for practical reasons",
              "samples the funneled movement network, not the landscape"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable: {blind.absence_interpretable()}")

sim = inject_and_recover(true_value=5.0, chain_fidelity=rep["chain_fidelity"],
                         noise=0.4, model_bias=0.8, tol=0.3)
print(f"PHASE 6: injected density 5.0/km2, recovered {sim.recovered} "
      f"(error {sim.recovery_error:.3f}) -> {'RECOVERY PASS' if sim.passed else 'RECOVERY FAIL: raw event rates cannot be read as density'}")

aspects = [
    {"aspect": "trigger/imaging hardware", "grade": "measured"},
    {"aspect": "species classification", "grade": "estimated"},
    {"aspect": "detection probability", "grade": "estimated"},
    {"aspect": "animal movement parameters", "grade": "assumed"},
    {"aspect": "individual identifiability", "grade": "assumed"},
    {"aspect": "placement bias", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {"investigation_id": "inv-camera-trap-001", "instrument": "Camera trap array",
          "domain": "ecology",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade()},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "camera-trap-density.instrument.json"), "w"), indent=2)
print("record written to outputs/camera-trap-density.instrument.json")
