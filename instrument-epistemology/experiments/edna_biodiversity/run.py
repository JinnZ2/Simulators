"""Investigation: eDNA metabarcoding as an instrument for species presence.

Biology case: the transduction chain is biochemical (shedding -> capture -> PCR
-> sequencing -> library match), the reference 'standard' is a sequence library
with known gaps, and the gate blind spot (library miss = false absence) is the
defining hazard.
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
    measurand="Presence/absence (and relative abundance) of species in a water body",
    indication="Amplicon sequence read counts per barcode locus",
    bridge_model="Reference-library taxonomic assignment + occupancy/detection model",
    model_rung="M2")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("organism->DNA shedding", "Species shed DNA at wildly different rates",
                     fidelity=0.55, grade="estimated",
                     alias_states=["high shedder at low abundance looks like low shedder at high abundance"]),
    TransductionLink("shedding->capture", "Water sampling + filtration",
                     fidelity=0.7, grade="estimated",
                     alias_states=["DNA transport from upstream — species never present at site"]),
    TransductionLink("capture->amplification", "PCR with locus-specific primers",
                     fidelity=0.6, grade="estimated",
                     alias_states=["primer mismatch suppresses entire taxonomic groups"]),
    TransductionLink("amplification->sequencing", "High-throughput read generation",
                     fidelity=0.95, grade="measured"),
    TransductionLink("reads->taxon assignment", "Match against reference barcode library",
                     fidelity=0.75, grade="estimated",
                     alias_states=["library gap: present species assigns to wrong taxon or nothing"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "sequencer base-call quality calibrated"},
    {"level": "working_standard", "status": "lapsed",
     "note": "mock community standards exist but not run every batch"},
    {"level": "reference_standard", "status": "broken",
     "note": "reference barcode libraries are incomplete community resources, not standards"},
    {"level": "SI", "status": "none", "note": "'species presence' has no SI realization"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")

blind = BlindnessMap(spots=[
    BlindSpot("gate", "Species absent from reference library reads as ABSENT from the water body",
              "false absences for exactly the rare/undescribed species surveys care most about"),
    BlindSpot("null_state", "Low-shedding or ephemeral species produce no signal at sampling time",
              "presence becomes a lottery of shedding kinetics, not occupancy"),
    BlindSpot("alias_state", "Upstream transport deposits DNA of species not living at the site",
              "false presences inflate richness estimates"),
    BlindSpot("frame", "Sampling only open water misses benthic/crevice communities",
              "community composition skewed toward pelagic taxa"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable as absence: "
      f"{blind.absence_interpretable()}")

sim = inject_and_recover(true_value=1.0, chain_fidelity=rep["chain_fidelity"],
                         noise=0.05, model_bias=0.0, tol=0.5)
print(f"PHASE 6: injected presence signal 1.0, recovered {sim.recovered} "
      f"-> {'chain passes presence/absence at generous tolerance' if sim.passed else 'even PRESENCE fails without detection modelling'}")

aspects = [
    {"aspect": "sequencing chemistry", "grade": "measured"},
    {"aspect": "PCR amplification fidelity", "grade": "estimated"},
    {"aspect": "shedding-rate heterogeneity", "grade": "assumed"},
    {"aspect": "reference library completeness", "grade": "assumed"},
    {"aspect": "transport/alias correction", "grade": "estimated"},
    {"aspect": "detection probability model", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {"investigation_id": "inv-edna-001", "instrument": "eDNA metabarcoding assay",
          "domain": "biology",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade()},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "edna-biodiversity.instrument.json"), "w"), indent=2)
print("record written to outputs/edna-biodiversity.instrument.json")
