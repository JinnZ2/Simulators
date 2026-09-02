#!/usr/bin/env python3
"""Checks for label_position_test.py. Known answers first, then both
directions of every guard. Rows here are CONSTRUCTED and say so in
their source_url scheme; nothing is a claim about any case.

    python3 label-position-test/selftest_lpt.py
"""

import ast
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import label_position_test as L  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def row(**kw):
    base = dict(actor_class="agent", position_t0="up", move="declared_path",
                wall_author="task_setter", wall_purpose_visible_to_actor="y",
                cost_bearer="self", outcome_t1="success", label_source="press",
                label_term="cheat", label_valence="-", label_t="2026-01-01",
                relabel_term="", relabel_t="", arbiter="press",
                beneficiary="press", overlap="y",
                source_url="constructed://fixture/1")
    base.update(kw)
    return base


def to_csv(rows):
    buf = io.StringIO()
    w = __import__("csv").DictWriter(buf, fieldnames=L.FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


# --- constructed worlds ----------------------------------------------
MOVES = L.VOCAB["move"]
CLASSES = L.VOCAB["actor_class"]


def world_position(n=24):
    """valence tracks position_t0 and nothing else (H1 by construction)."""
    out = []
    for i in range(n):
        pos = "up" if i % 2 == 0 else "down"
        out.append(row(position_t0=pos, label_valence="+" if pos == "up" else "-",
                       move=MOVES[i % 3], outcome_t1=L.VOCAB["outcome_t1"][(i // 2) % 3],
                       actor_class=CLASSES[(i // 3) % 4],
                       label_term="innovation" if pos == "up" else "cheat",
                       source_url="constructed://fixture/pos/%d" % i))
    return out


def world_move(n=24):
    """valence tracks move and nothing else (H0 by construction)."""
    out = []
    for i in range(n):
        mv = MOVES[i % 3]
        out.append(row(move=mv, label_valence={"declared_path": "+",
                                                "undeclared_open": "0",
                                                "built_wall_crossed": "-"}[mv],
                       position_t0=L.VOCAB["position_t0"][(i // 3) % 3],
                       outcome_t1=L.VOCAB["outcome_t1"][(i // 2) % 3],
                       actor_class=CLASSES[(i // 5) % 4],
                       label_term=mv, source_url="constructed://fixture/move/%d" % i))
    return out


def main():
    print("selftest_lpt")

    # ---- known answers: chi2 and Cramer's V by hand
    check("V=1 on a perfect 2x2",
          abs(L.cramers_v({"+": {"a": 10}, "-": {"b": 10}}) - 1.0) < 1e-12)
    check("V=0 on an independent 2x2",
          abs(L.cramers_v({"+": {"a": 5, "b": 5}, "-": {"a": 5, "b": 5}})) < 1e-12)
    hand = {"+": {"a": 3, "b": 1, "c": 0}, "-": {"a": 0, "b": 1, "c": 3}}
    x, n, r, k = L.chi2(hand)
    check("chi2 on the hand table is 6.0", abs(x - 6.0) < 1e-12 and n == 8)
    check("V on the hand table is sqrt(0.75)",
          abs(L.cramers_v(hand) - 0.75 ** 0.5) < 1e-12)
    check("V is None with one row level (undefined, not zero)",
          L.cramers_v({"+": {"a": 3, "b": 4}}) is None)
    check("V is None with one column level",
          L.cramers_v({"+": {"a": 3}, "-": {"a": 4}}) is None)
    check("V is None on an empty table", L.cramers_v({}) is None)

    # ---- the two constructed worlds separate on the order's rule
    wp = L.validate_rows(world_position())
    wm = L.validate_rows(world_move())
    vp, vm = L.cross_tabs(wp), L.cross_tabs(wm)
    check("position world: V_position = 1", abs(vp["V_position"] - 1.0) < 1e-12)
    check("position world: V_move ~ 0", vp["V_move"] < 0.05)
    check("position world: order's rule does not falsify H1",
          L.h1_rule(vp).startswith("H1 not falsified"))
    check("move world: V_move = 1", abs(vm["V_move"] - 1.0) < 1e-12)
    check("move world: V_position ~ 0", vm["V_position"] < 0.05)
    check("move world: order's rule falsifies H1", L.h1_rule(vm).startswith("H1 FALSE"))
    check("rule is undetermined when a V is None",
          L.h1_rule({"V_move": None, "V_position": 0.5, "V_outcome": 0.1}) == "undetermined")

    # ---- per-term rows are undefined by construction where valence is constant
    tab = L.output_table(wp)
    terms = {t["term"]: t for t in tab}
    check("output table has ALL plus one row per term",
          set(terms) == {"ALL", "innovation", "cheat"})
    check("term row with constant valence has V None on every axis",
          all(terms["cheat"][k] is None for k in ("V_position", "V_move", "V_outcome", "V_actor")))
    check("pooled row carries the V", terms["ALL"]["V_position"] is not None)

    # ---- schema refusals, both directions
    good = [row()]
    check("a valid row validates", L.validate_rows(good) is good)
    for bad, why in [
        ({"actor_class": "robot"}, "vocabulary"),
        ({"label_valence": ""}, "empty required"),
        ({"source_url": "metr.org/report.pdf"}, "not a URL"),
    ]:
        try:
            L.validate_rows([row(**bad)])
            check("refuses %s" % why, False)
        except L.SchemaRefused:
            check("refuses %s" % why, True)
    try:
        r = row(); del r["overlap"]
        L.validate_rows([r]); check("refuses missing column", False)
    except L.SchemaRefused:
        check("refuses missing column", True)
    try:
        r = row(); r["extra"] = "x"
        L.validate_rows([r]); check("refuses extra column", False)
    except L.SchemaRefused:
        check("refuses extra column", True)
    try:
        L.validate_rows([]); check("refuses zero rows", False)
    except L.SchemaRefused:
        check("refuses zero rows", True)
    check("empty relabel cells are a state, not a gap",
          L.validate_rows([row(relabel_term="", relabel_t="")]) is not None)
    check("load_csv round-trips the constructed world",
          len(L.load_csv(to_csv(wp))) == len(wp))
    check("provenance counts constructed rows apart from public",
          L.provenance(wp) == {"constructed": len(wp)})
    check("provenance counts http(s) as public",
          L.provenance([row(source_url="https://x/y")]) == {"public": 1})

    # ---- overlap (P5)
    ov = L.overlap_rates([row(arbiter="a", beneficiary="a"),
                          row(arbiter="b", beneficiary="b"),
                          row(arbiter="a", beneficiary="a"),
                          row(arbiter="b", beneficiary="b")])
    o = ov["press"]
    check("overlap strict = 1.0 when coded y throughout", o["strict"] == 1.0)
    check("chance under independence = 0.5 with two parties balanced",
          abs(o["chance"] - 0.5) < 1e-12)
    check("H2 not falsified there", L.h2_rule(ov)["press"].startswith("H2 not"))
    ov1 = L.overlap_rates([row(arbiter="a", beneficiary="a")] * 3)
    check("one party throughout: chance = 1, so H2 FALSE by construction",
          ov1["press"]["chance"] == 1.0 and L.h2_rule(ov1)["press"].startswith("H2 FALSE"))
    ovd = L.overlap_rates([row(arbiter="a", beneficiary="a", overlap="n")])
    check("coded overlap disagreeing with derived is counted",
          ovd["press"]["coded_vs_derived_disagree"] == 1)
    ovp = L.overlap_rates([row(arbiter="a", beneficiary="b", overlap="partial")])
    check("partial is not counted as a disagreement",
          ovp["press"]["coded_vs_derived_disagree"] == 0)
    check("half rate weights partial at 0.5", ovp["press"]["half"] == 0.5
          and ovp["press"]["strict"] == 0.0)
    check("overlap is per label_source class",
          set(L.overlap_rates([row(label_source="x"), row(label_source="y")])) == {"x", "y"})

    # ---- leak test (P2), both directions
    leaky = []
    for i in range(12):
        mv = MOVES[i % 3]
        leaky.append(row(move=mv, actor_class={"declared_path": "agent",
                                               "undeclared_open": "firm",
                                               "built_wall_crossed": "state"}[mv]))
    lk = L.leak_test(leaky)
    check("leaky world: in-sample 1.0", lk["in_sample"] == 1.0)
    check("leaky world: leave-one-out 1.0 (tuples repeat)", lk["loo"] == 1.0)
    check("leaky world: baseline is the majority share", abs(lk["baseline"] - 4 / 12) < 1e-12)
    inert = [row(move=MOVES[i % 3], actor_class=CLASSES[(i // 3) % 4]) for i in range(24)]
    lk0 = L.leak_test(inert)
    check("inert world: leave-one-out at or below baseline", lk0["loo"] <= lk0["baseline"] + 1e-9)
    uniq = [row(move=MOVES[i % 3], wall_author=L.VOCAB["wall_author"][i // 3],
                cost_bearer=L.VOCAB["cost_bearer"][i % 4],
                actor_class=CLASSES[i % 4]) for i in range(9)]
    lku = L.leak_test(uniq)
    check("unique tuples: in-sample reads 1.0 by construction",
          lku["distinct_tuples"] == 9 and lku["in_sample"] == 1.0)
    check("unique tuples: leave-one-out does not", lku["loo"] < 1.0)
    check("tuple space is 72", L._tuple_space() == 72)
    check("empty leak test is None, not 0", L.leak_test([])["loo"] is None)

    # ---- within-document control
    wd = L.within_document_control([
        row(source_url="constructed://doc/1", move="declared_path", label_valence="+"),
        row(source_url="constructed://doc/1", move="built_wall_crossed", label_valence="-"),
        row(source_url="constructed://doc/2"),
    ])
    check("a pair differing on move alone with a valence flip reads 1.0",
          wd["constructed://doc/1"]["valence_varies"] == 1.0)
    check("a single-row URL carries nothing and is None",
          wd["constructed://doc/2"]["valence_varies"] is None)
    wd2 = L.within_document_control([
        row(source_url="constructed://doc/3", move="declared_path", position_t0="up"),
        row(source_url="constructed://doc/3", move="built_wall_crossed", position_t0="down"),
    ])
    check("a pair that also moves position is not a control pair",
          wd2["constructed://doc/3"]["pairs"] == 0)

    # ---- relabel agreement (P3), known answers
    ra = L.relabel_agreement({"r1": {"a": "+", "b": "+", "c": "+"},
                              "r2": {"a": "-", "b": "-", "c": "-"}})
    check("perfect agreement: pairwise 1, kappa 1", ra["pairwise"] == 1.0 and ra["kappa"] == 1.0)
    ra1 = L.relabel_agreement({"r1": {"a": "+", "b": "+"}, "r2": {"a": "+", "b": "+"}})
    check("one category throughout: kappa None", ra1["kappa"] is None and ra1["pairwise"] == 1.0)
    rah = L.relabel_agreement({"r1": {"a": "x", "b": "x", "c": "y"},
                               "r2": {"a": "y", "b": "y", "c": "y"}})
    check("hand Fleiss: pairwise 2/3, kappa 0.25",
          abs(rah["pairwise"] - 2 / 3) < 1e-12 and abs(rah["kappa"] - 0.25) < 1e-12)
    try:
        L.relabel_agreement({"r1": {"a": "+"}}); check("refuses one labeler", False)
    except ValueError:
        check("refuses one labeler", True)
    check("empty relabel sheet is None throughout",
          L.relabel_agreement({})["kappa"] is None)

    # ---- no interior claims: the verdict strings only restate the rule
    src = open(os.path.join(HERE, "label_position_test.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    check("instrument imports no statistics library",
          not any(m in src for m in ("import numpy", "import scipy", "import statistics")))
    check("no author section", "Author" not in src and "author:" not in src.lower())

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "label_position_test.py"),
                         "--selftest"], capture_output=True).returncode
    check("instrument refuses --selftest with rc 2", rc == 2)
    out_u = L.render(None)
    out_f = L.render(wp, {"r1": {"a": "+", "b": "+"}, "r2": {"a": "-", "b": "+"}})
    check("unfilled render screens clean", not no_severity.hits(out_u))
    check("constructed render screens clean", not no_severity.hits(out_f))
    check("screen fires on a planted word",
          bool(no_severity.hits(out_f + "\nthis label is wrong\n")))
    check("every [CHOICE] is printed in both renders",
          all(("[CHOICE %d]" % i) in out_u and ("[CHOICE %d]" % i) in out_f for i in (1, 2, 3)))
    check("unfilled render says no rows and names the seed case",
          "ROWS: none" in out_u and "METR" in out_u)
    check("constructed render says its rows are not public record",
          "not public record" in out_f)

    # ---- the v2 revision, as a copy and as a claim
    import revision_audit as RA
    v1, v2 = RA._read(RA.V1), RA._read(RA.V2)
    pi = RA.pure_insertion(v1, v2)
    check("v2 is a pure insertion into v1 that reassembles v1", pi["pure"] and pi["reassembles"])
    check("the inserted block is the N2 CONTROL bullet, six lines",
          pi["lines"] == 6 and "N2 CONTROL" in pi["block"])
    doctored = v2.replace("H0  labels track the move", "H0  labels track the actor")
    check("a doctored v2 with a second change is not a pure insertion",
          RA.pure_insertion(v1, doctored)["pure"] is False)
    check("changelog unchanged across the revision",
          RA.section(v1, "CHANGELOG") == RA.section(v2, "CHANGELOG"))
    check("section() returns None on a missing heading", RA.section(v1, "NO SUCH") is None)
    r = RA.referent(v1, v2)
    check("N2 and null have no occurrence in v1", r["v1_N2"] == [] and r["v1_null"] == [])
    check("N2 and null each occur once in v2, inside the bullet",
          len(r["v2_N2"]) == 1 and len(r["v2_null"]) == 1 and 92 <= r["v2_N2"][0] <= 97)
    check("the referent's N2 title is read from the null construction",
          r["null_construction_N2"].startswith("curriculum present"))
    mm = RA.measurable_map()
    check("three measurables mapped", len(mm) == 3)
    check("every mapped field exists in the sibling sheet", all(m["fields_exist"] for m in mm.values()))
    check("one exact, two partial", sorted(m["fit"] for m in mm.values()) == ["exact", "partial", "partial"])
    t = RA.transparency_removes()
    check("N3 states three inputs and transparency removes one",
          t["before"] == ["gradient", "open channel", "opacity"] and t["removed"] == 1)
    oc = RA.outcome_check()
    check("the bullet's persists reading names the template where the table routes to N3",
          oc["persists"]["names_template"] and oc["persists"]["routes_to_N3"])
    rc = subprocess.run([sys.executable, os.path.join(HERE, "revision_audit.py"), "--selftest"],
                        capture_output=True).returncode
    check("revision_audit refuses --selftest with rc 2", rc == 2)
    out_r = RA.render()
    # declared exemption: `risk` inside the delivered term "self-risk rate", three arms
    masked = out_r.replace("self-risk", "self-r1sk")
    check("revision render clean with the delivered term masked", not no_severity.hits(masked))
    check("the delivered term is the only thing that fires",
          {h[1] for h in no_severity.hits(out_r)} == {"risk"})
    check("a planted word is caught through the exemption",
          {h[1] for h in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})
    with open(os.path.join(HERE, "samples", "revision_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_r)

    # ---- pin the samples
    sd = os.path.join(HERE, "samples")
    with open(os.path.join(sd, "constructed_rows.csv"), "w", encoding="utf-8") as fh:
        fh.write(to_csv(wp))
    with open(os.path.join(sd, "constructed_relabel.json"), "w", encoding="utf-8") as fh:
        json.dump({"r1": {"a": "+", "b": "+"}, "r2": {"a": "-", "b": "+"}}, fh, indent=1)
    with open(os.path.join(sd, "render_constructed.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_f)
    with open(os.path.join(sd, "render_unfilled.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_u)

    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
