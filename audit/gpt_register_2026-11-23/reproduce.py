# SPDX-License-Identifier: CC0-1.0
"""reproduce.py: recompute the R01-R04 numbers of REPRODUCTION.md. Read-only.

    python3 -B audit/gpt_register_2026-11-23/reproduce.py

Imports the validator and the case checker as they are; writes no file and
edits nothing. Stdlib only. ASCII only. Co-authored (JinnZ2 + Claude).
"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INST = os.path.join(ROOT, "blind-reader-void12", "studies", "instrument")
FLB = os.path.join(ROOT, "frame-location-benchmark")
sys.path.insert(0, INST)
sys.path.insert(0, FLB)
import validate as V  # noqa: E402
import validate_cases as VC  # noqa: E402

READINGS = ("a1_defined", "presence", "applicability")


def git(*a):
    return subprocess.run(("git", "-C", ROOT) + a, capture_output=True, text=True).stdout.strip()


def r01():
    recs = json.load(open(os.path.join(os.path.dirname(INST), "m01_records.json"), encoding="utf-8"))
    readers = sorted({x["reader_id"] for x in recs})
    print("R01 records %d readers %d" % (len(recs), len(readers)))
    print("R01 structural %d" % len(V.m01_structural_errors(recs)))
    listed = [x for x in recs if x["reader"]["listed"] == "LISTED"]
    for rd in READINGS:
        bad = [x for x in listed if not (V.tag_by(x, rd) == "YES" and V.independence_of(x) == "YES")]
        assert len(bad) == len(V.gpt_rule_errors(recs, rd))
        per = ", ".join("%s %d of %d" % (r, sum(1 for x in bad if x["reader_id"] == r),
                                         sum(1 for x in listed if x["reader_id"] == r)) for r in readers)
        print("R01 rule_on %-13s rejected %d of %d listed (%s)" % (rd, len(bad), len(listed), per))
    print("R01 per field (term field | readers listing | rejected under a1_defined / presence / applicability)")
    fields = {}
    for x in listed:
        fields.setdefault((x["term_id"], x["field"]), []).append(x)
    for (t, f), xs in sorted(fields.items()):
        rej = ["%d" % sum(1 for x in xs if not (V.tag_by(x, rd) == "YES" and V.independence_of(x) == "YES"))
               for rd in READINGS]
        if any(r != "0" for r in rej):
            print("  %-4s %-27s | %d | %s" % (t, f, len(xs), " / ".join(rej)))
    for arm in ("rule_off", "rule_on"):
        p = subprocess.run([sys.executable, "-B", os.path.join(INST, "validate.py"), "--arm=" + arm, "m01",
                            os.path.join(os.path.dirname(INST), "m01_records.json")], capture_output=True, text=True)
        print("R01 validate.py --arm=%s exit %d : %s" % (arm, p.returncode, p.stdout.splitlines()[0]))
    p = subprocess.run([sys.executable, "-B", os.path.join(INST, "arms.py"), "--check"], capture_output=True, text=True)
    print("R01 arms.py --check exit %d : %s" % (p.returncode, p.stdout.strip()))


def r02():
    recs = json.load(open(os.path.join(os.path.dirname(INST), "m01_records.json"), encoding="utf-8"))
    for x in recs:
        if x["term_id"] == "T02" and x["field"] == "value":
            s = x["source"]
            print("R02 %s origin %s scopes %s/%s/%s | TAG a1 %s presence %s applicability %s | INDEPENDENCE %s | "
                  "reader %s | key_a1 %s" % (x["reader_id"], s["origin"], s["presence_scope"], s["applicability_scope"],
                                             s["requirement_scope"], V.tag_by(x, "a1_defined"), V.tag_by(x, "presence"),
                                             V.tag_by(x, "applicability"), V.independence_of(x), x["reader"]["listed"],
                                             x["key_a1"]["listed"]))


def r03_r04():
    for f in ("harness/arm1_format.txt", "harness/arm2_positions.txt", "harness/arm3_corrections.txt",
              "harness/arm4_full.txt", "cases.jsonl", "FREEZE_LOG.md"):
        print("R03 %-30s commits %s" % (f, git("log", "--format=%h", "--", "frame-location-benchmark/" + f).split()))
    H = VC.load_harness(os.path.join(FLB, "harness"))
    print("R03 arm4 == arm2 ++ arm3 : %s" % (H["arm4_full.txt"] == H["arm2_positions.txt"] + H["arm3_corrections.txt"]))
    norm = lambda s: " ".join((s or "").lower().split())
    for label, text in (("HEAD", open(os.path.join(FLB, "cases.jsonl"), encoding="utf-8").read()),
                        ("a70eb40", git("show", "a70eb40:frame-location-benchmark/cases.jsonl"))):
        cases = [json.loads(l) for l in text.splitlines() if l.strip()]
        p = sum(1 for c in cases for h in H.values() if norm(c["prompt"]) in norm(h))
        t = sum(1 for c in cases if c.get("fault_target") for h in H.values() if norm(c["fault_target"]) in norm(h))
        print("R03 cases at %-7s : %d cases, %d with fault_target ; prompt in harness %d ; fault_target in harness %d"
              % (label, len(cases), sum(1 for c in cases if c.get("fault_target")), p, t))
    ok, msgs = VC.validate(os.path.join(FLB, "cases.jsonl"), os.path.join(FLB, "harness"))
    print("R04 validate_cases.validate : ok %s, %d message(s)" % (ok, len(msgs)))
    p = subprocess.run([sys.executable, "-B", "validate_cases.py"], cwd=FLB, capture_output=True, text=True)
    print("R04 validate_cases.py exit %d : %s" % (p.returncode, p.stdout.strip()))
    p = subprocess.run([sys.executable, "-B", "selftest_flb.py"], cwd=FLB, capture_output=True, text=True)
    print("R04 selftest_flb.py exit %d : %s" % (p.returncode, p.stdout.strip().splitlines()[-1]))


if __name__ == "__main__":
    r01()
    r02()
    r03_r04()
