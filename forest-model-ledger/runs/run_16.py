"""run_16: support_match on the first-hand attribution cases a-d (work order 2026-11-11, tool #3).

    python3 runs/run_16.py     # stdlib only; reproduces samples/run_16.sample.txt

Before: attribution_directionality's detector (assigns_without_support) on the same
records, unchanged since run_13. After: support_match's detector (unsupported_assignment),
which reads from the sha-pinned texts whether the cited basis supports the attribution.
Both detectors are reported side by side; neither replaces the other.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ledger.toolkit import attribution_directionality as ad
from ledger.toolkit import support_match as sm
from ledger.toolkit import gate as G

first = ad.load_cases(ad.CASES_FIRST)
before = {r["id"]: r for r in ad.read(first)["rows"]}
after = {r["id"]: r for r in sm.read_cases(first)}
g = sm.gate()
print("support_match gate:", G.summary(g))
print(f"paraphrase_recall (credit to the addressee without a listed word): {g['paraphrase_recall']:.3f}  -- not in the gate's TP")
print(f"\n{'case':26s} {'fits':12s} {'before: assigns_without_support':32s} after: support_match")
for r in first:
    b, a = before[r["id"]], after[r["id"]]
    print(f"{r['id']:26s} {r['fits_question']:12s} {str(b['detector']):32s} {a['verdict']:18s} fires {a['fires']}")
hb = [i for i, b in before.items() if b["detector"]]
ha = [i for i, a in after.items() if a["fires"]]
shape = [r["id"] for r in first if r["open_slot_filled"] == "YES" and r["fits_question"] == "IN_SCOPE"]
print(f"\ndetector hits before: {len(hb)} {hb}")
print(f"detector hits after:  {len(ha)} {ha}")
print(f"records carrying the shape (open_slot_filled YES, in scope; coder-entered): {shape}")
print(f"shape present, after-detector silent: {[i for i in shape if i not in ha]}")
print(f"after-detector fires, shape absent:   {[i for i in ha if i not in shape]}")
