#!/usr/bin/env python3
"""Checks for envelope_score.py and protocol_audit.py: known answers
first, both directions, on constructed rows labelled so. Writes samples/.

    python3 envelope-asymmetry/selftest_env.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import envelope_score as ES  # noqa: E402
import protocol_audit as A  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_env")
    for f in ("envelope_score.py", "protocol_audit.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)
    R = A.row
    # ---- schema, both directions
    good = R("d1", "A", (1, 0, 1, 0, 1, 0), 400)
    check("a well-formed row validates", ES.validate_rows([good]) == [])
    bad = dict(good, envelope_score=5)
    check("a stored score that is not the marker sum is refused", any("marker sum" in f for f in ES.validate_rows([bad])))
    bad = dict(good, structural_absence=True)
    check("structural absence with a marker present is refused", any("structural absence" in f for f in ES.validate_rows([bad])))
    bad = dict(good, E3=2)
    check("a marker outside {0,1} is refused", any("outside" in f for f in ES.validate_rows([bad])))
    bad = dict(good, doc_words=0)
    check("zero words on an existing document is refused", any("zero words" in f for f in ES.validate_rows([bad])))
    absent = R("d2", "B", (1, 1, 1, 1, 1, 1), 0, absent=True)
    check("a structural absence carries score 0, zero words, and validates", absent["envelope_score"] == 0 and ES.validate_rows([absent]) == [])
    check("per-1000 is None on a document with no words, 5.0 on 1000 words with five markers",
          ES.per_1000(absent) is None and ES.per_1000(R("x", "A", (1, 1, 1, 1, 1, 0), 1000)) == 5.0)
    # ---- agreement and the gate
    agr = ES.agreement([good])
    check("no double-coded document: agreement undetermined and the gate refuses", agr["kappa"] is None and not ES.gate(agr)[0])
    kv = A.kappa_vs_percent()
    check("one disagreement on E6 over 20 docs: E6 percent 0.95, E6 kappa 0.0, pooled gate passes on both statistics",
          kv["one_disagreement"]["E6_percent"] == 0.95 and kv["one_disagreement"]["E6_kappa"] == 0.0
          and kv["one_disagreement"]["gate_percent"][0] and kv["one_disagreement"]["gate_kappa_pooled"][0])
    check("all-absent double coding: kappa 1.0 and the gate passes with no marker ever coded present",
          kv["all_absent"]["kappa"] == 1.0 and kv["all_absent"]["gate_kappa"][0])
    few = [R("d%d" % i, "A", (1, 0, 0, 0, 0, 0), 100, coder="c1") for i in range(10)] + [R("d0", "A", (1, 0, 0, 0, 0, 0), 100, coder="c2")]
    check("double-coded share below 0.20 refuses the gate", not ES.gate(ES.agreement(few))[0] and "share" in ES.gate(ES.agreement(few))[1])
    low = [R("d%d" % i, "A", (1, 0, 0, 0, 0, 0), 100, coder="c1") for i in range(10)] + [R("d%d" % i, "A", (0, 1, 1, 0, 0, 0), 100, coder="c2") for i in range(10)]
    check("kappa below 0.7 refuses the gate", not ES.gate(ES.agreement(low))[0] and "underspecified" in ES.gate(ES.agreement(low))[1])
    # ---- sign test known answers
    check("sign test: 10 positive of 10 gives 2/1024; all zero gives None; 5/5 gives 1.0",
          abs(ES.sign_test([1] * 10) - 2 / 1024) < 1e-12 and ES.sign_test([0, 0]) is None and ES.sign_test([1] * 5 + [-1] * 5) == 1.0)
    # ---- test 1
    t = ES.test1([])
    check("test 1 with no pair: undetermined", t["reading"] == "undetermined")
    sa = A.structural_absence_flip()
    check("structural absence: all-pairs reads SPLIT at mean diff 1.0, documents-only reads KILL at 0.0, absence rate 1/3",
          sa["all_pairs"][0] == 1.0 and sa["all_pairs"][1].startswith("SPLIT") and sa["documents_only"][0] == 0.0
          and sa["documents_only"][1].startswith("KILL") and abs(sa["absence_rate"] - 1 / 3) < 1e-12)
    e6 = A.e6_flat_two_ways()
    check("E6 flat at 0 reads SPLIT; flat at 1 reads the split as not applying",
          e6["E6_flat_at_0"].startswith("SPLIT") and "does not apply" in e6["E6_flat_at_1"])
    rows = []
    for i in range(30):
        rows.append(R("a%d" % i, "A", (1, 1, 1, 1, 0, 1), 800 + 20 * i, pair=i))
        rows.append(R("b%d" % i, "B", (1, 0, 0, 0, 0, 0), 500 + 20 * i, pair=i))
    t = ES.test1(rows)
    check("A >> B with E6 varying reads SUPPORTED; per-marker deltas 0/1/1/1/0/1", t["all_pairs"]["reading"].startswith("SUPPORTED")
          and [t["all_pairs"]["per_marker"][m] for m in ES.MARKERS] == [0.0, 1.0, 1.0, 1.0, 0.0, 1.0] and t["min_pairs_met"])
    # ---- test 2
    tk = A.template_kill()
    check("template kill: zero variance at n=100 and at n=2, reading names the re-target", tk["n100_zero_variance"] and tk["n2_zero_variance"] and "re-target" in tk["n100_reading"])
    r2 = [R("f%d" % i, "A", (1, 1, 0, 1, 0, 0), 300) for i in range(50)] + [R("g%d" % i, "B", (0, 0, 0, 0, 0, 0), 300) for i in range(50)]
    check("A > B on E1/E2/E4 reads SUPPORTED with min n met", ES.test2(r2)["reading"].startswith("SUPPORTED") and ES.test2(r2)["min_n_met"])
    r2[0] = dict(r2[0], filing_period="P2")
    check("two filing periods refuse test 2", ES.test2(r2)["reading"] == "REFUSED")
    check("an empty arm is undetermined", ES.test2([R("f", "A", (1, 0, 0, 0, 0, 0), 300)])["reading"] == "undetermined")
    # ---- threats
    inv = A.per_1000_inversion()
    check("per-1000 secondary outcome ranks the short document above the long one; the primary ranks the reverse",
          inv["primary_prefers_long"] and inv["secondary_prefers_short"])
    cv = ES.covariate(rows)
    # A scores 5, B scores 1, so the arm coefficient is 4.0 (a first draft of this line said 3.0)
    check("covariate OLS: arm coefficient 4.0 with words varying; None when words are constant",
          cv["beta"] is not None and abs(cv["beta"][2] - 4.0) < 1e-9
          and ES.covariate([R("c%d" % i, "A" if i % 2 else "B", (1, 0, 0, 0, 0, 0), 300) for i in range(8)])["beta"] is None)
    check("unblindable fraction is None when never recorded, 0.5 when half inferable",
          ES.unblindable(rows)["fraction"] is None and ES.unblindable([dict(good, domain_inferable=True), dict(good, domain_inferable=False)])["fraction"] == 0.5)
    d = ES.domains()
    check("T4 pre-registration: seven arm A domains, two mid-standard, hash printed", len(d["arm_A"]) == 7 and d["t4_met"] and len(d["sha256"]) == 16)
    # ---- protocol text and cross-links
    mm = A.marker_map()
    check("five of six markers map onto a claim-record field; E6 has none", mm["markers_without_field"] == ["E6"])
    cb = A.compressed_block()
    check("the compressed block drops nine of ten probed elements and keeps the inter-rater rule",
          sum(1 for v in cb.values() if v["in_full"] and not v["in_compressed"]) == 9 and cb["inter-rater rule"]["in_compressed"])
    check("readout-count records whether a channel returns", A.domain_of_arm_A_in_readout_count()["positions_returning"])
    # ---- renders and the screen
    out_u = ES.render([])
    out_r = ES.render(rows)
    out_a = A.render()
    for name, txt in (("unfilled", out_u), ("constructed", out_r), ("audit", out_a)):
        check("%s render screens clean" % name, not no_severity.hits(txt))
    check("screen fires on a planted word", bool(no_severity.hits(out_a + "\nthis is wrong\n")))
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    for name, txt in (("envelope_unfilled", out_u), ("envelope_constructed", out_r), ("protocol_audit", out_a)):
        with open(os.path.join(HERE, "samples", name + ".sample.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt + "\n")
    with open(os.path.join(HERE, "samples", "constructed_rows.sample.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows[:4]:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
