"""run_12: attribution_directionality on the four second-hand seed cases (a-d),
known-answer planted cases, null harness, and the coincidence card on the shared
shape. stdlib only. Work order 2026-11-10 (cross-model audit follow-up), item 2.

    python3 runs/run_12.py     # reproduces samples/run_12.sample.txt
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ledger.toolkit import attribution_directionality as ad
from ledger.toolkit import coincidence_card as cc

print("== known-answer planted cases (record, expected, got)")
for rid, expect, got in ad.known_answers():
    print(f"  {rid:24s} expect {str(expect):5s} got {str(got):5s} {'ok' if expect == got else 'MISMATCH'}")
print("== null harness, seeds 0-2")
for s in (0, 1, 2):
    print("  ", ad.null_harness(seed=s))
print("== seed cases (second hand: chat-side read, 2026-11-10)")
res = ad.read(ad.load_cases())
for row in res["rows"]:
    print(f"  {row['id']:26s} first {row['first']:12s} {row['fits']:12s} detector {str(row['detector']):5s} {row['flags']}")
print("  directionality:", res["directionality"])
in_scope = [r for r in res["rows"] if r["fits"] == "IN_SCOPE"]
shape = [r["id"] for r in in_scope if "FILLS_OPEN_SLOT" in r["flags"]]
print(f"  in scope {len(in_scope)} of {res['n']}; FILLS_OPEN_SLOT on {len(shape)} of {len(in_scope)} in scope (coder-entered field)")
missed = [r["id"] for r in in_scope if "FILLS_OPEN_SLOT" in r["flags"] and not r["detector"]]
print("  shape present, detector silent:", missed)
print("== coincidence card on the shared shape")
card = cc.load_all()["CC_004_open_slot_filled_across_families"]
print("  ", cc.read(card), "exits", cc.exits(card))
