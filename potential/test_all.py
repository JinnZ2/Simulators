"""test_all.py — known-answer tests for the three modules.

Run: python3 test_all.py
Every module prints its own count; this file prints the total.
"""

import json
import tempfile
from pathlib import Path

from transformation import Entry, MECHANISMS, SHAPE_PAIRS, DEFAULT_DIRECTION
from ledger import Ledger
from baseline import Hit, SIGNATURES, scan_candidates, check_no_composite
import baseline as baseline_mod
import ledger as ledger_mod
import transformation as transformation_mod

CHECKS = 0
def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)

# transformation.py

def test_mechanism_vocab():
    check(len(MECHANISMS) == 10, f"expected 10 mechanisms, got {len(MECHANISMS)}")
    check(len(set(MECHANISMS)) == 10, "mechanisms not unique")
    check(len(SHAPE_PAIRS) == 8, f"expected 8 shape-pairs, got {len(SHAPE_PAIRS)}")
    check(len(set(SHAPE_PAIRS)) == 8, "shape-pairs not unique")
    # every default direction is a declared pair
    for m, dirs in DEFAULT_DIRECTION.items():
        for d in dirs:
            check(d in SHAPE_PAIRS, f"default direction {d} not in SHAPE_PAIRS")

def test_entry_validates():
    # happy path
    e = Entry("SUBSTITUTE", "unresolved", "familiar", reader="audit", date="2026-09-28")
    check(e.direction_str == "unresolved -> familiar", "direction_str wrong")
    # unknown mechanism refused
    try:
        Entry("FROBNICATE", "unresolved", "familiar")
        check(False, "should have refused unknown mechanism")
    except ValueError:
        check(True, "refused unknown mechanism")
    # unknown shape-pair refused
    try:
        Entry("DELETE", "cats", "dogs")
        check(False, "should have refused unknown shape-pair")
    except ValueError:
        check(True, "refused unknown shape-pair")

def test_entry_roundtrip():
    e = Entry("TERMINATE", "recursive", "terminal",
              source_span=(10, 20), target_span=(5, 12),
              reader="r1", date="2026-09-28")
    d = e.to_dict()
    e2 = Entry.from_dict(d)
    check(e2.source_span == (10, 20), "source_span roundtrip failed")
    check(e2.target_span == (5, 12), "target_span roundtrip failed")
    check(e2.mechanism == "TERMINATE", "mechanism roundtrip failed")

# ledger.py

def test_ledger_add_and_summary():
    L = Ledger()
    L.add(Entry("SUBSTITUTE", "unresolved", "familiar", reader="r1"))
    L.add(Entry("SUBSTITUTE", "unresolved", "familiar", reader="r1"))
    L.add(Entry("TERMINATE", "recursive", "terminal", reader="r2"))
    s = L.summary()
    check(s["n_entries"] == 3, "wrong entry count")
    check(s["n_readers"] == 2, "wrong reader count")
    check(s["mechanisms_seen"] == 2, "wrong mechanism count")
    check(s["directions_seen"] == 2, "wrong direction count")
    check(s["triples_seen"] == 2, "wrong triple count")
    check(s["triples_possible"] == 80, "wrong triples_possible")

def test_ledger_refuses_composite():
    L = Ledger()
    try:
        L.composite()
        check(False, "composite should have raised")
    except NotImplementedError:
        check(True, "composite refused")

def test_ledger_save_load():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "led.jsonl"
        L = Ledger()
        L.add(Entry("COMPLETE", "unfinished", "polished", reader="r1"))
        L.add(Entry("MERGE", "distinct", "merged", reader="r2"))
        L.save(p)
        L2 = Ledger().load(p)
        check(len(L2.entries) == 2, "save/load lost entries")
        check(L2.entries[0].mechanism == "COMPLETE", "first entry wrong")
        check(L2.entries[1].source_type == "distinct", "second entry wrong")

def test_ledger_load_bad_line():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "bad.jsonl"
        p.write_text(json.dumps({
            "mechanism": "NOT_A_MECHANISM",
            "source_type": "unresolved",
            "target_type": "familiar",
        }) + "\n")
        try:
            Ledger().load(p)
            check(False, "should have refused bad mechanism on load")
        except ValueError as e:
            check("NOT_A_MECHANISM" in str(e), "wrong error message")

# baseline.py

def test_hit_validates():
    h = Hit("CLOSURE_BEFORE_CHAIN", (0, 10), (0, 5),
            reader="audit", reason="chain not traced")
    check(h.signature in SIGNATURES, "signature not in vocab")
    try:
        Hit("CLOSURE_BEFORE_CHAIN", (0, 10), (0, 5), reader="audit", reason="")
        check(False, "should refuse empty reason")
    except ValueError:
        check(True, "refused empty reason")
    try:
        Hit("CLOSURE_BEFORE_CHAIN", (0, 10), (0, 5), reader="", reason="x")
        check(False, "should refuse empty reader")
    except ValueError:
        check(True, "refused empty reader")
    try:
        Hit("NOT_A_SIGNATURE", (0, 10), (0, 5), reader="r", reason="x")
        check(False, "should refuse unknown signature")
    except ValueError:
        check(True, "refused unknown signature")

def test_scanner_is_candidate_only():
    # The scanner returns candidates with a suggested signature but no hit.
    hits = scan_candidates("The answer should be this because it is right.")
    check(len(hits) >= 3, f"expected >=3 candidates, got {len(hits)}")
    # Every candidate carries a string signature suggestion and offsets.
    for sig, term, a, b in hits:
        check(sig in SIGNATURES, f"candidate suggested unknown sig {sig}")
        check(a < b, "offset range invalid")

def test_no_composite_on_module_source():
    src = Path(ledger_mod.__file__).read_text()
    check(check_no_composite(src),
          "ledger.py must not combine mechanism and direction counts")

def test_no_composite_catches_plant():
    bad = """
x = by_mechanism() + by_direction()
"""
    try:
        check_no_composite(bad)
        check(False, "should have caught composite")
    except AssertionError:
        check(True, "caught planted composite")

# main

def main():
    tests = [
        test_mechanism_vocab,
        test_entry_validates,
        test_entry_roundtrip,
        test_ledger_add_and_summary,
        test_ledger_refuses_composite,
        test_ledger_save_load,
        test_ledger_load_bad_line,
        test_hit_validates,
        test_scanner_is_candidate_only,
        test_no_composite_on_module_source,
        test_no_composite_catches_plant,
    ]
    for t in tests:
        t()
    print(f"checks: {CHECKS}")
    print(f"tests:  {len(tests)}")
    print("PASS")

if __name__ == "__main__":
    main()
