#!/usr/bin/env python3
"""Checks for pilot_loop.py. CC0, stdlib only.

Every guard is exercised in both directions where it has two. A scanner only
ever seen silent has not been shown to discriminate, and a state only ever seen
unused has not been shown to be reachable.
"""

from __future__ import annotations

import ast
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import frame_audit
import pilot_loop as P

CHECKS = 0
FAILED = 0


def ck(cond, label):
    global CHECKS, FAILED
    CHECKS += 1
    if not cond:
        FAILED += 1
        print("FAIL  %s" % label)
    else:
        print("ok    %s" % label)


def run() -> int:
    global CHECKS, FAILED
    CHECKS = 0
    FAILED = 0

    print("-- monetary scanner: the run fails if the model carries the frame")
    scan = P.monetary_scan()
    ck(scan["clean"], "pilot_loop.py is clean (hits: %s)"
       % [h["name"] for h in scan["hits"]])
    ck(scan["prose_chars_not_scanned"] > 0,
       "prose is counted on its own line, not silently dropped")

    tmp = tempfile.mkdtemp(prefix="pilot_scan_")
    planted = os.path.join(tmp, "planted.py")
    io.open(planted, "w", encoding="utf-8").write(
        "from dataclasses import dataclass\n"
        "@dataclass\nclass Thing:\n    price: int\n")
    ck(not P.monetary_scan(planted)["clean"],
       "the scanner fires on a planted monetary field DEFINITION")

    accessed = os.path.join(tmp, "accessed.py")
    io.open(accessed, "w", encoding="utf-8").write(
        "def f(thing):\n    return thing.price\n")
    ck(P.monetary_scan(accessed)["clean"],
       "and stays silent on an attribute ACCESS, the declared narrowing")

    ck(P.monetary_scan(os.path.join(HERE, "frame_audit.py"))["clean"] is False,
       "the lexicon file itself is not clean, which is the use-mention "
       "case and the reason the model is a different file")

    print("\n-- the exemption list: declared, every entry cites, usage measured")
    ck(len(P.SCANNER_EXEMPTIONS) > 0, "an exemption list exists")
    for entry in P.SCANNER_EXEMPTIONS:
        ck(len(entry) == 3 and all(str(x).strip() for x in entry),
           "exemption %r carries a word, a source id and a note" % (entry[0],))
        ck(entry[1] in ("S-NIMS3", "S-ICS-ORG", "S-ICS-REV", "S-ICS-FORMS"),
           "exemption %r cites a source id in SOURCES.md" % (entry[0],))
    ck(scan["exemptions_used"] == 0,
       "no exemption is used in this build, and the zero is reported "
       "rather than the list being assumed load-bearing")

    print("\n-- provenance states")
    states = set(e.provenance for e in P.ICS_STRUCTURE)
    for want in (P.Provenance.CITED, P.Provenance.ASSUMED, P.Provenance.CARRIED,
                 P.Provenance.NOT_ACTIVATED):
        ck(want in states, "%s is used by the structure" % want.value)
    ck(P.Provenance.EXCLUDED not in states,
       "EXCLUDED is unused in this build")

    try:
        P.Element("E-X", "t", P.Provenance.EXCLUDED, None, False, "n")
        ck(False, "EXCLUDED without a reason must raise")
    except ValueError:
        ck(True, "EXCLUDED without excluded_by and omitted raises")
    ok = P.Element("E-X", "t", P.Provenance.EXCLUDED, None, False, "n",
                   excluded_by="a named requirement", omitted="what was left out")
    ck(ok.excluded_by and ok.omitted, "EXCLUDED with both fields constructs")

    try:
        P.Element("E-Y", "t", P.Provenance.CITED, None, False, "n")
        ck(False, "CITED without a source must raise")
    except ValueError:
        ck(True, "CITED without a source id raises")

    print("\n-- EXCLUDED, when used, reports at the TOP")
    saved = P.ICS_STRUCTURE
    try:
        P.ICS_STRUCTURE = saved + (ok,)
        report = P.provenance_report()
        first = report.strip().split("\n")[0]
        ck(first.startswith("EXCLUDED ELEMENTS: 1"),
           "the excluded count is the first line (got %r)" % first[:40])
        ck("a named requirement" in report and "what was left out" in report,
           "and it names the requirement and what was omitted")
    finally:
        P.ICS_STRUCTURE = saved
    ck(P.provenance_report().strip().split("\n")[0]
       .startswith("EXCLUDED ELEMENTS: 0"),
       "with none used, the zero is printed rather than the section omitted")

    print("\n-- citation depth: unverified everywhere, and said so")
    cited = [e for e in P.ICS_STRUCTURE if e.provenance is P.Provenance.CITED]
    ck(cited, "the structure carries cited elements")
    ck(all(not e.section_verified for e in cited),
       "every cited element is section_verified False")
    ck(all(e.source_id for e in cited), "and every one names a source")
    src = io.open(os.path.join(HERE, "SOURCES.md"), encoding="utf-8").read()
    for e in cited:
        ck(e.source_id in src, "%s's source %s appears in SOURCES.md"
           % (e.id, e.source_id))
    ck("NOT ANSWERABLE FROM THE BUILDING SESSION" in src,
       "the NIMS edition question is recorded as unanswered, not answered")

    print("\n-- conditional activation, not deletion")
    fin = [e for e in P.ICS_STRUCTURE if e.id == "E-FIN"]
    ck(len(fin) == 1, "Finance/Administration is present in the structure")
    ck(fin[0].provenance is P.Provenance.NOT_ACTIVATED,
       "and is NOT_ACTIVATED rather than EXCLUDED")
    ck(fin[0].activation is P.Activation.NOT_ACTIVATED,
       "and carries the non-activated activation state")
    ck(fin[0].source_id == "S-ICS-ORG", "and cites the doctrine that says so")
    intel = [e for e in P.ICS_STRUCTURE if e.id == "E-INT"]
    ck(intel and intel[0].provenance is P.Provenance.NOT_ACTIVATED,
       "Intelligence/Investigations is represented the same way")

    print("\n-- the loop closes, and returns rather than raising")
    base = P.run_loop(P.load_params(os.path.join(HERE, "params",
                                                 "baseline.json")))
    ck(base.assignments, "baseline produces assignments")
    ck(base.unmet, "baseline produces UNMET as a value")
    ck(base.untyped, "baseline produces UNTYPED as a value")
    ck(all(isinstance(u, P.Unmet) for u in base.unmet),
       "every unmet is an Unmet record, not an exception")
    ck(all(isinstance(u, P.Untyped) for u in base.untyped),
       "every untyped is an Untyped record, not an exception")

    print("\n-- UNMET signature is (need, quantity, reason), per the dispatch")
    keys = set(base.unmet[0].to_dict().keys())
    ck({"need", "quantity", "reason"} <= keys,
       "the record carries need, quantity and reason (got %s)" % sorted(keys))
    ck({"resource", "reason"} <= set(base.untyped[0].to_dict().keys()),
       "UNTYPED carries resource and reason")

    print("\n-- lag has three stages and they order")
    for a in base.assignments:
        ck(a.t_declared <= a.t_assigned <= a.t_arrived,
           "%s: declared <= assigned <= arrived" % a.need_node)
    ck(any(a.lag_to_arrival() > a.lag_to_assignment()
           for a in base.assignments),
       "arrival lag exceeds assignment lag where distance is non-zero")

    print("\n-- an absent lag is None, never a zero")
    idle = [n for n in base.lag_by_node
            if base.lag_by_node[n]["assignments"] == 0]
    ck(idle, "some node received nothing in the baseline")
    for n in idle:
        ck(base.lag_by_node[n]["lag_to_arrival_max"] is None,
           "%s reports None rather than 0 for a lag nobody measured" % n)

    print("\n-- span of control bounds assignments")
    span = P.run_loop(P.load_params(os.path.join(HERE, "params",
                                                 "span_limited.json")))
    per_holder = {}
    for a in span.assignments:
        per_holder[a.capacity_node] = per_holder.get(a.capacity_node, 0) + 1
    for holder in per_holder:
        ck(per_holder[holder] <= span.span_limits.get(holder, 99),
           "%s made no more assignments than its span limit" % holder)
    ck(any(u.reason is P.UnmetReason.SPAN_OF_CONTROL_REACHED
           for u in span.unmet),
       "and the need it could not reach returns SPAN_OF_CONTROL_REACHED")

    print("\n-- a scenario with no typing catalog types nothing, and says why")
    nc = P.run_loop(P.load_params(os.path.join(HERE, "params",
                                               "no_catalog.json")))
    ck(nc.untyped, "no_catalog returns UNTYPED")
    ck(all(u.reason is P.UntypedReason.CATALOG_ABSENT for u in nc.untyped),
       "with CATALOG_ABSENT as the reason, not a guess at a type")
    ck(not nc.assignments, "and nothing is assigned on untyped resources")

    print("\n-- the scenarios carry no money frame either")
    for name in sorted(os.listdir(os.path.join(HERE, "params"))):
        if not name.endswith(".json"):
            continue
        text = io.open(os.path.join(HERE, "params", name),
                       encoding="utf-8").read()
        r = frame_audit.audit(text.replace("_", " "))
        ck(not r.hits, "params/%s carries no money-frame token (%s)"
           % (name, [h.token for h in r.hits]))

    print("\n-- the model reaches no network and runs nothing")
    tree = ast.parse(io.open(os.path.join(HERE, "pilot_loop.py"),
                             encoding="utf-8").read())
    bad = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            mod = getattr(n, "module", None) or ""
            for alias in n.names:
                nm = (mod or alias.name).split(".")[0]
                if nm in ("socket", "urllib", "http", "requests",
                          "subprocess", "ftplib"):
                    bad.append(nm)
    ck(not bad, "no network or subprocess import (got %s)" % bad)

    print("\n-- json round trip")
    d = base.to_dict()
    ck(json.loads(json.dumps(d))["scenario"] == "baseline",
       "the result serialises")
    ck(len(d["structure"]) == len(P.ICS_STRUCTURE),
       "and carries the full structure with its provenance")

    print("\nchecks: %d   failed: %d" % (CHECKS, FAILED))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if FAILED == 0 else "FAIL", CHECKS, FAILED))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
