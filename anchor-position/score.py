#!/usr/bin/env python3
"""score.py -- the mechanical scorer of WORK ORDER section 6, the claims of
section 7 and the nulls of section 8, over a responses.jsonl the operator
filled by running prompts.py's files in fresh sessions.

    python3 score.py cases.jsonl responses.jsonl [codings.jsonl] [--arm-md] [--n2-first]
    python3 score.py --selftest

Every response is scored under BOTH published lists (transforms.json,
transforms_alt.json); N4 is their disagreement. Under each list every
response is scored TWICE -- unknown tokens as residue (the floor,
crossing_count) and as measurand vocabulary (the ceiling,
crossing_count_max) -- and a claim is SUPPORTED or REFUTED only when both
ends agree, else BAND (WORK_ORDER_2 W3). No grader judgement: the only
human input is the optional codings.jsonl for N1 (practitioner
recognition), which is reported as a rate and never gates anything.

Every open decision is one entry in CHOICES, printed in every report
header; every amendment to the delivered order's design is a FLAG, default
off, OPEN in CLAIM_TABLE.md until the operator signs (WORK_ORDER_2 W7,
W9, W10).
"""
import json
import os
import re
import sys

import normalize as nz
import prompts

HERE = os.path.dirname(os.path.abspath(__file__))
DEFECT_RE = re.compile(r"^\s*DEFECT\s+(\d+)\s*$")
FIELD_RE = re.compile(r"^\s*(quantity|set|defect|measured_by_method|gap)\s*:\s*(.*)$")
M_FORM = ("M", "M+", "B", "C")          # DEFECT-block form
D_FORM = ("D", "M_D")                    # three-field form (M_D only under FLAGS["arm_md"])
REQUIRED = ("case_id", "arm", "model", "version", "date", "response")
FORM_FLOOR = 0.8                         # [CHOICE 4]
D_LEVEL = "ge"                           # [CHOICE 5] "ge" | "gt"; read by claims() (W2)
KEYS = ("crossing_count", "crossing_count_max")   # the two ends of the band [CHOICE 9]

# One registry (W7). README.md cites these by id; the report header prints
# every entry; the selftest asserts the header carries every id.
CHOICES = {
    1: "M+ places D's one sentence after the claim+method block (--mplus-tail appends it after the last line)",
    2: "the [CLAIM + METHOD] block carries claim and method only; field and native are withheld",
    3: "crossing_count subtracts native_groups_hit (a disjunctive native names two measurands); cc_order keeps the order's 0/1 form",
    4: "FORM_FLOOR=%s: N5 fires only when both M and D form-ok rates fall below it" % FORM_FLOOR,
    5: "D_LEVEL=%s: M+ reaches D-level when cc(M+) >= cc(D) under 'ge', > under 'gt'" % D_LEVEL,
    6: "control cases (decision_native) are excluded from AP-2/AP-3/AP-6 and named; scored under N2",
    7: "a continuation line (indented, no field) appends to the last field; any other line outside the fields is stray",
    8: "parentheticals in a quantity string are stripped as glosses or units (normalize.py)",
    9: "every list scored twice: unknown tokens as residue (crossing_count, floor) and as measurand vocabulary (crossing_count_max, ceiling); a claim is SUPPORTED/REFUTED only at both ends, else BAND",
    10: "replicate rows per (case, model, arm) are all kept: paired claims run on every pair, collisions counted and printed",
    11: "AP-3 is evaluated only on (case, model) triples where cc(D) > cc(M); the rest are listed as uninformative",
    12: "an empty response scores None on every crossing field (ABSENT); every comparison skips it and counts it",
}
FLAGS = {
    "arm_md": [False, "W9 ORDER: arm M_D (M's question, D's three-field schema, no decision) accepted and read; "
                      "M_D ~ D -> schema carries the effect, M_D ~ M -> anchor survives the schema control"],
    "n2_first": [False, "W10 ORDER: N2 read on entry 1 of a control D response only; entries 2..n reported as N2_rest"],
}


def parse_response(text, arm):
    """-> (entries, form). Continuation lines (indented, no field) append to
    the last field [CHOICE 7]; any other line outside the fields is stray."""
    m_form = arm in M_FORM
    entries, stray, cur, last = [], 0, None, None
    for line in text.splitlines():
        if not line.strip():
            continue
        dm = DEFECT_RE.match(line)
        if dm and m_form:
            cur, last = {"n": int(dm.group(1))}, None
            entries.append(cur)
            continue
        fm = FIELD_RE.match(line)
        if fm:
            key, val = fm.group(1), fm.group(2).strip()
            if not m_form and key == "quantity":
                cur = {}
                entries.append(cur)
            if cur is None or key in cur:
                stray += 1
                continue
            cur[key], last = val, key
            continue
        if cur is not None and last and line[:1].isspace():
            cur[last] = (cur[last] + " " + line.strip()).strip()
            continue
        stray += 1
    need = ("quantity", "set", "defect") if m_form else ("quantity", "measured_by_method", "gap")
    complete = [e for e in entries if all(k in e for k in need)]
    values_ok = m_form or all(e["measured_by_method"] in ("yes", "no", "partial")
                              for e in complete)
    form = {"stray_lines": stray, "incomplete": len(entries) - len(complete),
            "values_ok": values_ok,
            "form_ok": stray == 0 and len(complete) == len(entries)
            and bool(entries) and values_ok}
    return complete, form


def load_responses(path, cases, flags=None):
    flags = flags or {}
    rows = []
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                continue
            r = json.loads(line)
            if "_constructed" in r:
                continue
            missing = [k for k in REQUIRED if k not in r]
            if missing:
                raise ValueError("%s line %d missing %s" % (path, ln, missing))
            if r["case_id"] not in cases:
                raise ValueError("%s line %d: unknown case %s" % (path, ln, r["case_id"]))
            if r["arm"] not in M_FORM + D_FORM:
                raise ValueError("%s line %d: unknown arm %s" % (path, ln, r["arm"]))
            if r["arm"] == "M_D" and not flags.get("arm_md"):
                raise ValueError("%s line %d: arm M_D is the W9 ORDER item, behind --arm-md "
                                 "(default off, OPEN until the operator signs)" % (path, ln))
            if r["arm"] in ("D", "M+"):
                if r.get("decision") != cases[r["case_id"]]["decision"]:
                    raise ValueError("%s line %d: %s row must log the case's decision "
                                     "string verbatim" % (path, ln, r["arm"]))
            if r["arm"] == "C" and "supplied_measurand" not in r:
                raise ValueError("%s line %d: C row needs supplied_measurand" % (path, ln))
            r["_line"] = ln
            rows.append(r)
    return rows


def score_rows(rows, cases, lexes):
    out = []
    for r in rows:
        entries, form = parse_response(r["response"], r["arm"])
        qs = [e["quantity"] for e in entries]
        native = cases[r["case_id"]]["native"]
        rec = {"case_id": r["case_id"], "arm": r["arm"], "model": r["model"],
               "family": r.get("family", "unstated"), "form": form,
               "entries": entries, "by_lexicon": {}}
        for lex in lexes:
            rec["by_lexicon"][lex["name"]] = nz.score(qs, native, lex)
        if r["arm"] == "C":
            rec["supplied_measurand"] = r["supplied_measurand"]
        out.append(rec)
    return out


def cells(scored):
    """(case, model, arm) -> every row scored for it, in input order."""
    idx = {}
    for s in scored:
        idx.setdefault((s["case_id"], s["model"], s["arm"]), []).append(s)
    return idx


def collisions(scored):
    """cells holding more than one row (W4): counted and printed, never merged."""
    return sorted((c, m, a, len(v)) for (c, m, a), v in cells(scored).items() if len(v) > 1)


def _pairs(scored, a, b, cases):
    """(case, model) cells holding both arms -> every (rec_a, rec_b) pair
    [CHOICE 10]. Control cases (decision_native) are EXCLUDED [CHOICE 6]:
    there D == M is the correct reading by construction, so AP-2/AP-3/AP-6
    as written would be refuted by the control section 8 requires."""
    idx = cells(scored)
    for (c, m, arm), rows in sorted(idx.items(), key=lambda kv: kv[0]):
        if arm == a and (c, m, b) in idx and not cases[c]["decision_native"]:
            for s in rows:
                for t in idx[(c, m, b)]:
                    yield s, t


def cc(s, lexname, key="crossing_count"):
    """None when the response carried no entries (ABSENT) [CHOICE 12]."""
    return s["by_lexicon"][lexname][key]


def absent_by_arm(scored, lexname):
    out = {}
    for s in scored:
        d = out.setdefault(s["arm"], {"rows": 0, "absent": 0})
        d["rows"] += 1
        d["absent"] += 1 if cc(s, lexname) is None else 0
    for arm, d in out.items():
        d["share"] = round(d["absent"] / d["rows"], 3) if d["rows"] else None
    return out


def _claims_at(scored, cases, lexname, key, d_level):
    """AP-1..AP-6 at one end of the band; each SUPPORTED / REFUTED / UNRUN
    with its evidence. ABSENT rows (None) are skipped and counted (W1)."""
    res = {}
    m_rows = [s for s in scored if s["arm"] == "M"]
    m_abs = [s["case_id"] for s in m_rows if cc(s, lexname, key) is None]
    m_live = [s for s in m_rows if cc(s, lexname, key) is not None]
    hits = [(s["case_id"], cc(s, lexname, key)) for s in m_live if cc(s, lexname, key) > 0]
    res["AP-1"] = ("UNRUN" if not m_live else "REFUTED" if hits else "SUPPORTED",
                   {"M_rows": len(m_rows), "absent": len(m_abs), "crossings": hits})
    pairs = list(_pairs(scored, "D", "M", cases))
    live = [(d, m) for d, m in pairs if cc(d, lexname, key) is not None and cc(m, lexname, key) is not None]
    bad = [(d["case_id"], cc(d, lexname, key), cc(m, lexname, key)) for d, m in live
           if cc(d, lexname, key) <= cc(m, lexname, key)]
    ctl = sorted(c for c in cases if cases[c]["decision_native"])
    res["AP-2"] = ("UNRUN" if not live else "REFUTED" if bad else "SUPPORTED",
                   {"pairs": len(pairs), "absent_pairs": len(pairs) - len(live), "D_le_M": bad,
                    "controls_excluded": ctl})
    # AP-3 on informative triples only [CHOICE 11]: a triple is (M+, D, M) on one
    # (case, model) cell; it is informative when cc(D) > cc(M), since where D
    # produced no more crossings than M there is no D-level for M+ to reach.
    idx = cells(scored)
    triples, uninf, absent3 = [], [], 0
    for p, d in _pairs(scored, "M+", "D", cases):
        ms = idx.get((p["case_id"], p["model"], "M"), [])
        if not ms:
            uninf.append((p["case_id"], "no M row"))
            continue
        for m in ms:
            vals = (cc(p, lexname, key), cc(d, lexname, key), cc(m, lexname, key))
            if any(v is None for v in vals):
                absent3 += 1
                continue
            if vals[1] > vals[2]:
                triples.append((p["case_id"], vals[0], vals[1], vals[2]))
            else:
                uninf.append((p["case_id"], "cc(D)=%d <= cc(M)=%d" % (vals[1], vals[2])))
    reaches = [t for t in triples if (t[1] >= t[2] if d_level == "ge" else t[1] > t[2])]
    res["AP-3"] = ("UNRUN" if not triples else "REFUTED" if reaches else "SUPPORTED",
                   {"triples": len(triples), "uninformative": uninf, "absent": absent3,
                    "Mplus_reaches_D": [(t[0], t[1], t[2]) for t in reaches], "d_level": d_level})
    bp = list(_pairs(scored, "B", "M", cases))
    sup, absent4 = [], 0
    lex = LEX[lexname]
    for b, m in bp:
        bq = [e["quantity"] for e in b["entries"]]
        mq = [e["quantity"] for e in m["entries"]]
        if not bq or not mq:
            absent4 += 1
            continue
        sb, sm, names = nz.measurand_sets(bq, mq, cases[b["case_id"]]["native"], lex,
                                          unknown_is_vocab=(key == "crossing_count_max"))
        if sb > sm:
            sup.append((b["case_id"], [q for g in sorted(sb - sm) for q in names[g]]))
    res["AP-4"] = ("UNRUN" if not (bp and len(bp) > absent4) else "REFUTED" if sup else "SUPPORTED",
                   {"pairs": len(bp), "absent_pairs": absent4, "strict_superset": sup,
                    "compared_on": "measurand groups, not strings (W5)"})
    crows = [s for s in scored if s["arm"] == "C"]
    ret, absent5 = [], 0
    for s in crows:
        qs = [e["quantity"] for e in s["entries"]]
        if not qs:
            absent5 += 1
            continue
        r = nz.score(qs, s["supplied_measurand"], lex)
        if (r["native_hit"] if key == "crossing_count" else r["native_hit_max"]):
            ret.append(s["case_id"])
    res["AP-5"] = ("UNRUN" if not (crows and len(crows) > absent5) else "REFUTED" if ret else "SUPPORTED",
                   {"C_rows": len(crows), "absent": absent5, "returned_supplied": ret})
    fams = {}
    for d, m in live:
        fams.setdefault(d["family"], []).append(cc(d, lexname, key) == cc(m, lexname, key))
    eq = [f for f, v in fams.items() if v and all(v)]
    res["AP-6"] = ("UNRUN" if len(fams) < 2 else "REFUTED" if eq else "SUPPORTED",
                   {"families": sorted(fams), "D_eq_M_family": eq})
    return res


def claims(scored, cases, lexname, d_level=None):
    """Both ends of the band [CHOICE 9]: a claim is SUPPORTED / REFUTED /
    UNRUN when the floor and the ceiling agree, else BAND with both ends
    shown. Evidence is the floor's, with `max` carrying the ceiling's."""
    d_level = d_level or D_LEVEL
    lo = _claims_at(scored, cases, lexname, KEYS[0], d_level)
    hi = _claims_at(scored, cases, lexname, KEYS[1], d_level)
    out = {}
    for k in lo:
        st = lo[k][0] if lo[k][0] == hi[k][0] else "BAND"
        ev = dict(lo[k][1])
        ev["band"] = [lo[k][0], hi[k][0]]
        ev["max"] = hi[k][1]
        out[k] = (st, ev)
    return out


def md_reading(scored, cases, lexname):
    """W9 (flag): per (case, model) cell holding M_D, D and M -- which of D
    and M the schema-controlled arm sits nearer to, per band end."""
    idx = cells(scored)
    out = []
    for (c, m, arm), rows in sorted(idx.items()):
        if arm != "M_D" or cases[c]["decision_native"]:
            continue
        ds, ms = idx.get((c, m, "D"), []), idx.get((c, m, "M"), [])
        for md in rows:
            for d in ds:
                for mm in ms:
                    row = {"case_id": c, "model": m}
                    for key in KEYS:
                        v = (cc(md, lexname, key), cc(d, lexname, key), cc(mm, lexname, key))
                        if any(x is None for x in v):
                            row[key] = {"reading": "ABSENT"}
                            continue
                        if v[1] <= v[2]:
                            r = "uninformative (cc(D) <= cc(M))"
                        elif abs(v[0] - v[1]) < abs(v[0] - v[2]):
                            r = "M_D ~ D: schema carries the effect"
                        elif abs(v[0] - v[2]) < abs(v[0] - v[1]):
                            r = "M_D ~ M: anchor survives the schema control"
                        else:
                            r = "equidistant"
                        row[key] = {"M_D": v[0], "D": v[1], "M": v[2], "reading": r}
                    out.append(row)
    return out


def _n2(rows, lexname, which):
    """which: 'all' (the delivered rule), 'first', 'rest'."""
    gaps = []
    for s in rows:
        ents = s["entries"] if which == "all" else s["entries"][:1] if which == "first" else s["entries"][1:]
        if not ents:
            continue
        labels = [e["measured_by_method"] for e in ents]
        r = nz.score([e["quantity"] for e in ents], s["_native"], LEX[lexname])
        if r["crossing_count"] > 0 or any(l != "yes" for l in labels):
            gaps.append((s["case_id"], r["crossing_count"], labels))
    return gaps


def nulls(scored, cases, codings, lexes, flags=None):
    flags = flags or {}
    p, a = lexes[0]["name"], lexes[1]["name"]
    out = {}
    if codings is None:
        out["N1"] = ("NOT_EVALUATED", {"why": "no codings.jsonl; practitioner "
                                              "recognition is a human coding"})
    else:
        rec = [c["practitioner_recognizes"] for c in codings if c["arm"] == "D"]
        out["N1"] = ("REPORTED", {"n": len(rec), "unrecognized_rate":
                                  (None if not rec else round(1 - sum(rec) / len(rec), 3))})
    ctl = [s for s in scored if s["arm"] == "D" and cases[s["case_id"]]["decision_native"]]
    for s in ctl:
        s["_native"] = cases[s["case_id"]]["native"]
    absent2 = sum(1 for s in ctl if cc(s, p) is None)
    if flags.get("n2_first"):
        first, rest = _n2(ctl, p, "first"), _n2(ctl, p, "rest")
        out["N2_first"] = ("NOT_EVALUATED" if not ctl else "FIRES" if first else "CLEAN",
                           {"control_D_rows": len(ctl), "absent": absent2, "gaps_on_control": first,
                            "flag": "n2_first ON (W10 ORDER item)",
                            "N-W10": "D over-flags independent of enumeration" if first else "not fired"})
        out["N2_rest"] = ("REPORTED", {"entries_2_to_n_gaps": rest})
    else:
        gaps = _n2(ctl, p, "all")
        out["N2"] = ("NOT_EVALUATED" if not ctl else "FIRES" if gaps else "CLEAN",
                     {"control_D_rows": len(ctl), "absent": absent2, "gaps_on_control": gaps})
    by_field = {}
    for s in scored:
        if s["arm"] == "M" and cc(s, p) is not None and cc(s, p) > 0:
            by_field.setdefault(cases[s["case_id"]]["field"], []).append(s["case_id"])
    out["N3"] = ("FIRES" if by_field else "SILENT", {"M_crossings_by_field": by_field})
    dis = [(s["case_id"], s["arm"], cc(s, p), cc(s, a)) for s in scored
           if cc(s, p) is not None and cc(s, a) is not None and cc(s, p) != cc(s, a)]
    out["N4"] = ("FIRES" if dis else "AGREE", {"lists": [p, a], "n_scored": len(scored),
                                                "disagreements": dis})
    rate = {}
    for arm in ("M", "D", "M+"):
        rs = [s for s in scored if s["arm"] == arm]
        rate[arm] = None if not rs else round(sum(s["form"]["form_ok"] for s in rs) / len(rs), 3)
    both_low = all(v is not None and v < FORM_FLOOR for v in (rate["M"], rate["D"]))
    out["N5"] = ("FIRES" if both_low else "SILENT", {"form_ok_rate": rate, "floor": FORM_FLOOR})
    return out


def self_label(scored, cases, lexname):
    """W11, gates nothing: on every D-form entry, the model's own
    measured_by_method label against the scorer's native membership of
    that entry's quantity. yes <-> native agrees; no <-> non-native agrees;
    partial is its own bucket, neither agree nor disagree."""
    out = []
    for s in scored:
        if s["arm"] not in D_FORM or not s["entries"]:
            continue
        r = s["by_lexicon"][lexname]
        nat = set(q for g in r["groups"] if g["native"] for q in g["quantities"])
        rows, agree, disagree, partial = [], 0, 0, 0
        for e in s["entries"]:
            is_nat = e["quantity"] in nat
            lab = e["measured_by_method"]
            if lab == "partial":
                verdict, partial = "partial", partial + 1
            elif (lab == "yes") == is_nat:
                verdict, agree = "agree", agree + 1
            else:
                verdict, disagree = "disagree", disagree + 1
            rows.append((e["quantity"], lab, "native" if is_nat else "non-native", verdict))
        n = agree + disagree
        out.append({"case_id": s["case_id"], "arm": s["arm"], "model": s["model"], "rows": rows,
                    "agree": agree, "disagree": disagree, "partial": partial,
                    "agreement_rate": round(agree / n, 3) if n else None})
    return out


LEX = {}


def _fmt(v):
    return "-" if v is None else str(v)


def report(cases, scored, cl, nl, lexes, flags=None):
    flags = flags or {}
    L = ["ANCHOR POSITION AND MEASURAND CROSSING -- scorer output",
         "lists: %s" % ", ".join("%s (%s)" % (x["name"], os.path.basename(x["_path"])) for x in lexes)]
    for k in sorted(CHOICES):
        L.append("[CHOICE %d] %s" % (k, CHOICES[k]))
    for k in sorted(FLAGS):
        L.append("[FLAG %s=%s] %s" % (k, "ON" if flags.get(k) else "off", FLAGS[k][1]))
    L.append("")
    L.append("%-8s %-3s %-16s %-4s %-8s %-6s %-8s %-8s %-8s %-4s %s" % (
        "case", "arm", "model", "n", "distinct", "native", "cc_min", "cc_max", "cc_order", "form", "unknown_tokens"))
    for s in scored:
        for lex in lexes:
            b = s["by_lexicon"][lex["name"]]
            L.append("%-8s %-3s %-16s %-4d %-8d %-6d %-8s %-8s %-8s %-4s %s  [%s]" % (
                s["case_id"], s["arm"], s["model"][:16], b["n_entries"], b["distinct_measurands"],
                b["native_groups_hit"], _fmt(b["crossing_count"]), _fmt(b["crossing_count_max"]),
                _fmt(b["crossing_count_order"]),
                "ok" if s["form"]["form_ok"] else "BAD", ",".join(b["unknown_tokens"]) or "-",
                lex["name"]))
    L.append("")
    p = lexes[0]["name"]
    ab = absent_by_arm(scored, p)
    L.append("ABSENT rows (no entries; None, skipped by every comparison) per arm: " + ", ".join(
        "%s %d of %d" % (arm, d["absent"], d["rows"]) for arm, d in sorted(ab.items())))
    high = [arm for arm, d in ab.items() if d["share"] is not None and d["share"] > 0.2]
    if high:
        L.append("  N-W1: ABSENT exceeds 20%% of arm(s) %s -- reported, arm not dropped" % ", ".join(sorted(high)))
    col = collisions(scored)
    L.append("replicate collisions (cells with >1 row; all pairs used [CHOICE 10]): %d%s" % (
        len(col), "" if not col else " -- " + "; ".join("%s/%s/%s x%d" % c for c in col)))
    L.append("")
    L.append("groups (primary, floor end):")
    for s in scored:
        for g in s["by_lexicon"][p]["groups"]:
            L.append("  %s %-3s %s %s" % (s["case_id"], s["arm"], "NATIVE " if g["native"] else "       ",
                                          " | ".join(g["quantities"])))
    for lex in lexes:
        L.append("")
        L.append("claims under %s (floor / ceiling; BAND when the ends differ):" % lex["name"])
        for k, (st, ev) in sorted(cl[lex["name"]].items()):
            ev = dict(ev)
            band, mx = ev.pop("band"), ev.pop("max")
            L.append("  %-5s %-10s %s" % (k, st, json.dumps(ev)))
            L.append("        band %s; ceiling %s" % (json.dumps(band), json.dumps(mx)))
        bands = [k for k, (st, ev) in cl[lex["name"]].items() if st == "BAND"]
        if bands:
            L.append("  N-W3: BAND on %s under %s -- reported as the result" % (", ".join(sorted(bands)), lex["name"]))
    L.append("")
    L.append("nulls:")
    for k, (st, ev) in sorted(nl.items()):
        L.append("  %-8s %-14s %s" % (k, st, json.dumps(ev)))
    if flags.get("arm_md"):
        L.append("")
        L.append("M_D reading (W9 ORDER item, flag ON):")
        rows = md_reading(scored, cases, p)
        if not rows:
            L.append("  no (case, model) cell holds M_D, D and M")
        for r in rows:
            L.append("  %s %s  floor %s  ceiling %s" % (r["case_id"], r["model"], json.dumps(r[KEYS[0]]), json.dumps(r[KEYS[1]])))
    else:
        L.append("")
        L.append("N-W9: M_D not run (flag off) -- the AP-3 finding stays 'anchor OR schema'")
    L.append("")
    L.append("self-label vs scorer (W11; reported, gates nothing; primary list, floor end):")
    sl = self_label(scored, cases, p)
    if not sl:
        L.append("  no D-form rows")
    for r in sl:
        L.append("  %s %-3s %s  agree %d  disagree %d  partial %d  rate %s" % (
            r["case_id"], r["arm"], r["model"][:16], r["agree"], r["disagree"], r["partial"], _fmt(r["agreement_rate"])))
        for q, lab, nat, v in r["rows"]:
            L.append("      %-9s %-7s %-10s %s" % (v, lab, nat, q))
    L.append("")
    L.append("decision strings logged (section 9): " + "; ".join(
        "%s=%r" % (c, cases[c]["decision"]) for c in sorted(cases)))
    return "\n".join(L)


def run(cases_path, responses_path, codings_path=None, flags=None):
    flags = dict(flags or {})
    cases = {c["case_id"]: c for c in prompts.load_cases(cases_path)}
    lexes = [nz.load_lexicon(nz.PRIMARY), nz.load_lexicon(nz.ALT)]
    for lex in lexes:
        LEX[lex["name"]] = lex
    rows = load_responses(responses_path, cases, flags)
    codings = None
    if codings_path:
        codings = [json.loads(l) for l in open(codings_path) if l.strip()]
    scored = score_rows(rows, cases, lexes)
    cl = {lex["name"]: claims(scored, cases, lex["name"]) for lex in lexes}
    nl = nulls(scored, cases, codings, lexes, flags)
    return cases, scored, cl, nl, lexes


def main(argv):
    if "--selftest" in argv:
        import selftest_apm
        return selftest_apm.main()
    flags = {"arm_md": "--arm-md" in argv, "n2_first": "--n2-first" in argv}
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    cases, scored, cl, nl, lexes = run(args[0], args[1], args[2] if len(args) > 2 else None, flags)
    print(report(cases, scored, cl, nl, lexes, flags))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
