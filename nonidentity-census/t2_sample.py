# SPDX-License-Identifier: CC0-1.0
"""
T2 -- BASE RATE. Stratified sample across fields, T1 applied, proportion
non-identity reported PER FIELD.

TWO PATHS, AND THEY HAVE DIFFERENT STATUS:

  --jsonl PATH   RUN AND TESTED. Reads {"id","field","abstract"} per line,
                 applies T1, aggregates. Exercised by --selftest against an
                 inline fixture, so the aggregation path is checked.

  --openalex     NEVER RUN. The network fetch was refused by this
                 environment's egress proxy on 2026-08-23 (see FINDINGS
                 T2-1). The code below is written and has never executed.
                 It is a reproduction command for an unblocked host, not a
                 tested path, and it is labelled that way at runtime too.

The eight fields are the work order's, not a choice made here. The OpenAlex
concept ids are a choice made here and are the weakest part of the fetch
path: a concept id is a lexical handle on a field, which is the operation
T1 exists to avoid, one level up at the sampling frame. Stated, not solved.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import json
import sys

import t1_predicate_unit as t1

FIELDS = ("economics", "sociology", "psychology", "ecology",
          "systems_control", "thermodynamics", "law",
          "organizational_theory")

# OpenAlex concept ids. Chosen here, not given by the work order.
OPENALEX_CONCEPT = {
    "economics": "C162324750",
    "sociology": "C144024400",
    "psychology": "C15744967",
    "ecology": "C18903297",
    "systems_control": "C50522688",
    "thermodynamics": "C97355855",
    "law": "C199539241",
    "organizational_theory": "C39389867",
}

FIXTURE = [
    {"id": "F-1", "field": "ecology",
     "abstract": "We show that populations declined across all sampled "
                 "sites."},
    {"id": "F-2", "field": "ecology",
     "abstract": "We report that the niche remained unoccupied for three "
                 "seasons."},
    {"id": "F-3", "field": "thermodynamics",
     "abstract": "We find that energy flux through the boundary layer "
                 "increases with surface roughness."},
    {"id": "F-4", "field": "economics",
     "abstract": "The market allocates scarce goods without a designer."},
    {"id": "F-5", "field": "economics",
     "abstract": "We find that firms with concentrated ownership reduce "
                 "investment following the reform."},
    {"id": "F-6", "field": "law",
     "abstract": "It increased sharply thereafter."},
]


def load_jsonl(path):
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            out.append((d["id"], d.get("field", "unrecorded"),
                        d["abstract"]))
    return out


def fetch_openalex(per_field=50):
    """NEVER RUN. See module docstring."""
    import urllib.request
    out = []
    for fld, cid in OPENALEX_CONCEPT.items():
        url = ("https://api.openalex.org/works?filter=concepts.id:%s"
               "&per-page=%d&select=id,abstract_inverted_index"
               % (cid, per_field))
        with urllib.request.urlopen(url, timeout=30) as fh:
            payload = json.load(fh)
        for w in payload.get("results", []):
            inv = w.get("abstract_inverted_index")
            if not inv:
                continue
            positions = {}
            for word, idxs in inv.items():
                for i in idxs:
                    positions[i] = word
            text = " ".join(positions[i] for i in sorted(positions))
            out.append((w["id"], fld, text))
    return out


def per_field(rows):
    """Proportions per field. UNDECIDABLE is its own arm (BOUNDARY D4)."""
    tally = {}
    for r in rows:
        f = r["field"]
        t = tally.setdefault(f, {t1.IDENTITY: 0, t1.NONIDENTITY: 0,
                                 t1.UNDECIDABLE: 0, "n": 0,
                                 t1.BY_PREDICATE: 0, t1.BY_TABLE: 0})
        t[r["label"]] += 1
        t["n"] += 1
        if r["decided_by"] in (t1.BY_PREDICATE, t1.BY_TABLE):
            t[r["decided_by"]] += 1
    return tally


def render(tally):
    print("%-22s %5s %6s %6s %6s   %s"
          % ("field", "n", "ident", "nonid", "undec", "pred/table"))
    for f in sorted(tally):
        t = tally[f]
        n = float(t["n"]) or 1.0
        print("%-22s %5d %6.3f %6.3f %6.3f   %d/%d"
              % (f, t["n"], t[t1.IDENTITY] / n, t[t1.NONIDENTITY] / n,
                 t[t1.UNDECIDABLE] / n, t[t1.BY_PREDICATE],
                 t[t1.BY_TABLE]))
    print()
    print("UNDECIDABLE is reported as its own arm and is not folded into")
    print("either side (BOUNDARY.md D4). pred/table is the T1-1 diagnostic:")
    print("the table column is the lexically-decided share.")


def selftest():
    fails = []
    rows = t1.report([(d["id"], d["field"], d["abstract"])
                      for d in FIXTURE])
    tally = per_field(rows)
    if set(tally) != {"ecology", "thermodynamics", "economics", "law"}:
        fails.append("field stratification lost: %r" % sorted(tally))
    if tally["law"][t1.UNDECIDABLE] != 1:
        fails.append("pronoun-subject fixture must land UNDECIDABLE")
    if tally["ecology"][t1.IDENTITY] != 1 or \
            tally["ecology"][t1.NONIDENTITY] != 1:
        fails.append("ecology fixture must split 1/1")
    if tally["economics"][t1.BY_PREDICATE] != 1:
        fails.append("the market fixture must be decided by predicate")
    total = sum(t["n"] for t in tally.values())
    if total != len(FIXTURE):
        fails.append("row count lost in aggregation: %d != %d"
                     % (total, len(FIXTURE)))
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--fixture" in argv:
        rows = t1.report([(d["id"], d["field"], d["abstract"])
                          for d in FIXTURE])
        print("T2 aggregation over the inline fixture (NOT a corpus, n=6)")
        render(per_field(rows))
        return 0
    if "--jsonl" in argv:
        path = argv[argv.index("--jsonl") + 1]
        rows = t1.report(load_jsonl(path))
        render(per_field(rows))
        return 0
    if "--openalex" in argv:
        sys.stderr.write(
            "NOTE: this path has never been executed. It was written after "
            "the fetch was refused by this environment's egress proxy. "
            "Treat a first run as untested code.\n")
        rows = t1.report(fetch_openalex())
        render(per_field(rows))
        return 0
    print(__doc__.strip())
    print("\nusage: t2_sample.py [--selftest | --fixture | "
          "--jsonl PATH | --openalex]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
