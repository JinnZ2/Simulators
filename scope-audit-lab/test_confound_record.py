#!/usr/bin/env python3
"""Checks for confound_record.py (SAL-WO2). Stdlib only."""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "lab_0_3"))
import confound_record as cr  # noqa: E402
from scope_audit_lab.core import validate_record  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


def raises(fn, *a, **kw):
    try:
        fn(*a, **kw)
    except cr.ConfoundRecordError:
        return True
    return False


stamp = cr.version_stamp("WITHHELD", reason="session rule: no model id in pushed artifacts",
                         date="2026-10-27")

# state rules
ok("UNTESTED with a result is refused", raises(cr.make, "C01", "x", "UNTESTED", result="y"))
ok("RAN_NO_SIGNAL without a test is refused", raises(cr.make, "C01", "x", "RAN_NO_SIGNAL", result="y", stamp=stamp))
ok("RAN_SIGNAL without a stamp is refused (confound 7)",
   raises(cr.make, "C01", "x", "RAN_SIGNAL", test_applied="t", result="r"))
ok("NOT_TESTABLE without a reason is refused", raises(cr.make, "C01", "x", "NOT_TESTABLE"))
ok("unknown status refused", raises(cr.make, "C01", "x", "CONFOUNDED"))
ok("STATED stamp without a model id refused", raises(cr.version_stamp, "STATED"))
ok("WITHHELD stamp without a reason refused", raises(cr.version_stamp, "WITHHELD"))
r_ok = cr.make("C06", "sampling variance", "RAN_NO_SIGNAL", test_applied="10 reruns at T=1",
               result="spread within stated band", stamp=stamp)
ok("a complete RAN record validates", cr.validate(r_ok) == [])

# seed and the lab encoding
seed = cr.seed_thread_b(["model_x"])
ok("ten thread-B confounds seeded", len(seed) == 10)
ok("all seeded UNTESTED", set(cr.current(seed).values()) == {"UNTESTED"})
ok("every native seed record validates", all(cr.validate(r) == [] for r in seed))
ok("native type is refused by the delivered lab (closed type list)",
   validate_record(seed[0]) != [])
labenc = [cr.to_lab_audit_event(r) for r in seed + [r_ok]]
ok("lab-encoded records pass the delivered lab's own validator",
   all(validate_record(x) == [] for x in labenc))
ok("lab encoding keeps verdict None", all(x["payload"]["verdict"] is None for x in labenc))

# append-only chain
first = cr.make("C06", "sampling variance", "UNTESTED", record_id="r1")
second = cr.make("C06", "sampling variance", "RAN_SIGNAL", test_applied="t", result="r",
                 stamp=stamp, supersedes="r1", record_id="r2")
ok("supersedes chain validates", cr.validate_stream([first, second]) == [])
ok("current takes the head of the chain", cr.current([first, second]) == {"C06": "RAN_SIGNAL"})
ok("forward reference refused", cr.validate_stream([second, first]) != [])
other = cr.make("C07", "version drift", "UNTESTED", supersedes="r1", record_id="r3")
ok("superseding another confound refused", cr.validate_stream([first, other]) != [])
ok("repeated id (edit in place) refused", cr.validate_stream([first, first]) != [])
c = cr.counts([first, second] + seed)
ok("counts are per state, sum to confounds", sum(c.values()) == len(cr.current([first, second] + seed)))

# no combined call anywhere
tree = ast.parse((HERE / "confound_record.py").read_text(encoding="utf-8"))
names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
ok("no function named like a combined verdict",
   not any(w in n for n in names for w in ("verdict", "is_confounded", "clean", "score")))
src = (HERE / "confound_record.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)

failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
