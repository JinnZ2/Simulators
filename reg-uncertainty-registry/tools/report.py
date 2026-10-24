#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
report.py -- the four documents that state numbers, rendered from the
registry so none of them carries a typed count.

    REVISED_REPORT.md      REVISED_REPORT.template.md with every {key}
                           filled from values(); the template itself carries
                           no bare count (validate.py lints it)
    CHANGE_LOG.md          every CHANGE object, in order, with its NCR
    schema/QA_MAPPING.md   the nuclear-QA terms the work order borrows,
                           each against the clause it borrows from and that
                           clause's ledger state

    CLAIM_TABLE.md         CLAIM_TABLE.template.md, the same way

validate.py re-renders all four and compares bytes, and lints both templates.

Usage   python3 tools/report.py           write the four files
        python3 tools/report.py --keys    list every template key and value
Refuses --selftest (checks run in tools/validate.py). Stdlib only.
"""

import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reglib  # noqa: E402
import stats  # noqa: E402
import symmetry  # noqa: E402
import chain  # noqa: E402
import gaps  # noqa: E402

FOLDER = reglib.FOLDER
REPORT = os.path.join(FOLDER, "REVISED_REPORT.md")
TEMPLATE = os.path.join(FOLDER, "REVISED_REPORT.template.md")
CLAIMS = os.path.join(FOLDER, "CLAIM_TABLE.md")
CLAIMS_TEMPLATE = os.path.join(FOLDER, "CLAIM_TABLE.template.md")
TEMPLATED = ((REPORT, TEMPLATE), (CLAIMS, CLAIMS_TEMPLATE))
CHANGELOG = os.path.join(FOLDER, "CHANGE_LOG.md")
QA = os.path.join(FOLDER, "schema", "QA_MAPPING.md")

TALLY_KEYS = ("below", "conform", "exceeds", "over_restrictive", "statute")


def _fmt(v):
    if isinstance(v, float):
        return ("%.4f" % v).rstrip("0").rstrip(".") if abs(v) < 1 else "%.2f" % v
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    return str(v)


def values(reg):
    O = reg.objects
    v = {}
    sample = stats.coded_sample(O)
    v["n.sample"] = len(sample)
    v["n.objects"] = len(O)
    v["n.edges"] = len(reg.edges)
    for t in ("EVIDENCE", "SOURCE", "ACTOR", "AUTHORITY", "CONFLICT", "NCR", "CHANGE",
              "REVERSAL", "OUTCOME", "ENDPOINT_ABSENCE", "SUBSTANCE", "ENDPOINT"):
        v["n.%s" % t.lower()] = len(reg.of(t))
    v["n.decision"] = len(reg.of("DECISION"))
    v["n.non_decision"] = len(reg.of("NON_DECISION"))
    v["n.sample_non_decision"] = sum(1 for o in sample if o["type"] == "NON_DECISION")
    # ledger
    led = [o for o in reg.of("EVIDENCE") if o["verification"].get("ledger_row")]
    v["led.rows"] = len(led)
    v["led.searched"] = sum(1 for o in led if o["verification"]["reached"] != "N")
    for st in ("VERIFIED", "CORRECTED", "NOT_FOUND", "UNREACHABLE"):
        v["led.%s" % st.lower()] = sum(1 for o in led if o["verification"]["state"] == st)
    v["pins.inputs"] = reglib.pinned_count()
    # annex
    mm = stats.annex_reproduction(O)
    v["annex.mismatches"] = len(mm)
    # tallies
    for name, variant in (("rus02", stats.RUS02), ("rus03", stats.RUS03)):
        for basis in ("annex", "action", "outcome"):
            if name == "rus03" and basis == "annex":
                continue
            for side in ("src", "reg"):
                t = stats.tally_of(sample, basis, side, variant)
                p = "t.%s.%s.%s" % (name, basis, side)
                for k in TALLY_KEYS + ("over_reachable", "over_possible", "reading", "n"):
                    v["%s.%s" % (p, k)] = t[k]
                v["%s.over_rows" % p] = ", ".join(t["over_rows"]) or "none"
    # R8 rows
    for o in stats.frame(O, "R8"):
        for k in ("rus02.action.src", "rus03.action.src"):
            g = o["grades"][k]
            p = "r8.%s.%s" % (o["id"], k.split(".")[0])
            v[p + ".floor"] = g["floor"]
            v[p + ".actual"] = g["actual"]
            v[p + ".status"] = g["status"]
            v[p + ".gap"] = g["gap"]
            v[p + ".r6"] = g.get("r6", "R6 not applied")
    # sweep
    for r in stats.sweep(O):
        p = "sw.%s" % r["variant"]
        v[p + ".published"] = "/".join(str(x) for x in r["published"]) if r["published"] else "none"
        v[p + ".computed"] = "/".join(str(x) for x in r["computed"])
        v[p + ".below"] = r["computed"][0]
        v[p + ".reproduces"] = {True: "reproduces", False: "does not reproduce", None: "registry variant"}[r["reproduces"]]
        v[p + ".over_possible"] = r["over_possible"]
        v[p + ".over_reachable"] = r["over_reachable"]
        v[p + ".reading"] = r["reading"]
        v[p + ".u3"] = "/".join(r["u3_row"]) if r["u3_row"] else "standard"
    sv = stats.statement_values(O)
    for k, x in sv.items():
        v["st.%s" % k] = x
    # bivariate
    for fr in ("source_frame", "decision_only"):
        for rule in ("L", "S"):
            b = stats.bivariate(O, rule, fr)
            p = "bv.%s.%s" % (fr, rule)
            v[p + ".conc"] = "%d/%d" % b["concentrated"]
            v[p + ".diff"] = "%d/%d" % b["diffuse"]
            v[p + ".p"] = "%.4f" % b["p"]
            v[p + ".reading"] = b["reading"]
            v[p + ".n"] = b["n"]
    # forcing
    f = stats.forcing(O)
    v["fc.list"] = ", ".join(f["list"])
    v["fc.n"] = len(f["list"])
    v["fc.forced"] = len(f["forced"])
    v["fc.discretionary"] = ", ".join(f["discretionary"])
    v["fc.all_forced"] = f["all_forced"]
    v["fc.all_n"] = f["all_n"]
    # c2
    c = stats.c2_counts(O)
    for k, x in c.items():
        v["c2.%s" % k] = x
    # mirrors
    m = stats.mirrors(O)
    v["mi.n"], v["mi.divergent"], v["mi.ge2"] = m["n"], m["divergent"], m["ge2"]
    # reversals
    for anchor in ("2016", "1970"):
        rv = stats.reversals(O, anchor)
        p = "rv.%s" % anchor
        for g in ("restrictive_to_permissive", "permissive_to_restrictive"):
            ts = [t for _, t, _ in rv["groups"][g]]
            v["%s.%s.n" % (p, g)] = len(ts)
            v["%s.%s.median" % (p, g)] = "%.2f" % statistics.median(ts)
            v["%s.%s.times" % (p, g)] = ", ".join("%.2f" % t for t in sorted(ts))
        v[p + ".U"] = "%.1f" % rv["mann_whitney"]["U"]
        v[p + ".p"] = "%.4f" % rv["mann_whitney"]["p_two_sided"]
        v[p + ".arrangements"] = rv["mann_whitney"]["enumerated"]
        v[p + ".toward"] = ", ".join(rv["toward_permissive_from_list"])
    v["rv.n"] = len(reg.of("REVERSAL"))
    # symmetry
    cases = [o for o in reg.cases() if o["frame"] in ("A", "B", "C", "D", "E") and "consequence" in o]
    for side in ("src", "reg"):
        ps = symmetry.pairs(cases, side)
        v["sym.%s.pairs" % side] = len(ps)
        v["sym.%s.fail" % side] = sum(1 for p in ps if p["fail"])
        v["sym.%s.fail_mixed_group" % side] = sum(1 for p in ps if p["fail"] and p["group_a"] != p["group_b"])
    # chain flags
    coded2 = chain.second_coded()
    graded = [o for o in reg.cases() if o["frame"] in ("A", "B", "C", "D", "E", "R8")]
    tally = {}
    for o in graded:
        for x in chain.flags(reg, o["id"], coded2):
            tally[x.split()[0]] = tally.get(x.split()[0], 0) + 1
    v["ch.graded"] = len(graded)
    for k in ("ONE_CODER", "ONE_SOURCE", "NO_LOCATED_SOURCE", "AUTHORITY_GAP", "ORIGINATOR_ONLY"):
        v["ch.%s" % k.lower()] = tally.get(k, 0)
    # gaps
    g = gaps.collect(reg)
    for k, rows in g.items():
        v["gap.%s" % k] = len(rows)
    # NCRs
    ncr = reg.of("NCR")
    for d in ("ACCEPT", "REJECT", "MODIFY"):
        v["ncr.%s" % d.lower()] = sum(1 for x in ncr if x["disposition"] == d)
    v["ncr.open"] = sum(1 for x in ncr if x["state"] == "OPEN")
    v["ncr.review"] = sum(1 for x in ncr if x["origin"] != "AUDIT_WO-REG-1")
    v["ncr.audit"] = sum(1 for x in ncr if x["origin"] == "AUDIT_WO-REG-1")
    v["ncr.open_ids"] = ", ".join(sorted(x["id"] for x in ncr if x["state"] == "OPEN"))
    # graded approach: does verification scale with tier?
    for tier in ("T1", "T2", "T3"):
        tc = [o for o in graded if o.get("rigor_tier") == tier]
        rows = set()
        for o in tc:
            for e in reg.in_edges(o["id"], "supports"):
                x = reg.get(e["from"])
                if x["type"] == "EVIDENCE" and x["verification"].get("ledger_row"):
                    rows.add(x["id"])
        loc = sum(1 for r in rows if reg.get(r)["verification"]["state"] in ("VERIFIED", "CORRECTED"))
        v["tier.%s.cases" % tier] = len(tc)
        v["tier.%s.rows" % tier] = len(rows)
        v["tier.%s.located" % tier] = loc
        v["tier.%s.share" % tier] = ("%.2f" % (loc / float(len(rows)))) if rows else "none"
    # second coder
    k = stats.second_coder(O)
    v["k2.state"] = k["state"]
    v["k2.reason"] = k.get("reason", "")
    # text checks
    v["text.r1_found"] = sum(1 for *_, n in stats.text_checks(O) if n == 1)
    v["text.r1_n"] = len(stats.TEXT_CHECKS)
    # statement table
    rows = ["| id | NCR | source | as stated | registry value |", "|---|---|---|---|---|"]
    for o in sorted((x for x in reg.of("EVIDENCE") if x["kind"] == "statement"), key=lambda x: x["id"]):
        ncrs = [n["id"] for n in ncr if o["id"] in n["statements"]]
        rows.append("| %s | %s | %s line %d | %s | %s |" % (
            o["id"], ", ".join(ncrs), os.path.basename(o["located"]["path"]), o["located"]["line"],
            o["statement"].replace("|", "\\|").replace("\n", " "), o["registry_value"].replace("|", "\\|")))
    v["table.statements"] = "\n".join(rows)
    # NCR table
    rows = ["| NCR | origin | items | disposition | state | changes |", "|---|---|---|---|---|---|"]
    for x in sorted(ncr, key=lambda x: (x["origin"], int(re.sub(r"\D", "", x["id"]) or 0))):
        rows.append("| %s | %s | %s | %s | %s | %s |" % (
            x["id"], x["origin"], ", ".join(x["item"]), x["disposition"], x["state"],
            ", ".join(x["changes"]) or "-"))
    v["table.ncr"] = "\n".join(rows)
    # sweep table
    rows = ["| variant | published | computed | | U3 row | over_reachable | over_possible | reading |",
            "|---|---|---|---|---|---|---|---|"]
    for r in stats.sweep(O):
        p = "sw.%s" % r["variant"]
        rows.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["variant"], v[p + ".published"], v[p + ".computed"], v[p + ".reproduces"],
            v[p + ".u3"], v[p + ".over_reachable"], v[p + ".over_possible"], v[p + ".reading"]))
    v["table.sweep"] = "\n".join(rows)
    # tally table
    rows = ["| standard | basis | C_restrict | below | conform | exceeds | over | statute | over_reachable | over_possible | one-directional reading |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name in ("rus02", "rus03"):
        for basis in ("annex", "action", "outcome"):
            if name == "rus03" and basis == "annex":
                continue
            for side in ("src", "reg"):
                p = "t.%s.%s.%s" % (name, basis, side)
                rows.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                    "RUS-0.2" if name == "rus02" else "RUS-0.3", basis, side,
                    v[p + ".below"], v[p + ".conform"], v[p + ".exceeds"], v[p + ".over_restrictive"],
                    v[p + ".statute"], v[p + ".over_reachable"], v[p + ".over_possible"], v[p + ".reading"]))
    v["table.tallies"] = "\n".join(rows)
    rows = ["| basis | variant | below | conform | exceeds | over | statute | over_possible | one-directional reading | R6_SELF_SEALING rows |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for r in stats.components(O):
        t = r["tally"]
        rows.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["basis"], r["variant"], t["below"], t["conform"], t["exceeds"], t["over_restrictive"],
            t["statute"], t["over_possible"], t["reading"], r["r6_self_sealing"]))
        v["cmp.%s.%s.below" % (r["basis"], r["variant"])] = t["below"]
        v["cmp.%s.%s.reading" % (r["basis"], r["variant"])] = t["reading"]
    v["table.components"] = "\n".join(rows)
    for basis in ("action", "outcome"):
        sa = stats.sub_alone(O, basis)
        v["sub.%s.floors" % basis] = len(sa["floors"])
        v["sub.%s.floor_rows" % basis] = ", ".join(sa["floors"]) or "none"
        v["sub.%s.statuses" % basis] = len(sa["statuses"])
    return {k: _fmt(x) for k, x in v.items()}


PLACEHOLDER = re.compile(r"\{([a-z][A-Za-z0-9_.+\-]*)\}")


def render(reg, tmpl, name="REVISED_REPORT.template.md"):
    vals = values(reg)
    def sub(m):
        k = m.group(1)
        if k not in vals:
            raise reglib.RegistryError("template key {%s} has no value" % k)
        return vals[k]
    body = PLACEHOLDER.sub(sub, tmpl)
    return ("<!-- GENERATED by tools/report.py from %s and registry/; "
            "do not edit -->\n" % name + body)


def render_changelog(reg):
    out = ["<!-- GENERATED by tools/report.py from registry/changes.json; do not edit -->",
           "# CHANGE LOG", "",
           "Every edit to a recorded value, in the order applied by `tools/build.py`. A recode "
           "asserts the source carries `from` before it applies; the claim keeps both values in "
           "its `history`. Addenda tags: `wo`.", "",
           "| seq | id | kind | object | field | from | to | NCR | wo | applied |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    def cell(x):
        s = "-" if x is None else str(x)
        s = s if len(s) <= 24 else s[:10] + "..." + s[-8:]
        return s.replace("|", "\\|")
    for c in sorted(reg.of("CHANGE"), key=lambda c: c["seq"]):
        out.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            c["seq"], c["id"], c["kind"], c["object"], c["field"], cell(c["from"]),
            cell(c["to"]), c["ncr"] or "-", c["wo"], c["applied"]))
    out += ["", "## Reasons", ""]
    for c in sorted(reg.of("CHANGE"), key=lambda c: c["seq"]):
        out.append("- **%s** -- %s" % (c["id"], c["reason"]))
    return "\n".join(out) + "\n"


# (term, the work order's reading, clause borrowed from, ledger rows, registry
#  implementation, difference)
QA_ROWS = [
    ("design basis", "every grade and direction traces to evidence objects",
     "10 CFR 50 App B Criterion III (design control; verification by others)", ["V091", "V092"],
     "every claim carries status, coder, source/basis; tools/chain.py walks evidence, actor and authority chains with the state at each hop",
     "the regulatory term 'design bases' (10 CFR 50.2) has no ledger row here; the registry borrows the traceability requirement, not the definition"),
    ("independent verification", "BLIND or CONTAMINATED-BY-PRIOR, recorded per verifier",
     "App B Criterion III: design verification by individuals or groups other than those who performed the original design", ["V091"],
     "independence field on claims and NCRs; ACT-CODER2 second coding with a contamination probe first",
     "Criterion III asks for a different person; the registry's second coder is a different session of the same model class, so 'other than' holds for the session and not for the class [INFERENCE]"),
    ("configuration management", "versioned records, pinned hashes, a CHANGE per edit",
     "App B Criterion III (design changes controlled like the original) and Criteria VI/XVII (document control, records)", ["V092", "V095", "V100"],
     "bundle_pins.json, bundle/MANIFEST.sha256, registry/MANIFEST.json, version and history on every recoded claim, CHANGE objects",
     "'configuration management' as a named criterion: not confirmed either way (V100); the registry implements the controls the cited criteria name"),
    ("corrective action", "one NCR per review item; ACCEPT / REJECT / MODIFY plus a reason",
     "App B Criterion XV (nonconforming items: accepted, rejected, repaired or reworked) and Criterion XVI (corrective action; cause determined for significant conditions)", ["V093", "V094", "V098"],
     "NCR objects with disposition, reason, changes, statements; validate.py checks each CHANGE names an NCR that lists it",
     "same word, opposite operation: under Criterion XV 'accepted' disposes of a nonconforming ITEM unchanged (use-as-is), while the work order's ACCEPT accepts a review FINDING and changes the record. The registry keeps the work order's sense. Criterion XVI's cause determination has no NCR field here"),
    ("graded approach", "verification rigor scales with consequence grade",
     "10 CFR 830.3 (DOE): level of analysis, documentation and actions commensurate with importance to safety; App B Criterion II: QA applied consistent with importance to safety", ["V099", "V090"],
     "rigor_tier per case from its C_permit grade (C4 T1, C3 T2, else T3)",
     "the definition located is DOE's (10 CFR 830), not NRC's; tiers are assigned and verification did not scale with them in this session (see the graded-approach table in REVISED_REPORT.md)"),
    ("single-failure check", "flag any conclusion resting on one source or one coder",
     "10 CFR 50 App A, Definitions: an occurrence that results in loss of a component's capability to perform its safety function", ["V097"],
     "tools/chain.py flags ONE_CODER, ONE_SOURCE, NO_LOCATED_SOURCE, AUTHORITY_GAP, ORIGINATOR_ONLY; audit NCRs carry single_failure",
     "the defined term is in Appendix A (design criteria), not Appendix B, and concerns component failure in a system; the registry's use is evidentiary redundancy, an analogy to the term [INFERENCE]"),
    ("NQA-1", "the consensus standard behind Appendix B practice",
     "NRC Regulatory Guide 1.28 endorses ASME NQA-1 as a way to meet Appendix B", ["V096", "V098"],
     "none beyond the vocabulary above",
     "NQA-1's own text is not public and was not read; its disposition list (V098) is not verified"),
]


def render_qa(reg):
    out = ["<!-- GENERATED by tools/report.py (QA_ROWS) with ledger states from registry/evidence.json; do not edit -->",
           "# QA MAPPING", "",
           "The work order borrows six terms from nuclear QA (the seventh row is NQA-1, the standard behind them) and asks that the mapping be verified, "
           "not assumed (NCR-N23). Each row: the work order's reading, the clause it borrows from, the "
           "ledger rows for that clause and their states (search-index depth at most; eCFR not opened), "
           "what the registry implements, and where the borrowed term and the registry differ.", "",
           "| term | work order reading | clause | ledger (state) | registry implements | difference |",
           "|---|---|---|---|---|---|"]
    for term, wo, clause, rows, impl, diff in QA_ROWS:
        states = ", ".join("%s %s" % (r, reg.get("EV-" + r)["verification"]["state"]) for r in rows)
        out.append("| %s | %s | %s | %s | %s | %s |" % (term, wo, clause, states, impl, diff))
    return "\n".join(out) + "\n"


def write_all(reg=None):
    reg = reg or reglib.Registry()
    outs = []
    for path, tpath in TEMPLATED:
        tmpl = open(tpath, "r", encoding="utf-8").read()
        outs.append((path, render(reg, tmpl, os.path.basename(tpath))))
    outs += [(CHANGELOG, render_changelog(reg)), (QA, render_qa(reg))]
    for path, text in outs:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return [p for p, _ in outs]


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("report.py: checks run in tools/validate.py --selftest\n")
        return 2
    reg = reglib.Registry()
    if "--keys" in argv:
        for k, x in sorted(values(reg).items()):
            if not k.startswith("table."):
                print("%-52s %s" % (k, x))
        return 0
    for p in write_all(reg):
        print("wrote %s" % reglib.rel(p))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
