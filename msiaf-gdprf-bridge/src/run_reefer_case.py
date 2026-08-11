"""Run the reefer-trucking MSIAF case through the GDPRF engine.

Usage: python3 src/run_reefer_case.py
Outputs: outputs/reefer-investigation-report.md, outputs/reefer-provenance-ledger.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bridge import Investigation

here = os.path.dirname(__file__)
case = json.load(open(os.path.join(here, "..", "cases", "reefer-trucking.case.json")))
inv = Investigation(case)

print(f"CASE: {case['title']}\n" + "=" * 70)
for link in inv.case["links"]:
    r = inv.run_link(link)
    print(f"[{r['link_id']}] {r['pathway']:<40} posterior={r['posterior']:.3f} "
          f"(cascade f={r['cascade_fidelity']:.3f}, gate={r['gate']})")

agg = inv.aggregate()
print("=" * 70)
print(f"SYSTEMIC DETERMINATION")
print(f"  chain (conjunctive) confidence : {agg['confidence_gradient']:.3f}")
print(f"  weakest-link bound             : {agg['weakest_link_bound']:.3f}")
print(f"  bound divergence               : {agg['bound_divergence']:.3f} "
      f"({'RESIDUAL TRIGGER' if agg['hidden_variable_search']['triggered'] else 'within tolerance'})")
print(f"  max unknown-variable risk      : {agg['unknown_variable_risk_score']:.3f}")

dp = inv.decide(agg)
print(f"\nDECISION POINT: {dp.action.value.upper()}")
print(f"  {dp.rationale}")
print(f"\nProvenance ledger: {len(inv.ledger.records)} records, "
      f"chain valid: {inv.ledger.verify_chain()}")

os.makedirs(os.path.join(here, "..", "outputs"), exist_ok=True)
json.dump(json.loads(inv.ledger.to_json()),
          open(os.path.join(here, "..", "outputs", "reefer-provenance-ledger.json"), "w"), indent=2)

lines = ["# MSIAF x GDPRF Investigation Report — Reefer Run-Off-Road", "",
         f"**Case:** {case['title']}", "",
         "## Link Determinations", "",
         "| Link | Pathway | Posterior | Cascade fidelity | Gate |", "|---|---|---|---|---|"]
for r in inv.link_results:
    lines.append(f"| {r['link_id']} | {r['pathway']} | {r['posterior']:.3f} | "
                 f"{r['cascade_fidelity']:.3f} | {r['gate']} |")
lines += ["", "## Systemic Determination", "",
          f"- Chain (conjunctive) confidence: **{agg['confidence_gradient']:.3f}**",
          f"- Weakest-link bound: **{agg['weakest_link_bound']:.3f}**",
          f"- Bound divergence: {agg['bound_divergence']:.3f} "
          f"({'residual variance trigger fired' if agg['hidden_variable_search']['triggered'] else 'within tolerance'})",
          f"- Max unknown-variable risk: {agg['unknown_variable_risk_score']:.3f}", "",
          "## Decision Point", "",
          f"**{dp.action.value.upper()}** — {dp.rationale}", "",
          "## Human Translation Layer Output", ""]
# HTL narrative
weakest = min(inv.link_results, key=lambda r: r["posterior"])
lines.append(
    f"> The systemic determination — financial penalty structure (D4) driving dispatch "
    f"pressure (D2), degrading driver physiology (D1), meeting an uncommunicated "
    f"infrastructure hazard (D3) — is **supported at chain confidence "
    f"{agg['confidence_gradient']:.2f}** (weakest link: {weakest['pathway']} at "
    f"{weakest['posterior']:.2f}). The moment-of-incident reconstruction link "
    f"remains model-based and uncalibrated, and its identification gate failed: "
    f"the exact contribution of fatigue to the overcorrection is recorded as "
    f"**unexplained ignorance**, not asserted. Per the decision policy, this "
    f"determination is **{dp.action.value}**. {dp.rationale}.")
open(os.path.join(here, "..", "outputs", "reefer-investigation-report.md"), "w").write("\n".join(lines))
print("report + ledger written to outputs/")
