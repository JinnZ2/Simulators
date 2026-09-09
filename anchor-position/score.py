#!/usr/bin/env python3
"""score.py -- the mechanical scorer of WORK ORDER section 6, the claims of
section 7 and the nulls of section 8, over a responses.jsonl the operator
filled by running prompts.py's files in fresh sessions.

    python3 score.py cases.jsonl responses.jsonl [codings.jsonl]
    python3 score.py --selftest

Every response is scored under BOTH published lists (transforms.json,
transforms_alt.json); N4 is their disagreement. No grader judgement:
the only human input is the optional codings.jsonl for N1 (practitioner
recognition), which is reported as a rate and never gates anything.
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
D_FORM = ("D",)                          # three-field form
REQUIRED = ("case_id", "arm", "model", "version", "date", "response")
FORM_FLOOR = 0.8                         # [CHOICE 3] N5 fires below this, both arms
D_LEVEL = "ge"                           # [CHOICE 4] M+ reaches D-level when >= D


def parse_response(text, arm):
    """-> (entries, form). Continuation lines (indented, no field) append to
    the last field [CHOICE 5]; any other line outside the fields is stray."""
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


def load_responses(path, cases):
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


def _pairs(scored, a, b, cases):
    """(case, model) pairs holding both arms -> (rec_a, rec_b). Control cases
    (decision_native) are EXCLUDED [CHOICE 6]: there D == M is the correct
    reading by construction, so AP-2/AP-3/AP-6 as written would be refuted
    by the control section 8 requires. Controls are scored under N2."""
    idx = {}
    for s in scored:
        idx.setdefault((s["case_id"], s["model"], s["arm"]), s)
    for (c, m, arm), s in sorted(idx.items(), key=lambda kv: kv[0]):
        if arm == a and (c, m, b) in idx and not cases[c]["decision_native"]:
            yield s, idx[(c, m, b)]


def cc(s, lexname):
    return s["by_lexicon"][lexname]["crossing_count"]


def claims(scored, cases, lexname):
    """AP-1..AP-6; each SUPPORTED / REFUTED / UNRUN with its evidence."""
    res = {}
    m_rows = [s for s in scored if s["arm"] == "M"]
    hits = [(s["case_id"], cc(s, lexname)) for s in m_rows if cc(s, lexname) > 0]
    res["AP-1"] = ("UNRUN" if not m_rows else "REFUTED" if hits else "SUPPORTED",
                   {"M_rows": len(m_rows), "crossings": hits})
    pairs = list(_pairs(scored, "D", "M", cases))
    bad = [(d["case_id"], cc(d, lexname), cc(m, lexname)) for d, m in pairs
           if cc(d, lexname) <= cc(m, lexname)]
    ctl = sorted(c for c in cases if cases[c]["decision_native"])
    res["AP-2"] = ("UNRUN" if not pairs else "REFUTED" if bad else "SUPPORTED",
                   {"pairs": len(pairs), "D_le_M": bad, "controls_excluded": ctl})
    mp = list(_pairs(scored, "M+", "D", cases))
    reach = [(p["case_id"], cc(p, lexname), cc(d, lexname)) for p, d in mp
             if cc(p, lexname) >= cc(d, lexname)]
    res["AP-3"] = ("UNRUN" if not mp else "REFUTED" if reach else "SUPPORTED",
                   {"pairs": len(mp), "Mplus_reaches_D": reach, "d_level": D_LEVEL})
    bp = list(_pairs(scored, "B", "M", cases))
    sup = []
    for b, m in bp:
        bq = set(e["quantity"].lower() for e in b["entries"])
        mq = set(e["quantity"].lower() for e in m["entries"])
        if bq > mq:
            sup.append(b["case_id"])
    res["AP-4"] = ("UNRUN" if not bp else "REFUTED" if sup else "SUPPORTED",
                   {"pairs": len(bp), "strict_superset": sup})
    crows = [s for s in scored if s["arm"] == "C"]
    ret = []
    for s in crows:
        lex = LEX[lexname]
        qs = [e["quantity"] for e in s["entries"]]
        if qs and nz.score(qs, s["supplied_measurand"], lex)["native_hit"]:
            ret.append(s["case_id"])
    res["AP-5"] = ("UNRUN" if not crows else "REFUTED" if ret else "SUPPORTED",
                   {"C_rows": len(crows), "returned_supplied": ret})
    fams = {}
    for d, m in pairs:
        fams.setdefault(d["family"], []).append(cc(d, lexname) == cc(m, lexname))
    eq = [f for f, v in fams.items() if v and all(v)]
    res["AP-6"] = ("UNRUN" if len(fams) < 2 else "REFUTED" if eq else "SUPPORTED",
                   {"families": sorted(fams), "D_eq_M_family": eq})
    return res


def nulls(scored, cases, codings, lexes):
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
    gaps = [(s["case_id"], cc(s, p), [e["measured_by_method"] for e in s["entries"]])
            for s in ctl if cc(s, p) > 0 or any(e["measured_by_method"] != "yes"
                                                for e in s["entries"])]
    out["N2"] = ("NOT_EVALUATED" if not ctl else "FIRES" if gaps else "CLEAN",
                 {"control_D_rows": len(ctl), "gaps_on_control": gaps})
    by_field = {}
    for s in scored:
        if s["arm"] == "M" and cc(s, p) > 0:
            by_field.setdefault(cases[s["case_id"]]["field"], []).append(s["case_id"])
    out["N3"] = ("FIRES" if by_field else "SILENT", {"M_crossings_by_field": by_field})
    dis = [(s["case_id"], s["arm"], cc(s, p), cc(s, a)) for s in scored if cc(s, p) != cc(s, a)]
    out["N4"] = ("FIRES" if dis else "AGREE", {"lists": [p, a], "n_scored": len(scored),
                                                "disagreements": dis})
    rate = {}
    for arm in ("M", "D", "M+"):
        rs = [s for s in scored if s["arm"] == arm]
        rate[arm] = None if not rs else round(sum(s["form"]["form_ok"] for s in rs) / len(rs), 3)
    both_low = all(v is not None and v < FORM_FLOOR for v in (rate["M"], rate["D"]))
    out["N5"] = ("FIRES" if both_low else "SILENT", {"form_ok_rate": rate, "floor": FORM_FLOOR})
    return out


LEX = {}


def report(cases, scored, cl, nl, lexes):
    L = ["ANCHOR POSITION AND MEASURAND CROSSING -- scorer output",
         "lists: %s" % ", ".join("%s (%s)" % (x["name"], os.path.basename(x["_path"])) for x in lexes),
         "[CHOICE] FORM_FLOOR=%s  D_LEVEL=%s  crossing_count subtracts native_groups_hit; "
         "crossing_count_order is the order's arithmetic" % (FORM_FLOOR, D_LEVEL), ""]
    L.append("%-8s %-3s %-16s %-4s %-8s %-6s %-8s %-8s %-4s %s" % (
        "case", "arm", "model", "n", "distinct", "native", "crossing", "cc_order", "form", "unknown_tokens"))
    for s in scored:
        for lex in lexes:
            b = s["by_lexicon"][lex["name"]]
            L.append("%-8s %-3s %-16s %-4d %-8d %-6d %-8d %-8d %-4s %s  [%s]" % (
                s["case_id"], s["arm"], s["model"][:16], b["n_entries"], b["distinct_measurands"],
                b["native_groups_hit"], b["crossing_count"], b["crossing_count_order"],
                "ok" if s["form"]["form_ok"] else "BAD", ",".join(b["unknown_tokens"]) or "-",
                lex["name"]))
    L.append("")
    L.append("groups (primary):")
    for s in scored:
        for g in s["by_lexicon"][lexes[0]["name"]]["groups"]:
            L.append("  %s %-3s %s %s" % (s["case_id"], s["arm"], "NATIVE " if g["native"] else "       ",
                                          " | ".join(g["quantities"])))
    for lex in lexes:
        L.append("")
        L.append("claims under %s:" % lex["name"])
        for k, (st, ev) in sorted(cl[lex["name"]].items()):
            L.append("  %-5s %-10s %s" % (k, st, json.dumps(ev)))
    L.append("")
    L.append("nulls:")
    for k, (st, ev) in sorted(nl.items()):
        L.append("  %-3s %-14s %s" % (k, st, json.dumps(ev)))
    L.append("")
    L.append("decision strings logged (section 9): " + "; ".join(
        "%s=%r" % (c, cases[c]["decision"]) for c in sorted(cases)))
    return "\n".join(L)


def run(cases_path, responses_path, codings_path=None):
    cases = {c["case_id"]: c for c in prompts.load_cases(cases_path)}
    lexes = [nz.load_lexicon(nz.PRIMARY), nz.load_lexicon(nz.ALT)]
    for lex in lexes:
        LEX[lex["name"]] = lex
    rows = load_responses(responses_path, cases)
    codings = None
    if codings_path:
        codings = [json.loads(l) for l in open(codings_path) if l.strip()]
    scored = score_rows(rows, cases, lexes)
    cl = {lex["name"]: claims(scored, cases, lex["name"]) for lex in lexes}
    nl = nulls(scored, cases, codings, lexes)
    return cases, scored, cl, nl, lexes


def main(argv):
    if "--selftest" in argv:
        import selftest_apm
        return selftest_apm.main()
    if len(argv) < 2:
        print(__doc__)
        return 2
    cases, scored, cl, nl, lexes = run(argv[0], argv[1], argv[2] if len(argv) > 2 else None)
    print(report(cases, scored, cl, nl, lexes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
