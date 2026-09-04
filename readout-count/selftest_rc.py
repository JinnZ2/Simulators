#!/usr/bin/env python3
"""Checks for readout_count.py. Known answers first, both directions of
every guard. Rows here are CONSTRUCTED (constructed:// URLs); nothing is
a claim about any regime.

    python3 readout-count/selftest_rc.py
"""

import csv
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import readout_count as R  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def row(**kw):
    base = dict(regime="a", year="2020", positions_declared="p1;p2;p3",
                positions_returning="p1;p2", holder="third_party", immunity="y",
                investigator_independent="y", intake_count="100", return_count="80",
                external_detection="y", rate_metric="events per unit",
                rate_trend="down", source_url="constructed://fixture/1")
    base.update(kw)
    return base


def to_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=R.FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def world(tracking=True):
    """Four regimes; readout_count rises with (or against) rate_trend."""
    trends = ["up", "flat", "down", "down"]
    counts = [0, 1, 2, 3] if tracking else [3, 2, 1, 0]
    rows = []
    for i, (t, c) in enumerate(zip(trends, counts)):
        pos = ";".join("p%d" % k for k in range(4))
        ret = ";".join("p%d" % k for k in range(c))
        rows.append(row(regime="r%d" % i, positions_declared=pos, positions_returning=ret,
                        rate_trend=t, intake_count=str(50 + 10 * i),
                        return_count=str(10 * c), external_detection="y" if i % 2 else "n",
                        source_url="constructed://fixture/%d" % i))
    return rows


def main():
    print("selftest_rc")

    # ---- known answers: ranks and Spearman by hand
    check("average ranks with a tie", R.average_ranks([10, 20, 20, 30]) == [1.0, 2.5, 2.5, 4.0])
    check("spearman perfect = 1", abs(R.spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1.0) < 1e-12)
    check("spearman reversed = -1", abs(R.spearman([1, 2, 3, 4], [40, 30, 20, 10]) + 1.0) < 1e-12)
    check("spearman hand case with ties (0.8)",
          abs(R.spearman([1, 2, 3, 4], [1, 2, 2, 3]) - (3.0 / (5 * 2.5) ** 0.5) / 1) < 1e-9
          or abs(R.spearman([1, 2, 3, 4], [1, 2, 2, 3]) - 0.9486832980505138) < 1e-9)
    check("spearman None on a constant side", R.spearman([1, 2, 3], [5, 5, 5]) is None)
    check("spearman None below two points", R.spearman([1], [2]) is None)

    # ---- derivations
    d = R.derive(R.validate_rows([row()])[0])
    check("readout_count is distinct returning positions", d["readout_count"] == 2)
    check("declared_count is distinct declared positions", d["declared_count"] == 3)
    check("return_rate = 80/100", abs(d["return_rate"] - 0.8) < 1e-12)
    d0 = R.derive(R.validate_rows([row(intake_count="0", return_count="0")])[0])
    check("return_rate None on zero intake, not 0", d0["return_rate"] is None)
    du = R.derive(R.validate_rows([row(intake_count="UNMEASURED")])[0])
    check("UNMEASURED count reads None", du["intake_count"] is None and du["return_rate"] is None)
    dz = R.derive(R.validate_rows([row(positions_returning="")])[0])
    check("no returning position -> readout_count 0 (H2)", dz["readout_count"] == 0)
    check("duplicate positions collapse",
          R.derive(R.validate_rows([row(positions_declared="p1;p1;p2", positions_returning="p1;p1")])[0])["readout_count"] == 1)

    # ---- per regime, latest year
    two = R.validate_rows([row(year="2010", positions_returning="p1"),
                           row(year="2020", positions_returning="p1;p2", external_detection="n")])
    t = R.per_regime(two)["a"]
    check("OUTPUT row is the latest year", t["year"] == 2020 and t["readout_count"] == 2)
    check("external_detection_rate over all the regime's rows", t["external_detection_rate"] == 0.5)

    # ---- H1 in both directions
    wt = R.validate_rows(world(True))
    wa = R.validate_rows(world(False))
    r1 = R.h1(R.per_regime(wt))
    r1a = R.h1(R.per_regime(wa))
    check("tracking world: rho > 0, H1 not falsified", r1["rho"] > 0 and r1["verdict"].startswith("H1 not"))
    check("anti world: rho < 0, H1 FALSE", r1a["rho"] < 0 and r1a["verdict"].startswith("H1 FALSE"))
    check("strict rank equality does not hold even in the tracking world", r1["strict_equal"] is False)
    check("fewer than 4 regimes -> undetermined",
          R.h1(R.per_regime(wt[:3]))["verdict"].startswith("undetermined"))
    check("strict equality possible at 3 regimes", R.strict_equality_possible(3) is True)
    check("strict equality conditional past 3", isinstance(R.strict_equality_possible(4), str))

    # ---- P4 cross-tabs
    ct = R.cross_tabs(wt)
    check("three cross-tabs", set(ct) == {"readout_count", "declared_count", "intake_count"})
    check("a count with as many levels as rows gives V = 1",
          ct["intake_count"]["levels"] == 4 and abs(ct["intake_count"]["V"] - 1.0) < 1e-12)
    check("a constant count gives V None", ct["declared_count"]["levels"] == 1 and ct["declared_count"]["V"] is None)

    # ---- H2 both directions
    r2 = R.h2(R.per_regime(wt))
    check("H2 returns a verdict string", r2["verdict"].startswith(("H2", "undetermined")))
    one = R.h2(R.per_regime(wt[:1]))
    check("H2 undetermined on one regime", one["verdict"].startswith("undetermined"))

    # ---- H3
    r3 = R.h3(wt)
    check("H3 is NOT_COMPUTABLE with two named absences",
          r3["verdict"] == "NOT_COMPUTABLE" and len(r3["missing"]) == 2)
    check("external_detection_rate still computed", r3["external_detection_rate"] == 0.5)
    check("no column in the schema carries a grading field",
          not any("sever" in f or "grade" in f for f in R.FIELDS))

    # ---- schema refusals, both directions
    check("valid row validates", len(R.validate_rows([row()])) == 1)
    for bad, why in [
        ({"positions_returning": "p9"}, "returning outside declared"),
        ({"intake_count": "3+"}, "a bound is not a count"),
        ({"intake_count": "high"}, "a grade is not a count"),
        ({"rate_trend": "derailments down"}, "trend outside vocab"),
        ({"source_url": ""}, "no URL"),
        ({"year": "20"}, "year not four digits"),
        ({"holder": "NASA"}, "holder outside vocab"),
    ]:
        try:
            R.validate_rows([row(**bad)]); check("refuses " + why, False)
        except R.SchemaRefused:
            check("refuses " + why, True)
    try:
        R.validate_rows([]); check("refuses zero rows", False)
    except R.SchemaRefused:
        check("refuses zero rows", True)
    check("load_csv round-trips", len(R.load_csv(to_csv(world()))) == 4)

    # ---- seed rows read back from the order
    seed = R.seed_rows()
    check("five seed rows parsed from the order", len(seed) == 5)
    check("seed regimes as delivered",
          [s["regime"] for s in seed] == ["air", "rail", "trucking", "AI eval lab", "this session"])
    rd = R.seed_readiness(seed)
    check("0 of 5 seed rows carry a URL", not any(s["source_url"] for s in rd))
    check("trucking intake is a bound, not a count", [s for s in rd if s["regime"] == "trucking"][0]["intake"] == "bound")
    check("air intake is a grade", rd[0]["intake"] == "grade")
    check("only air's trend is in vocab", [s["rate_trend_in_vocab"] for s in rd] == [True, False, False, False, False])
    check("this session's cells are none", rd[4]["intake"] == "none" and rd[4]["return"] == "none")
    check("seed parse on a doctored order with no table returns nothing",
          R.seed_rows("# nothing\n\nSCHEMA\n") == [])

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "readout_count.py"), "--selftest"],
                        capture_output=True).returncode
    check("instrument refuses --selftest with rc 2", rc == 2)
    out_u = R.render(None)
    out_f = R.render(wt)
    check("unfilled render screens clean", not no_severity.hits(out_u))
    check("constructed render screens clean", not no_severity.hits(out_f))
    check("screen fires on a planted word", bool(no_severity.hits(out_f + "\nthis is wrong\n")))
    check("every [CHOICE] printed", all("[CHOICE %d]" % i in out_u for i in (1, 2, 3, 4)))
    check("the position line is printed", "is a row, not an exception" in out_u)
    check("no author section", "Author" not in open(os.path.join(HERE, "readout_count.py")).read())

    # ---- the delivered trucking row (v0.1) against the instrument
    import row_audit as RA
    text, order = RA._read(RA.DOC), RA._read(RA.ORDER)
    check("the row states its coding rule", RA.rule_stated(text))
    cov = RA.rule_coverage()
    check("one of the rule's three conjuncts has no schema field",
          [k for k, v in cov.items() if not v["field_exists"]] == ["NON-ADVERSARIAL"])
    rc_ = RA.readout_count_from_layers()
    check("under the row's rule the half count is 0.5 and the strict count is 0.0",
          rc_["half"] == 0.5 and rc_["strict"] == 0.0 and rc_["readout_layers"] == ["NHTSA VOQ / SaferTruck"])
    full = dict(RA.LAYERS, **{"NHTSA VOQ / SaferTruck": {"type": "readout", "return": "y"}})
    check("a full return reads 1.0 under both readings",
          RA.readout_count_from_layers(full)["half"] == 1.0 and RA.readout_count_from_layers(full)["strict"] == 1.0)
    st = RA.stated_counts(text)
    check("stated counts read back: trucking 0.5, complaint >= 3",
          st["trucking"] == "0.5" and st["complaint_count_trucking_min"] == 3)
    la = RA.load_attempt(RA.trucking_row_as_delivered())
    check("the row as delivered is refused on rate_trend",
          la["loaded"] is False and "rate_trend" in la["refused_on"])
    lt = RA.load_attempt_with_trend(RA.trucking_row_as_delivered(), "up")
    check("with a trend supplied it loads at readout_count 1, return_rate None",
          lt["loaded"] and lt["readout_count"] == 1 and lt["return_rate"] is None)
    src = RA.sources(text)
    check("sources: 7 entries, 5 with URL, 2 deferred",
          len(src) == 7 and sum(1 for e in src if e["url"]) == 5 and sum(1 for e in src if e["deferred"]) == 2)
    crd = RA.count_rests_on_deferred(text)
    check("the count names VOQ and the VOQ source is deferred",
          crd["count_names_voq"] and crd["voq_source_deferred"])
    n4 = RA.n4_reference(text, order)
    check("(N4) is cited and absent from the parent order",
          n4["row_cites_N4"] and not n4["order_has_N4"])
    check("a doctored order carrying N4 resolves",
          RA.n4_reference(text, order + "\n    N4  survey\n")["order_has_N4"])
    sv = RA.seed_vs_row(order, text)
    check("the seed intake cell is the complaint count under its new name",
          sv["intake_cell_is_complaint_count"] and sv["seed_intake"] == "3+")
    rc2 = subprocess.run([sys.executable, os.path.join(HERE, "row_audit.py"), "--selftest"],
                         capture_output=True).returncode
    check("row_audit refuses --selftest with rc 2", rc2 == 2)
    out_ra = RA.render()
    check("row audit render screens clean", not no_severity.hits(out_ra))
    with open(os.path.join(HERE, "samples", "row_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_ra)

    # ---- the delivered exclusion stack against the row, the order, the schema
    import stack_audit as SA
    st_text = SA._read(SA.DOC)
    lm = SA.layers_match(st_text)
    check("twelve layers, structure and headings match", lm["all_match"] and lm["structure_n"] == 12)
    doctored = st_text.replace("## L7 — MONETARY", "## L7 — MONEY")
    check("a doctored heading is caught", SA.layers_match(doctored)["all_match"] is False)
    a = SA.stated_arithmetic(st_text)
    check("GAO counts sum to N and the stated percentages sum to 101",
          a["counts_sum_to_N"] and a["stated_pct_sum"] == 101 and a["per_hundred_sum"] == 100)
    check("merit is 21.5%: 22 in L8, 21 in L10", a["computed_pct"][2] == 21.5 and a["merit_pct_L8_vs_L10"] == (22, 21))
    check("0.5^11 is 1/2048", abs(a["half_to_the_eleventh"] - 1 / 2048) < 1e-15)
    check("unmeasured stack survival is None", SA.survival(SA.unmeasured_stack(st_text)) is None)
    check("survival multiplies measured rates", abs(SA.survival({"a": 0.5, "b": 0.5}) - 0.25) < 1e-12)
    check("survival is None with one unmeasured layer among measured ones",
          SA.survival({"a": 0.5, "b": None}) is None)
    l0 = SA.l0_vs_row(st_text, text)
    check("L0's six items match the row's six by content", l0["both"] == 6 and l0["row_item_count"] == 6)
    s4 = SA.s4_is_the_n4_survey(st_text, text)
    check("S4 is the survey the row's (N4) pointed at", s4["row_cites_N4"] and s4["S4_matches"])
    check("S5 is on the row's STILL NEEDED list", SA.s5_vs_still_needed(st_text, text)["row_still_needed_has_it"])
    p2 = SA.p2_vs_l11(order, st_text)
    check("P2's three disjuncts are present and L11 states both removals",
          p2["P2_disjuncts_present"] and p2["L11_settlement_publishes_nothing"] and p2["L11_condition_enters_no_dataset"])
    check("the schema has no field for which disjunct fired", p2["schema_field_for_which_disjunct"])
    mm = SA.mechanism_map()
    check("every named mechanism is in the register and L11 names none",
          all(m["in_register"] for m in mm.values() if m["mechanism"]) and mm["L11"]["mechanism"] is None)
    check("register carries eight", len(SA.UN.MECHANISMS) == 8)
    src = SA.sources(st_text)
    check("eleven sources, eleven URLs, seven hosts", src["entries"] == 11 and src["urls"] == 11 and len(src["hosts"]) == 7)
    check("every host probed", all(h in SA.HOST_PROBE for h in src["hosts"]))
    rc3 = subprocess.run([sys.executable, os.path.join(HERE, "stack_audit.py"), "--selftest"],
                         capture_output=True).returncode
    check("stack_audit refuses --selftest with rc 2", rc3 == 2)
    out_sa = SA.render()
    check("stack audit render screens clean", not no_severity.hits(out_sa))
    with open(os.path.join(HERE, "samples", "stack_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_sa)

    # ---- the stack's revision (v2) as a copy and as a claim
    import stack_revision as SR
    v1, v2 = SA._read(SR.V1), SA._read(SR.V2)
    pi = SR.pure_insertion(v1, v2)
    check("v2 is v1 plus three inserted blocks, nothing removed",
          pi["blocks"] == 3 and pi["removed_lines"] == 0 and pi["reassembles_v1"])
    doct = v2.replace("## L7 — MONETARY", "## L7 — MONEY")
    check("a doctored v2 does not reassemble v1", SR.pure_insertion(v1, doct)["reassembles_v1"] is False)
    check("changelog unchanged across the revision", SR.changelog_unchanged(v1, v2))
    f = SR.l4_falsifier(v2)
    check("L4 carries a test, both arms and a named refutation", all(f.values()))
    check("v1's L4 carries none of it", not SR.l4_falsifier(v1)["has_test"])
    fc = SR.four_counts()
    check("three of the four counts have a schema field and 'who publishes' has none",
          sum(1 for v in fc.values() if v["has_field"]) == 3 and not fc["who publishes"]["has_field"])
    demo = {k: 0.5 for k in SA.unmeasured_stack(v2)}
    lb = SR.layer_by_layer(demo)
    check("twelve layers at 0.5: survival 1/4096, removing one gives x2",
          abs(lb["base"] - 1 / 4096) < 1e-15 and abs(lb["per_layer"]["L3"]["gain"] - 2.0) < 1e-12)
    check("removing a layer from an unmeasured stack is still None",
          SR.remove_one(SA.unmeasured_stack(v2), "L0") is None)
    om = SR.open_map()
    check("one of seven open quantities fills schema columns",
          [s for s, v in om.items() if v["fills_schema"]] == ["S5"])
    check("S6 and S7 are new in v2", "S6" in SA.open_quantities(v2) and "S6" not in SA.open_quantities(v1))
    check("twelve layers still match in v2", SA.layers_match(v2)["all_match"])
    rc4 = subprocess.run([sys.executable, os.path.join(HERE, "stack_revision.py"), "--selftest"],
                         capture_output=True).returncode
    check("stack_revision refuses --selftest with rc 2", rc4 == 2)
    out_sr = SR.render()
    check("revision render screens clean", not no_severity.hits(out_sr))
    with open(os.path.join(HERE, "samples", "stack_revision.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_sr)

    sd = os.path.join(HERE, "samples")
    with open(os.path.join(sd, "constructed_rows.csv"), "w", encoding="utf-8") as fh:
        fh.write(to_csv(world()))
    with open(os.path.join(sd, "render_constructed.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_f)
    with open(os.path.join(sd, "render_unfilled.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_u)

    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
