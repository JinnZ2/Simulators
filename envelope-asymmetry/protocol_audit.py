#!/usr/bin/env python3
"""Reads PROTOCOL.md against the instrument built to it, on constructed
records labelled so, and on the protocol's own text. Every number in
CLAIM_TABLE.md is computed here. No document is coded; nothing is a
statement about any vendor, filing or regime.
Refuses --selftest (checks live in selftest_env.py).
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "claim-record"))
import envelope_score as ES  # noqa: E402
import record as CR  # noqa: E402

PROTOCOL = os.path.join(HERE, "PROTOCOL.md")
HOST_PROBE = {"www.cac.gov.cn": "000 (no response)", "probed": "2026-09-04T17:45Z, one CONNECT"}

# E1-E6 read against claim-record's seven fields: a declared map.
MARKER_TO_RECORD = {
    "E1": ("domain_of_validity", "full"),
    "E2": ("domain_of_validity", "partial: outside_this names what is untested, not what is validated-against"),
    "E3": ("instrument", "partial: the instrument block describes the reading's own drift and bias, not the system's failure shape"),
    "E4": ("clock", "full: next_check is derived from a time constant and a coupling"),
    "E5": ("measurement", "full: an interval, never a point without basis"),
    "E6": (None, "no field"),
}


def row(doc_id, arm, score_markers, words, absent=False, pair=None, coder="c1", period="P1", inferable=None):
    r = {"doc_id": doc_id, "arm": arm, "vendor": "constructed", "host_domain": "constructed",
         "doc_type": "constructed", "doc_words": words, "structural_absence": absent, "coder": coder,
         "pair_id": pair, "filing_period": period, "domain_inferable": inferable}
    for i, m in enumerate(ES.MARKERS):
        r[m] = 0 if absent else score_markers[i]
    r["envelope_score"] = sum(r[m] for m in ES.MARKERS)
    return r


def kappa_vs_percent():
    """CONSTRUCTED double-coding, 20 documents. (a) both coders score E6
    absent on 19 and disagree on one; (b) both coders score everything
    absent on all 20."""
    ones = (1, 1, 1, 1, 1, 0)
    a = [row("d%d" % i, "A", ones, 500, coder="c1") for i in range(20)]
    b = [row("d%d" % i, "A", ones, 500, coder="c2") for i in range(20)]
    b[0] = row("d0", "A", (1, 1, 1, 1, 1, 1), 500, coder="c2")
    agr_a = ES.agreement(a + b)
    zero = (0, 0, 0, 0, 0, 0)
    c = [row("z%d" % i, "A", zero, 500, coder="c1") for i in range(20)] + [row("z%d" % i, "A", zero, 500, coder="c2") for i in range(20)]
    agr_c = ES.agreement(c)
    return {"one_disagreement": {"E6_percent": agr_a["per_marker"]["E6"]["percent"], "E6_kappa": agr_a["per_marker"]["E6"]["kappa"],
                                 "gate_percent": ES.gate(agr_a, "percent"), "gate_kappa_pooled": ES.gate(agr_a, "kappa")},
            "all_absent": {"percent": agr_c["percent"], "kappa": agr_c["kappa"], "gate_kappa": ES.gate(agr_c, "kappa")}}


def structural_absence_flip():
    """CONSTRUCTED 30 pairs: A and B identical on 20, B structurally
    absent on 10. The two accountings the instrument prints."""
    rows = []
    for i in range(30):
        rows.append(row("a%d" % i, "A", (1, 1, 1, 0, 0, 0), 800, pair=i))
        rows.append(row("b%d" % i, "B", (1, 1, 1, 0, 0, 0), 800, pair=i, absent=(i < 10)))
    t = ES.test1(rows)
    return {"all_pairs": (t["all_pairs"]["mean_diff"], t["all_pairs"]["reading"]),
            "documents_only": (t["documents_only"]["mean_diff"], t["documents_only"]["reading"]),
            "absence_rate": t["structural_absence_rate_B"]}


def e6_flat_two_ways():
    """CONSTRUCTED: A > B by two markers; E6 flat at 0 in one world and
    flat at 1 in the other."""
    out = {}
    for flat in (0, 1):
        rows = []
        for i in range(30):
            rows.append(row("a%d" % i, "A", (1, 1, 1, 0, 0, flat), 800, pair=i))
            rows.append(row("b%d" % i, "B", (1, 0, 0, 0, 0, flat), 800, pair=i))
        out["E6_flat_at_%d" % flat] = ES.test1(rows)["all_pairs"]["reading"]
    return out


def per_1000_inversion():
    """CONSTRUCTED pair: short document with two markers against a long
    one with all six. Primary and secondary outcomes rank them oppositely."""
    short = row("s", "B", (1, 1, 0, 0, 0, 0), 60)
    long_ = row("l", "A", (1, 1, 1, 1, 1, 1), 3000)
    return {"short": (short["envelope_score"], ES.per_1000(short)), "long": (long_["envelope_score"], ES.per_1000(long_)),
            "primary_prefers_long": long_["envelope_score"] > short["envelope_score"],
            "secondary_prefers_short": ES.per_1000(short) > ES.per_1000(long_)}


def template_kill():
    """CONSTRUCTED 100 filings, identical fields: the zero-variance kill,
    and the same property read from one record."""
    rows = [row("f%d" % i, "A" if i < 50 else "B", (1, 0, 0, 0, 0, 0), 300) for i in range(100)]
    t = ES.test2(rows)
    one = ES.test2([row("f0", "A", (1, 0, 0, 0, 0, 0), 300), row("f1", "B", (1, 0, 0, 0, 0, 0), 300)])
    return {"n100_zero_variance": t["zero_variance"], "n100_reading": t["reading"], "n2_zero_variance": one["zero_variance"]}


def marker_map():
    fields = CR.FIELDS
    out = {}
    for m, (f, note) in MARKER_TO_RECORD.items():
        out[m] = {"record_field": f, "exists": (f in fields) if f else False, "note": note}
    return {"record_fields": list(fields), "map": out, "markers_without_field": [m for m, v in out.items() if not v["exists"]]}


def compressed_block():
    """The protocol ends with a compressed restatement of itself. What
    the full text carries that the restatement drops."""
    text = open(PROTOCOL, encoding="utf-8").read()
    full, tail = text.split("ENVELOPE SCORE — code each document 0/1 per marker, sum 0-6")
    probes = {"T1 doc_words covariate": "doc_words", "T2 structural absence": "structural_absence",
              "T3 blinding": "strip vendor", "T4 pre-registration": "pre-register", "re-target on template kill": "Re-target",
              "kill-but-informative": "informative", "section 4 implications": "model tier", "section 5 scope": "intentions",
              "record schema": "\"doc_id\"", "inter-rater rule": "agreement"}
    return {k: {"in_full": v in full, "in_compressed": v in tail} for k, v in probes.items()}


def domain_of_arm_A_in_readout_count():
    """Arm A is defined by 'existing standards + return channel'; the
    tree's readout-count schema records exactly whether a channel
    returns. Existence of the fields, not a value."""
    sys.path.insert(0, os.path.join(ROOT, "readout-count"))
    import readout_count as RC
    return {"fields": [f for f in RC.FIELDS if "return" in f], "positions_returning": "positions_returning" in RC.FIELDS}


def render():
    L = ["envelope-asymmetry protocol audit"]
    L.append("kappa vs percent on constructed double-coding: %s" % kappa_vs_percent())
    L.append("structural absence, two accountings: %s" % structural_absence_flip())
    L.append("E6 flat two ways: %s" % e6_flat_two_ways())
    L.append("per-1000-words inversion: %s" % per_1000_inversion())
    L.append("template kill: %s" % template_kill())
    mm = marker_map()
    L.append("markers against claim-record fields %s: without a field %s" % (mm["record_fields"], mm["markers_without_field"]))
    for m, v in mm["map"].items():
        L.append("  %s -> %-20s %s" % (m, v["record_field"], v["note"]))
    L.append("compressed block against the full protocol:")
    for k, v in compressed_block().items():
        L.append("  %-30s full %-5s compressed %s" % (k, v["in_full"], v["in_compressed"]))
    L.append("arm A's 'return channel' in readout-count: %s" % domain_of_arm_A_in_readout_count())
    L.append("hosts: %s" % HOST_PROBE)
    L.append("rows coded: 0; no vendor documentation site or filing registry answers from here, and no row is invented")
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("protocol_audit has no selftest; run selftest_env.py", file=sys.stderr)
        sys.exit(2)
    print(render())
