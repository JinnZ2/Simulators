#!/usr/bin/env python3
"""check_v02.py -- confirm ICSC v0.2 landed verbatim and that the repo parts it cites resolve. CC0, stdlib.

Checks only what the delivered text says about this tree: its own sha256, that v0.1 is untouched
(via check_landing.py), that each section-13 tool path exists with one content marker, and that
the two live specimens it cites still read as cited. Nothing in the spec is run or built.

python3 ICSC/check_v02.py      prints checks: N failed: M
"""
import hashlib, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SIB = os.path.dirname(ROOT)
SHA = "5773584923e1f1f0fda7e2c687f5135a1497e37f406fe9b84284244e8f68791e"
ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)
spec_all = open(os.path.join(HERE, "SPEC_v0.2.md"), "rb").read()
REV_MARK = b"\n---\n\n## rev 2026-11-09 11:44\n"
REV_SHA = "8090a066c5a4fda84fe6d29ebaa232afeac60b332c67a8b8fc076b716fa8f43b"
cut = spec_all.find(REV_MARK)
spec = spec_all[:cut] if cut >= 0 else spec_all
check(hashlib.sha256(spec).hexdigest() == SHA, "SPEC_v0.2.md original landing (above the rev heading) matches its sha256")
# rev 2026-11-09 11:44: appended verbatim; the delivered text starts at its own title line
check(cut >= 0, "rev 2026-11-09 11:44 heading present")
rev = spec_all[spec_all.find(b"# ICSC v0.2", cut):] if cut >= 0 else b""
check(hashlib.sha256(rev).hexdigest() == REV_SHA, "rev 2026-11-09 11:44 text matches its sha256")
rt = rev.decode("utf-8")
check("CONDITIONAL(circular_control)" in rt and "same_author" not in rt, "rev: G1 / T30 read circular_control, no same_author")
check("T30b unregistered assumption" in rt and "UNREGISTERED_ASSUMPTION_CANDIDATE" in rt, "rev: T30b present")
check("never `COMPLETE`" in rt, "rev: assumption coverage is never COMPLETE")
import difflib
ops = [o for o in difflib.SequenceMatcher(None, spec.decode("utf-8").splitlines(), rt.splitlines(),
                                          autojunk=False).get_opcodes() if o[0] != "equal"]
check(len(ops) == 3, "rev: differs from the original in exactly three regions (sections 2, 4.1, 12); found %d" % len(ops))
r = subprocess.run([sys.executable, os.path.join(HERE, "check_landing.py")], capture_output=True, text=True)
check(r.returncode == 0, "v0.1 landing unchanged (check_landing.py exit 0)")
# section 13: path -> marker the fit column relies on; a missing sibling checkout reads NOT_RUN
G5 = [(os.path.join(ROOT, "null-harness"), "CONSTANT_FIRES"),
      (os.path.join(ROOT, "cutoff-attribution"), "UNRESOLVED"),
      (os.path.join(ROOT, "operator-machine-coupling"), "r_ij"),
      (os.path.join(ROOT, "model-provenance"), "STALE_TABLE"),
      (os.path.join(SIB, "cross-domain-toolkit", "falsification_ledger"), "verify"),
      (os.path.join(SIB, "cross-domain-toolkit", "multi_substrate_calibration"), "correlation_group")]
def has(d, m):
    for dp, _, fs in os.walk(d):
        for f in fs:
            if f.endswith((".py", ".md")) and m in open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read():
                return True
    return False
for d, m in G5:
    if not os.path.isdir(d):
        print("NOT_RUN: sibling checkout absent:", d); continue
    check(has(d, m), "section 13 %s carries %r" % (os.path.relpath(d, SIB), m))
# section 3 live specimen: MP_010 STALE_TABLE in the claim table
check("MP_010" in open(os.path.join(ROOT, "model-provenance", "CLAIM_TABLE.md"), encoding="utf-8").read(),
      "section 3 specimen: model-provenance MP_010 present")
# section 4.1 / T29 specimen: null_calibration totals as cited
n = subprocess.run([sys.executable, os.path.join(ROOT, "cutoff-attribution", "null_calibration.py")],
                   capture_output=True, text=True).stdout
check("total                                 1800             300    2400" in n,
      "T29 specimen: three-outcome total 1800 / 300 / 2400 WRONG")
check("abstain_status_ESTIMATED 300" in n, "T29 specimen: WRONG rows are abstain_status_ESTIMATED")
# LIVE_SPECIMENS.md item 3: self-firing scanner, fixed + planted case
lac = os.path.join(ROOT, "law-audit-card")
check("Self-firing scanner" in open(os.path.join(HERE, "LIVE_SPECIMENS.md"), encoding="utf-8").read(),
      "LIVE_SPECIMENS.md carries the self-firing scanner case")
probe = ("import sys; sys.path.insert(0, %r); import card, io\n"
         "src = io.open(card.__file__, encoding='utf-8').read()\n"
         "print(card.tool_writes_no_disposition(), card.tool_writes_no_disposition(src + '\\nX = {\"value\": \"RETIRE\"}\\n'))") % lac
r = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
check(r.stdout.strip() == "[] ['RETIRE']", "specimen 3: fixed scanner silent on its own source, fires on a planted RETIRE")
check("test_tool_writes_no_disposition" in open(os.path.join(lac, "tests", "test_card.py"), encoding="utf-8").read(),
      "specimen 3: planted test present in law-audit-card/tests/test_card.py")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
