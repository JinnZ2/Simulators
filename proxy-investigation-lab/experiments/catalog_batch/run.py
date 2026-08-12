"""Batch investigation: grade the entire MSIAF proxy catalog and rank by
groundedness. Writes outputs/catalog-coverage-report.md."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from proxy_lab.catalog import CATALOG
from proxy_lab.batch import run_batch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

results = run_batch(CATALOG)
lines = ["# MSIAF Proxy Catalog — Comparative Grounding Report", "",
         "Prior grading of all cataloged proxies through the lab protocol.",
         "Sorted by grounded fraction (how much of the chain is measured vs assumed).", "",
         "| Rank | Proxy | Mode | Chain fidelity | Grounded | Weakest link | Verdict |",
         "|---|---|---|---|---|---|---|"]
for i, r in enumerate(results, 1):
    lines.append(f"| {i} | {r['id']} | {r['mode']} | {r['chain_fidelity']:.3f} | "
                 f"{r['grounded_fraction']:.2f} | {r['weakest_link']} | {r['verdict']} |")
lines += ["", "## Reading the table", "",
          "- **Chain fidelity** is multiplicative across the causal chain — a proxy with one",
          "  assumed 0.55 link cannot exceed it, no matter how good the sensor is.",
          "- **Grounded fraction** weights measured=1.0, estimated=0.5, assumed=0.0 per link.",
          "- Bottom-of-table proxies are where investigation effort pays off most:",
          "  they are *used* in MSIAF reasoning but rest on assumed links.", "",
          "## Priority queue for full investigations", ""]
for r in results[-5:]:
    lines.append(f"1. **{r['id']}** (grounded {r['grounded_fraction']:.2f}) — weakest: {r['weakest_link']}")
open(os.path.join(OUT, "catalog-coverage-report.md"), "w").write("\n".join(lines))
print("\n".join(lines[:22]))
print(f"\n... full report written to {OUT}/catalog-coverage-report.md")
