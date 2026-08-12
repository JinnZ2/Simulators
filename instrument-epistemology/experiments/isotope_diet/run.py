"""Investigation: stable isotope ratios (d13C, d15N) as an instrument for
reconstructing animal diet.

Biology case: the mass spectrometer is exquisitely traceable, but the bridge
model (isotopic mixing model + trophic discrimination factors) is biological —
and the measurand itself ('diet') is an integration the animal's tissues made,
not the instrument.
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
    measurand="Proportional diet composition over tissue integration window (weeks-months)",
    indication="Isotope ratios d13C/d15N in consumer tissue (IRMS delta values)",
    bridge_model="Bayesian mixing model with trophic discrimination factors (TDFs)",
    model_rung="M2")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("diet->tissue incorporation", "Routing of dietary isotopes into tissue with TDFs",
                     fidelity=0.55, grade="assumed",
                     alias_states=["TDFs vary with species, tissue, diet quality, physiology"]),
    TransductionLink("tissue->sample prep", "Lipid extraction, preservation effects",
                     fidelity=0.85, grade="estimated",
                     alias_states=["lipids skew d13C; ethanol shifts ratios"]),
    TransductionLink("sample->IRMS reading", "Isotope ratio mass spectrometry",
                     fidelity=0.98, grade="measured"),
    TransductionLink("ratios->diet proportions (mixing model)", "Bayesian inversion; underdetermined if sources > isotopes+1",
                     fidelity=0.6, grade="estimated",
                     alias_states=["many diet mixtures produce identical isotope signature"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "IRMS calibrated vs. IAEA reference materials"},
    {"level": "working_standard", "status": "ok", "note": "lab reference materials run each batch"},
    {"level": "reference_standard", "status": "ok", "note": "IAEA standards anchor VPDB/Air scales"},
    {"level": "SI", "status": "ok", "note": "isotope delta scales are conventionally SI-anchored"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")
print("  NOTE: traceability covers the RATIO measurement only — not the diet inference.")

blind = BlindnessMap(spots=[
    BlindSpot("alias_state", "Many distinct diet mixtures yield identical isotope ratios",
              "mixing models return a posterior over diets, not 'the diet' — often reported as one"),
    BlindSpot("gate", "Unsampled food sources are excluded from the mixing model a priori",
              "the true diet component is invisible if nobody isotopically characterized it"),
    BlindSpot("null_state", "Tissue integrates only the assimilation window — no memory beyond turnover",
              "seasonal diet shifts vanish depending on tissue choice"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable: {blind.absence_interpretable()}")

sim = inject_and_recover(true_value=0.4, chain_fidelity=rep["chain_fidelity"],
                         noise=0.02, model_bias=0.05, tol=0.5)
print(f"PHASE 6: injected diet proportion 0.40, recovered {sim.recovered} "
      f"-> {'passes only at loose tolerance' if sim.passed else 'fails'}")

aspects = [
    {"aspect": "IRMS ratio measurement", "grade": "measured"},
    {"aspect": "sample preparation effects", "grade": "estimated"},
    {"aspect": "trophic discrimination factors", "grade": "assumed"},
    {"aspect": "mixing model identifiability", "grade": "estimated"},
    {"aspect": "source endmember completeness", "grade": "assumed"},
    {"aspect": "tissue integration window", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {"investigation_id": "inv-isotope-diet-001", "instrument": "IRMS + isotopic mixing model",
          "domain": "biology",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade(),
                            "scope_note": "traceability covers ratio measurement, not diet inference"},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "isotope-diet.instrument.json"), "w"), indent=2)
print("record written to outputs/isotope-diet.instrument.json")
