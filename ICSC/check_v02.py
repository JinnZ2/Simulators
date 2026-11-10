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
spec = open(os.path.join(HERE, "SPEC_v0.2.md"), "rb").read()
check(hashlib.sha256(spec).hexdigest() == SHA, "SPEC_v0.2.md bytes match the landed sha256")
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
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
