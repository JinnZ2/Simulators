#!/usr/bin/env python3
"""Checks for citations.py (OSC-WO4). Stdlib only."""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import citations as c  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


ids = [r["id"] for r in c.ROWS]
ok("row ids unique", len(ids) == len(set(ids)))
ok("every row has claim and note", all(r["claim"] and r["note"] for r in c.ROWS))
ok("states come from the imported rule", c.citation_state.__module__ == "_check_citations")
st = {r["id"]: c.state(r) for r in c.ROWS}
ok("C02 depinning precedent is NOT_FOUND (two empty searches)", st["C02"] == "NOT_FOUND")
ok("C10 0.3 T with one empty search is UNREACHABLE, not NOT_FOUND", st["C10"] == "UNREACHABLE")
ok("C04 7.6 uJ/cm2 value is UNREACHABLE", st["C04"] == "UNREACHABLE")
ok("C06 120 aJ is UNREACHABLE while C05 6 J/cm3 is VERIFIED",
   st["C06"] == "UNREACHABLE" and st["C05"] == "VERIFIED")
ok("C01 anchor paper VERIFIED", st["C01"] == "VERIFIED")
cnt = c.counts()
ok("counts sum to rows", sum(cnt.values()) == len(c.ROWS))
ok("no row is CORRECTED without a located differing value",
   all(c.state(r) != "CORRECTED" or r["says"] == "DIFFERS" for r in c.ROWS))
# no state field is declared in the data: the state is derived only
tree = ast.parse((HERE / "citations.py").read_text(encoding="utf-8"))
keys = {k.value for n in ast.walk(tree) if isinstance(n, ast.Dict)
        for k in n.keys if isinstance(k, ast.Constant)}
ok("no 'state' key declared in any row", "state" not in keys)
src = (HERE / "citations.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)

failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
