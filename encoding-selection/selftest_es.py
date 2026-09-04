#!/usr/bin/env python3
"""Checks for encoding_selection.py. Known answers first, both
directions of every guard. Rows are CONSTRUCTED; nothing is a claim
about any reader or format.

    python3 encoding-selection/selftest_es.py
"""

import csv
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import encoding_selection as E  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def row(**kw):
    base = dict(reader_id="r1", reader_substrate="human", item="M1", format="F1",
                design="between", quantities_recovered="disproportion",
                dropped_axes_named="n", rank_given="", decline_reason="",
                response_text="constructed response")
    base.update(kw)
    return base


def to_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=E.FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


NATIVE = {"F1": "disproportion", "F2": "chain", "F3": "magnitude", "F4": "exclusion",
          "F5": "cross-domain shape", "F6": "sequence", "F7": "other"}
ALL6 = ["F1", "F2", "F3", "F4", "F5", "F6"]


def world(format_driven=True, consistent_rank=False, n_readers=12):
    """Between-subjects rows where recovery tracks the format (or the
    reader), plus within-subjects rankers who rank consistently (or not),
    plus two decliners."""
    rows = []
    qs = list(E.QUANTITIES)
    for i in range(n_readers):
        for k, f in enumerate(ALL6):
            rid = "b%d_%d" % (i, k)
            q = NATIVE[f] if format_driven else qs[i % len(qs)]
            named = "y" if f in E.TABLE_CLASS else ("n" if f == "F6" else "partial")
            rows.append(row(reader_id=rid, format=f, quantities_recovered=q, dropped_axes_named=named,
                            reader_substrate="human" if i % 2 else "model:v%d" % (i % 3)))
    order = list(ALL6)
    for i in range(6):
        rk = list(order) if consistent_rank else [order[(j * 5 + i * 2) % 6] for j in range(6)]
        if not consistent_rank:
            rk = sorted(set(rk), key=rk.index)
            rk += [f for f in order if f not in rk]
        for f in ALL6:
            named = "y" if f in E.TABLE_CLASS else ("n" if f == "F6" else "partial")
            rows.append(row(reader_id="w%d" % i, format=f, design="within",
                            quantities_recovered=NATIVE[f] if format_driven else qs[i % len(qs)],
                            dropped_axes_named=named, rank_given=";".join(rk)))
    for i in range(2):
        for f in ALL6:
            named = "y" if f in E.TABLE_CLASS else ("n" if f == "F6" else "partial")
            rows.append(row(reader_id="d%d" % i, format=f, design="within",
                            rank_given="declined", decline_reason="each carries different information",
                            dropped_axes_named=named,
                            quantities_recovered=NATIVE[f] if format_driven else qs[i % len(qs)]))
    return rows


def main():
    print("selftest_es")

    # ---- known answers: Kendall's W
    check("W = 1 on identical rankings", E.kendall_w([["a", "b", "c"]] * 3) == 1.0)
    hand = [["a", "b", "c"], ["a", "b", "c"], ["b", "a", "c"]]
    check("W on the hand case is 168/216", abs(E.kendall_w(hand) - 168 / 216) < 1e-12)
    check("W None with one ranker", E.kendall_w([["a", "b"]]) is None)
    check("W None with one item", E.kendall_w([["a"], ["a"]]) is None)
    w, p = E.w_null([["a", "b", "c", "d", "e", "f"]] * 6, perms=500)
    check("identical rankings: W 1.0 and p small under the null", w == 1.0 and p < 0.05)
    check("jaccard distance: identical 0, disjoint 1, empty pair 0",
          E.jaccard_distance(["a"], ["a"]) == 0.0 and E.jaccard_distance(["a"], ["b"]) == 1.0
          and E.jaccard_distance([], []) == 0.0)
    check("material ratio is 24", E.material_ratio() == 24.0)

    # ---- constructed worlds, both directions
    wf = E.validate_rows(world(format_driven=True, consistent_rank=False))
    wr = E.validate_rows(world(format_driven=False, consistent_rank=True))
    r1f, r1r = E.h1(wf), E.h1(wr)
    check("inconsistent rankers: H1 not falsified", r1f["verdict"].startswith("H1 not"))
    check("consistent rankers: W 1.0, H1 FALSE", r1r["W"] == 1.0 and r1r["verdict"].startswith("H1 FALSE"))
    check("declines counted apart: 2 in both worlds", r1f["declines"] == 2 and r1r["declines"] == 2)
    r2f, r2r = E.h2(wf), E.h2(wr)
    check("format-driven world: within 0, between > 0, H2 not falsified",
          r2f["within_mean"] == 0.0 and r2f["between_mean"] > 0 and r2f["verdict"].startswith("H2 not"))
    check("reader-driven world: within >= between, H2 FALSE", r2r["verdict"].startswith("H2 FALSE"))
    check("one reader across formats: spread in the format world, none in the reader world",
          r2f["one_reader_across_formats_mean"] > 0 and r2r["one_reader_across_formats_mean"] == 0.0)
    r3 = E.h3(wf)
    check("prose 0 vs table 1: H3 not falsified", r3["prose_rate"] == 0.0 and r3["table_rate"] == 1.0
          and r3["verdict"].startswith("H3 not"))
    flat = [dict(r, dropped_axes_named="y") for r in world()]
    check("equal rates: H3 FALSE", E.h3(E.validate_rows(flat))["verdict"].startswith("H3 FALSE"))
    check("H3 undetermined with an empty arm",
          E.h3(E.validate_rows([row(format="F1")]))["verdict"].startswith("undetermined"))
    pf = E.per_format(wf)
    check("per-format n and declines", pf["F1"]["n"] == 20 and pf["F1"]["rank_declines"] == 2 and pf["F7"]["n"] == 0)
    check("empty format rates are None, not 0", pf["F7"]["dropped_named_rate"] is None)

    # ---- rank pooling
    mixed = E.validate_rows([row(reader_id="a", format="F1", design="within", rank_given="F1;F2"),
                             row(reader_id="b", format="F1", design="within", rank_given="F1;F3")])
    check("rankers over different format sets are refused, not pooled",
          E.rankings(mixed)["refused"] is not None and E.h1(mixed)["verdict"].startswith("undetermined"))
    check("H1 undetermined with one ranker",
          E.h1(E.validate_rows([row(reader_id="a", format="F1", design="within",
                                    rank_given="F1;F2")]))["verdict"].startswith("undetermined"))

    # ---- schema refusals
    for bad, why in [({"format": "F8"}, "format outside F1..F7"),
                     ({"quantities_recovered": "vibes"}, "quantity outside P3 vocabulary"),
                     ({"reader_substrate": "model"}, "model without vendor"),
                     ({"rank_given": "F1;F1"}, "a rank with a repeat"),
                     ({"rank_given": "F1;F2"}, "a between-subjects row with a rank"),
                     ({"design": "within", "rank_given": ""}, "a within row with neither rank nor decline"),
                     ({"design": "within", "rank_given": "declined"}, "declined with no reason"),
                     ({"response_text": ""}, "no verbatim response")]:
        try:
            E.validate_rows([row(**bad)]); check("refuses " + why, False)
        except E.SchemaRefused:
            check("refuses " + why, True)
    try:
        E.validate_rows([]); check("refuses zero rows", False)
    except E.SchemaRefused:
        check("refuses zero rows", True)
    check("load_csv round-trips", len(E.load_csv(to_csv(world()))) == len(world()))
    check("quantities de-duplicated and sorted",
          E.validate_rows([row(quantities_recovered="chain;magnitude;chain")])[0]["quantities_recovered"]
          == ["chain", "magnitude"])

    # ---- encodings check, both directions
    good = {"M1": {f: {"text": "x", "carries": list(E.FACTS["M1"][:2]), "drops": list(E.FACTS["M1"][2:])}
                   for f in E.FORMATS},
            "M2": {f: {"text": "x", "carries": list(E.FACTS["M2"]), "drops": []} for f in E.FORMATS}}
    ce = E.check_encodings(good)
    check("a complete encodings file passes with no refusal", ce["refused"] == [] and ce["items"]["M1"]["missing"] == [])
    added = {"M1": {"F1": {"text": "x", "carries": ["a new fact"], "drops": []}}}
    ce2 = E.check_encodings(added)
    check("an added fact is refused", any("not in the item's list" in m for m in ce2["refused"]))
    check("missing formats listed", len(ce2["items"]["M1"]["missing"]) == 6)
    both = {"M2": {"F6": {"text": "x", "carries": ["zero returns"], "drops": ["zero returns"]}}}
    check("carried-and-dropped refused", any("carried and dropped" in m for m in E.check_encodings(both)["refused"]))
    notext = {"M2": {"F6": {"text": "", "carries": [], "drops": []}}}
    check("an encoding with no text is refused", any("no text" in m for m in E.check_encodings(notext)["refused"]))

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "encoding_selection.py"), "--selftest"],
                        capture_output=True).returncode
    check("instrument refuses --selftest with rc 2", rc == 2)
    out_u = E.render(None)
    out_f = E.render(wf, good)
    check("unfilled render screens clean", not no_severity.hits(out_u))
    check("constructed render screens clean", not no_severity.hits(out_f))
    check("screen fires on a planted word", bool(no_severity.hits(out_f + "\nthis is wrong\n")))
    check("every [CHOICE] printed", all("[CHOICE %d]" % i in out_u for i in (1, 2, 3, 4)))
    src = open(os.path.join(HERE, "encoding_selection.py"), encoding="utf-8").read()
    check("no author section", "Author" not in src)
    check("no statistics library", not any(m in src for m in ("import numpy", "import scipy", "import statistics")))

    sd = os.path.join(HERE, "samples")
    with open(os.path.join(sd, "constructed_rows.csv"), "w", encoding="utf-8") as fh:
        fh.write(to_csv(world()))
    import json
    with open(os.path.join(sd, "constructed_encodings.json"), "w", encoding="utf-8") as fh:
        json.dump(good, fh, indent=1)
    with open(os.path.join(sd, "render_constructed.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_f)
    with open(os.path.join(sd, "render_unfilled.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_u)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
