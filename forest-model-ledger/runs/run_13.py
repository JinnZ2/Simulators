"""run_13: attribution_directionality on the FIRST-HAND seed records (texts supplied
by the operator 2026-11-10, pinned in ledger/toolkit/cases/texts/), diffed against
the second-hand records of run_12, which are kept unchanged. stdlib only.

    python3 runs/run_13.py     # reproduces samples/run_13.sample.txt
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ledger.toolkit import attribution_directionality as ad
from ledger.toolkit import coincidence_card as cc

second = ad.load_cases()
first = ad.load_cases(ad.CASES_FIRST)
print("== locators (first hand): quotes checked on their lines in sha-pinned texts")
for r in first:
    print(f"  {r['id']:26s} {ad.check_locators(r)} locators resolve")
print("== null harness (unchanged tool), seed 0:", ad.null_harness(seed=0)["verdict"])
res = ad.read(first)
print("== first-hand records")
for row in res["rows"]:
    print(f"  {row['id']:26s} first {row['first']:12s} {row['fits']:12s} detector {str(row['detector']):5s} {row['flags']}")
print("  directionality:", res["directionality"])
in_scope = [r for r in res["rows"] if r["fits"] == "IN_SCOPE"]
shape = [r["id"] for r in in_scope if "FILLS_OPEN_SLOT" in r["flags"]]
print(f"  in scope {len(in_scope)} of {res['n']}; FILLS_OPEN_SLOT on {len(shape)} of {len(in_scope)} in scope")
print("  shape present, detector silent:", [r["id"] for r in in_scope if "FILLS_OPEN_SLOT" in r["flags"] and not r["detector"]])
print("== second hand -> first hand, per case (both kept)")
for d in ad.diff_hands(second, first):
    ch = d["changed"]
    print(f"  {d['id']:26s} detector {d['detector'][0]!s:5s} -> {d['detector'][1]!s:5s}  fields changed {len(ch)}")
    for f, (a, b) in ch.items():
        print(f"      {f}: {a!r} -> {b!r}")
print("== cards")
for cid in ("CC_004_open_slot_filled_across_families", "CC_005_open_slot_filled_first_hand"):
    card = cc.load_all()[cid]
    print(f"  {cid}:", cc.read(card), "exits", cc.exits(card))
