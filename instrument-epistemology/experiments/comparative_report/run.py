"""Cross-instrument comparative report — what separates the instruments that
know from the instruments that estimate."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
files = ["seismometer.instrument.json", "satellite-sst.instrument.json",
         "lidar-biomass.instrument.json", "camera-trap-density.instrument.json",
         "isotope-diet.instrument.json", "edna-biodiversity.instrument.json"]
recs = []
for f in files:
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        recs.append(json.load(open(p)))

rows = []
for r in recs:
    rows.append({
        "instrument": r["instrument"], "domain": r["domain"],
        "rung": r["model_rung"],
        "chain_fidelity": r["transduction_chain"]["chain_fidelity"],
        "traceability": r["traceability"]["grade"],
        "blind_spots": len(r["blindness_map"]),
        "grounded": r["coverage"]["grounded_fraction"],
        "verdict": r["coverage"]["verdict"],
    })
rows.sort(key=lambda r: r["grounded"], reverse=True)

lines = ["# Cross-Instrument Comparative Report", "",
         "Six instruments, one question each: how does it know what it claims to know?", "",
         "| Instrument | Domain | Rung | Chain fidelity | Traceability | Blind spots | Grounded | Verdict |",
         "|---|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['instrument']} | {r['domain']} | {r['rung']} | {r['chain_fidelity']:.3f} | "
                 f"{r['traceability']} | {r['blind_spots']} | {r['grounded']:.2f} | {r['verdict']} |")
lines += ["", "## What separates the top from the bottom", "",
          "1. **It is not the hardware.** The eDNA sequencer and the IRMS are as precisely built as",
          "   the seismometer's digitizer. The difference is everything around the hardware:",
          "   transduction chain, bridge model, reference standards, blindness map.",
          "2. **Traceability is the strongest lever.** Both SI-traceable instruments (seismometer,",
          "   SST radiometer via buoy network) sit at the top. Every instrument without a primary",
          "   standard or reference population caps at 'estimated' no matter how good the sensor.",
          "3. **Model rung predicts groundedness.** M1 (calibrated reading) > M2 (model-derived) >",
          "   M3 (inverted). The reported quantity's rung is the single best predictor of how much",
          "   of the 'measurement' is actually a model output.",
          "4. **Every instrument has blind spots — the difference is whether they're mapped.**",
          "   Even the seismometer has three (magnitude-completeness gate, station geometry frame,",
          "   site-amplification alias). Well-grounded instruments know what they can't see.",
          "5. **Forward simulation separates honest pipelines from lucky ones.** The naive",
          "   seismometer pipeline fails; the response-deconvolved one recovers truth exactly.",
          "   The ecology instruments fail at their *bridge model* stage, not their sensors.", "",
          "## The pattern", "",
          "Physics instruments know more not because nature is simpler there, but because",
          "decades were spent building *standards, traceability chains, and response models*.",
          "Ecological and biological instruments are at the M2 frontier: their instruments are",
          "already excellent; what is missing is the institutional layer — reference standards,",
          "inter-lab comparisons, and published blindness maps."]
report = "\n".join(lines)
open(os.path.join(OUT, "cross-instrument-report.md"), "w").write(report)
print(report[:1800])
