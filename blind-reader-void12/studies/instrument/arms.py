"""arms.py: two analyses on m01_records.json, neither choosing an answer.

  python3 arms.py          writes arms_report.txt beside this file and prints it
  python3 arms.py --check  fails if arms_report.txt would change

1. The GPT-6 proposal's validator rule as an arm: rule_off (the instrument as adopted: structural checks only) and rule_on
   (a LISTED field must have TAG = YES and INDEPENDENCE = YES). Under rule_on, TAG is evaluated under BOTH readings below.
2. TAG under two readings, on every record (key a1's own reading is shown beside them): presence (the key is on every instance of the term and on no other: key a1's
   reading) and applicability (it is populated on every instance of the term and on no other). Per-record divergence list.

This lives here, not in scoring/score_v2.py, because score_v2.py is hash-pinned in PREREG (amendment 1); the scorer is not
changed. TAG / INDEPENDENCE are read off the source half of each record (see validate.tag_by, validate.independence_of);
the source half is SCRIPT_DERIVED or CODER_INFERRED as marked on each record.
"""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as V  # noqa: E402
RECS = os.path.join(os.path.dirname(HERE), "m01_records.json")
SHORT = {"2026-11-18_claude-v2-A": "claude", "2026-11-19_kimi-v2-A": "kimi", "2026-11-19_gpt6-v2": "gpt6"}

def report():
    recs = json.load(open(RECS, encoding="utf-8"))
    readers = sorted({x["reader_id"] for x in recs}, key=list(SHORT).index)
    L = ["arms.py on studies/m01_records.json (%d records, %d readers, condition D0)" % (len(recs), len(readers)), ""]
    # 1. arms
    off = V.m01_errors(recs, "rule_off")
    L += ["1. validator arms", "",
          "   rule_off (as adopted)                  structural errors: %d" % len(off)]
    for reading in ("a1_defined", "presence", "applicability"):
        on = V.m01_structural_errors(recs) + V.gpt_rule_errors(recs, reading)
        per = {r: sum(1 for e in on if (" %s " % r) in e) for r in readers}
        listed = {r: sum(1 for x in recs if x["reader_id"] == r and x["reader"]["listed"] == "LISTED") for r in readers}
        L.append("   rule_on, TAG read by %-13s       records rejected: %d   (%s)" % (
            reading, len(on), ", ".join("%s %d of %d listed" % (SHORT[r], per[r], listed[r]) for r in readers)))
    # self-check: does rule_on under key a1's own TAG reproduce key a1's specific lists?
    mism = sorted({(x["term_id"], x["field"]) for x in recs if x["key_a1"]["listed"] != "KEY_UNDETERMINED"
                   and (x["key_a1"]["listed"] == "LISTED") != (V.tag_by(x, "a1_defined") == "YES" and V.independence_of(x) == "YES")})
    L += ["", "   self-check: TAG = a1_defined and INDEPENDENCE reproduce key a1 on the catalog fields: %s" % (
          "yes, all" if not mism else "NO, %d field(s) differ: %s" % (len(mism), ", ".join("%s %s" % m for m in mism)))]
    L += ["", "   rule_on rejections by field (TAG by a1_defined / presence / applicability):", ""]
    pres = set(V.gpt_rule_errors(recs, "presence")); appl = set(V.gpt_rule_errors(recs, "applicability"))
    fields = {}
    for x in recs:
        if x["reader"]["listed"] != "LISTED": continue
        k = (x["term_id"], x["field"])
        f = fields.setdefault(k, {"readers": [], "d": V.tag_by(x, "a1_defined"), "p": V.tag_by(x, "presence"), "a": V.tag_by(x, "applicability"), "i": V.independence_of(x)})
        f["readers"].append(SHORT[x["reader_id"]])
    for (t, fld), f in sorted(fields.items()):
        rej = [n for n, k in (("a1_defined", "d"), ("presence", "p"), ("applicability", "a")) if not (f[k] == "YES" and f["i"] == "YES")]
        if rej:
            L.append("   %-4s %-27s by %-17s TAG d=%-3s p=%-3s a=%-3s IND=%-3s rejected under: %s" % (
                t, fld, ",".join(f["readers"]), f["d"][:3], f["p"][:3], f["a"][:3], f["i"][:3], ", ".join(rej) if len(rej) < 3 else "all three"))
    # 2. two readings of TAG
    L += ["", "2. TAG under two readings, every record", ""]
    div = [x for x in recs if V.tag_by(x, "presence") != V.tag_by(x, "applicability")]
    L.append("   records: %d ; divergent: %d ; agree: %d" % (len(recs), len(div), len(recs) - len(div)))
    L += ["", "   divergent records (reader, term, field: presence -> applicability ; a1_defined ; reader listed ; key a1):", ""]
    for x in div:
        L.append("   %-6s %-4s %-27s %-10s -> %-10s  a1 %-4s %-10s key a1 %s%s" % (
            SHORT[x["reader_id"]], x["term_id"], x["field"], V.tag_by(x, "presence"), V.tag_by(x, "applicability"), V.tag_by(x, "a1_defined"),
            x["reader"]["listed"], x["key_a1"]["listed"], "  [coder]" if x["source"]["provenance"] == "CODER_INFERRED" else ""))
    fl = sorted({(x["term_id"], x["field"]) for x in div})
    L += ["", "   distinct fields divergent: %d (%s)" % (len(fl), ", ".join("%s %s" % k for k in fl)),
          "   (the readings are properties of the source, so each divergent field appears once per reader)", "",
          "Neither reading is chosen; which reading TAG uses is the owner's definition."]
    return "\n".join(L) + "\n"

def main():
    out = report(); p = os.path.join(HERE, "arms_report.txt")
    if "--check" in sys.argv:
        same = os.path.exists(p) and open(p, encoding="utf-8").read() == out
        print("arms --check: " + ("identical" if same else "WOULD CHANGE")); sys.exit(0 if same else 1)
    open(p, "w", encoding="utf-8").write(out); print(out)

if __name__ == "__main__":
    main()
