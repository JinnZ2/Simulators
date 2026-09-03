#!/usr/bin/env python3
"""Checks for gap_audit.py. Known answers first, both directions of
every check. Every figure used is carried from the delivered document;
nothing here is a statement about any carrier or claimant.

    python3 claim-refusal-gap/selftest_crg.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import gap_audit as G  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_crg")
    text = G._read()

    # ---- anchor
    rows = G.anchor(text)
    check("two anchor rows parsed", len(rows) == 2 and rows[0]["y2025"] == "45" and rows[1]["y2016"] == "~25")
    ta = G.two_arm(rows)
    check("treated delta +10 with range +8..+12 under the tilde band",
          ta["arms"][0]["delta_point"] == 10 and ta["arms"][0]["delta_range"] == (8, 12))
    check("control delta 0 with range -4..+4", ta["arms"][1]["delta_point"] == 0 and ta["arms"][1]["delta_range"] == (-4, 4))
    check("difference of deltas +10, range +4..+16", ta["difference_point"] == 10 and ta["difference_range"] == (4, 16))
    check("with no tildes the range collapses to the point",
          G.two_arm([{"line": "a", "y2016": "35", "y2025": "45"}, {"line": "b", "y2016": "25", "y2025": "25"}])["difference_range"] == (10, 10))

    # ---- gaps and designs
    g, d = G.gaps(text), G.designs(text)
    check("seven gaps, five designs", len(g) == 7 and len(d) == 5)
    check("G-5 is marked primary and every gap has a Missing line",
          g["G-5"]["primary"] and all(v["missing"] for v in g.values()))
    cov = G.gap_coverage(text)
    check("G-6 and G-7 have no design; the rest do",
          [k for k, v in cov.items() if v is None] == ["G-6", "G-7"])
    check("E-4 bounds G-2 rather than closing it", d["E-4"]["relation"] == "bounds" and d["E-4"]["gap"] == "G-2")
    check("a doctored design line is parsed with its gap",
          G.designs("### E-9 (closes G-7) x\n")["E-9"]["gap"] == "G-7")

    # ---- G-2 estimator
    check("UM rate at 0/0 is None, not zero", G.um_rate(0, 0) is None)
    check("displacement of 50 moves (100, 1000) to 150/950", abs(G.displacement(100, 1000, 50) - 150 / 950) < 1e-12)
    ex = G.same_reading_two_causes(100, 1000, 50)
    check("the two worlds are the same pair and are not distinguishable from the ratio",
          ex["displacement_world"] == ex["non_purchase_world"] and ex["distinguishable_from_ratio"] is False)
    check("rose anyway: BI +10% and ratio +10% needs UM +21%", abs(G.rose_anyway(0.1, 0.1) - 0.21) < 1e-12)
    check("ratio flat with BI +10% needs UM +10%", abs(G.rose_anyway(0.1, 0.0) - 0.10) < 1e-12)

    # ---- G-3 rebase
    rb = G.rebase_summary(text)
    check("four rebase rows and every stated delta reproduces", len(rb["rows"]) == 4 and rb["all_match"])
    check("mean seam 1.45", rb["mean_seam"] == 1.45)
    check("1993 16.0 beats 2023 15.4 on the newer basis; restated 16.9 beats it",
          rb["record_on_newer_basis"] is False and rb["v2023_restated"] == 16.9 and rb["record_on_restated"])
    doct = text.replace("| 2015 | 13.0 | 11.3 | -1.7 |", "| 2015 | 13.0 | 11.3 | -1.9 |")
    check("a doctored delta is caught", G.rebase_summary(doct)["all_match"] is False)

    # ---- G-4 litigation
    li = G.litigation(text)
    check("litigation +8 against CWP +10, ratio 0.80, netted bounds (2, 10)",
          li["litigation_move"] == 8 and li["cwp_move"] == 10 and li["ratio"] == 0.8 and li["netted_move_bounds"] == (2, 10))

    # ---- G-5 volume
    check("wrongful total is None while the unappealed rate is None", G.wrongful_total(100, 0.01, 0.467, None) is None)
    fac = G.g5_factor(0.01, 0.467)
    check("factor between the two readings is 1/appeal_rate = 100", abs(fac["factor"] - 100) < 1e-9)
    check("published-only share is overturn x appeal rate", abs(fac["published_only"] - 0.00467) < 1e-12)
    check("converged share is the overturn rate", abs(fac["if_converged"] - 0.467) < 1e-12)
    f5 = G.g5_figures(text)
    check("NY trend read back 38 -> 52.5", f5["overturn_2019"] == 38.0 and f5["overturn_2025"] == 52.5)

    # ---- mechanisms and sources
    mm = G.mechanism_map()
    check("every named mechanism is in the register; three gaps name none",
          all(m["in_register"] for m in mm.values() if m["mechanism"]) and
          [k for k, m in mm.items() if m["mechanism"] is None] == ["G-2", "G-5", "G-6"])
    s = G.sources(text)
    check("zero URLs and seven named sources", s["urls"] == 0 and len(s["named"]) == 7)

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "gap_audit.py"), "--selftest"], capture_output=True).returncode
    check("gap_audit refuses --selftest with rc 2", rc == 2)
    out = G.render()
    # declared exemption: `error` inside the delivered G-5 title, rendered from the parse; three arms
    masked = out.replace("refusal error rate", "refusal err0r rate")
    check("render clean with the delivered title masked", not no_severity.hits(masked))
    check("the delivered title is the only thing that fires", {h[1] for h in no_severity.hits(out)} == {"error"}
          and all("refusal error rate" in h[2] for h in no_severity.hits(out)))
    check("a planted word is caught through the exemption",
          {h[1] for h in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})
    check("no author section", "Author" not in open(os.path.join(HERE, "gap_audit.py"), encoding="utf-8").read())
    with open(os.path.join(HERE, "samples", "gap_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
