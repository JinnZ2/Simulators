#!/usr/bin/env python3
# register_audit.py -- checks on driver_hours_evidence_register.py.
# CC0, stdlib only, no network.
#
# WHAT THIS DOES
#     The register is a Python object, so this IMPORTS it rather than
#     parsing it: SOURCES, QUESTIONS and RULES are read as the objects
#     they are, and no figure from the register is retyped here as a
#     literal (asserted by the suite). Every check below is arithmetic or
#     set logic over the register's own declarations.
#
# WHAT IT DOES NOT DO
#     It checks no claim about driving, fatigue, tenure or any vendor.
#     Every source in the register is CARRIED -- located by a search pass
#     this environment cannot repeat, the egress gate refusing every
#     publisher host -- and several are marked UNREAD by the register
#     itself. Nothing here reads a primary source or rules on one.
#     It checks whether the register is consistent with its own rules.
#
# usage:
#     python3 register_audit.py
#     python3 register_audit.py --json
#     python3 register_audit.py --selftest

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE]

import driver_hours_evidence_register as REG                    # noqa: E402


def _import(relpath, name):
    """Import a module whose folder name is not an identifier."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, relpath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# n_eff. IMPORTED, not reimplemented: a shared-node count is exactly what
# effective-redundancy-audit exists to compute, and a second copy is the
# drift this tree has a checker for. Channel takes a DECLARED boolean --
# the coder's call -- so the mechanical part (author overlap) and the
# reading (that overlap collapses two channels into one) stay apart.
_ER = _import("effective-redundancy-audit/effective_redundancy.py", "_er")

_NS = _import("sheet-structure-scan/no_severity.py", "_no_sev")


# ---------------------------------------------------------------- helpers

def _declared(heading):
    """Pull a declared vocabulary out of the register's own docstring."""
    block = re.search(heading + r".*?\n\n", REG.__doc__, re.S)
    if not block:
        raise AssertionError("vocabulary block not found: " + heading)
    return re.findall(r"^  ([A-Z_0-9]+)\s{2,}", block.group(0), re.M)


def _surnames(cite):
    """Name tokens ahead of the year. A citation string, not a name index:
    two different people sharing a surname read as one, and one person
    spelled two ways reads as two. Stated because the only positive this
    returns is a SUBSET relation over three tokens, which survives both."""
    return set(x.strip() for x in cite.split("(")[0].split(",") if x.strip())


# ---------------------------------------------------------------- checks

def status_vocabulary():
    """AGA_020 -- the register declares ONE scale and runs TWO. SOURCES
    and QUESTIONS use disjoint token sets, and the token carrying three of
    the eight question verdicts is on neither declared list."""
    declared = _declared("Status scale")
    in_sources, in_questions = set(), set()
    for s in REG.SOURCES.values():
        in_sources |= set(re.findall(r"\b[A-Z_]{4,}\b", s["status"]))
    for q in REG.QUESTIONS:
        in_questions |= set(re.findall(r"\b[A-Z_]{4,}\b", q[3]))
    return dict(declared=declared,
                in_sources=sorted(in_sources),
                in_questions=sorted(in_questions),
                unused_anywhere=[d for d in declared
                                 if d not in in_sources | in_questions],
                undeclared=sorted((in_sources | in_questions) - set(declared)))


def frame_vocabulary():
    """AGA_022 -- 'every source carries one', and the sources that do not."""
    declared = _declared("Sampling-frame flags")
    rule = re.search(r"Sampling-frame flags \(([^)]*)\)", REG.__doc__).group(1)
    used = set()
    for s in REG.SOURCES.values():
        used |= set(s["frame"])
    missing = [k for k, s in REG.SOURCES.items() if not s["frame"]]
    return dict(declared=declared, stated_rule=rule,
                undeclared=sorted(used - set(declared)),
                unused=sorted(set(declared) - used),
                sources_without_a_flag=missing,
                unknown_member_exists=any("UNKNOWN" in d for d in declared))


def question_refs():
    """Every source id a question names resolves; which sources none names."""
    referenced, unresolvable = set(), []
    for qid, _q, srcs, _st, _nx in REG.QUESTIONS:
        for s in srcs:
            referenced.add(s)
            if s not in REG.SOURCES:
                unresolvable.append((qid, s))
    return dict(unresolvable=unresolvable,
                unreferenced=sorted(set(REG.SOURCES) - referenced),
                n_sources=len(REG.SOURCES), n_questions=len(REG.QUESTIONS))


def author_overlap():
    """AGA_021 (mechanical half) -- citation strings sharing name tokens."""
    pairs = []
    keys = list(REG.SOURCES)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            sa, sb = _surnames(REG.SOURCES[a]["cite"]), _surnames(REG.SOURCES[b]["cite"])
            shared = sa & sb
            if shared:
                pairs.append(dict(a=a, b=b, shared=sorted(shared),
                                  subset=sa <= sb or sb <= sa,
                                  frames_equal=(sorted(REG.SOURCES[a]["frame"])
                                                == sorted(REG.SOURCES[b]["frame"]))))
    return pairs


def question_n_eff():
    """AGA_021 (the reading) -- nominal source count against n_eff, per
    question, through effective-redundancy-audit's own arithmetic. The
    collapse boolean is DECLARED from the mechanical overlap above; it is
    a reading, and a reader who holds two papers by one group to be two
    independent readings gets n_eff == n_nominal and the check says so."""
    out = {}
    for qid, _q, srcs, _st, _nx in REG.QUESTIONS:
        if not srcs:
            out[qid] = dict(n_nominal=0, n_eff=None, collapsed=[])
            continue
        chans, collapsed = [], []
        for s in srcs:
            shares = any(s != o and _surnames(REG.SOURCES[s]["cite"])
                         & _surnames(REG.SOURCES[o]["cite"]) for o in srcs)
            if shares:
                collapsed.append(s)
            chans.append(_ER.Channel(name=s, survives_all_shared_nodes=not shares))
        case = _ER.Case(name=qid, domain="driver-hours", outcome="held",
                        channels=chans)
        out[qid] = dict(n_nominal=case.n_nominal, n_eff=case.n_eff,
                        collapsed=collapsed)
    return out


def qe_scope():
    """AGA_023 -- QE's own sentence, counted against the frames."""
    claim = [q for q in REG.QUESTIONS if q[0] == "QE"][0][4]
    onroad = [k for k, s in REG.SOURCES.items() if "ON_ROAD" in s["frame"]]
    notsample = [k for k, s in REG.SOURCES.items()
                 if set(s["frame"]) & {"VENDOR", "N_OF_1", "ARCHIVE"}]
    noflag = [k for k, s in REG.SOURCES.items() if not s["frame"]]
    samples = [k for k in REG.SOURCES if k not in notsample]
    return dict(claim=claim, as_written=(len(onroad), len(REG.SOURCES)),
                not_a_sample=notsample, no_flag=noflag,
                over_samples=(len(onroad), len(samples)),
                blocked_by=noflag)


def frame_definition_fit():
    """AGA_024 -- does an ON_ROAD source's `where` match ON_ROAD's own
    definition? The definition names a METHOD (interviewed while working);
    the flag is carried for a CONSEQUENCE (survivorship)."""
    defn = re.search(r"ON_ROAD\s+(.*?)\n", REG.__doc__).group(1).strip()
    method = re.compile(r"interview|survey|rest area|truck stop|"
                        r"inspection|weigh station|roadside", re.I)
    rows = []
    for k, s in REG.SOURCES.items():
        if "ON_ROAD" not in s["frame"]:
            continue
        unknown = s["where"].strip() == "?"
        rows.append(dict(src=k, where=s["where"], where_unknown=unknown,
                         matches_definition=(None if unknown
                                             else bool(method.search(s["where"])))))
    return dict(definition=defn, rows=rows,
                mismatched=[r["src"] for r in rows
                            if not r["matches_definition"] and not r["where_unknown"]])


def holds_kinds():
    """AGA_025 -- `holds` carries findings and reading-state notes in one
    list with no field between them."""
    state = re.compile(r"UNREAD|UNCONFIRMED|NOT\s+SEARCHED|UNSEARCHED|"
                       r"not in relays", re.I)
    per, total, notes = {}, 0, 0
    for k, s in REG.SOURCES.items():
        n = sum(1 for h in s["holds"] if state.search(h))
        per[k] = dict(n_holds=len(s["holds"]), n_state=n,
                      all_state=(n == len(s["holds"])))
        total += len(s["holds"])
        notes += n
    return dict(per_source=per, total_holds=total, state_notes=notes,
                findings=total - notes,
                sources_with_no_finding=[k for k, v in per.items() if v["all_state"]])


def nested_rates():
    """AGA_026 -- S2's past-year rate must not exceed its ever rate."""
    holds = REG.SOURCES["S2"]["holds"]
    ever = float(re.search(r"([\d.]+)%", holds[0]).group(1))
    past = float(re.search(r"([\d.]+)%", holds[1]).group(1))
    return dict(ever=ever, past_year=past, nested=past <= ever,
                ratio=round(past / ever, 3))


def aurora_provenance():
    """AGA_027 -- the register gives these facts a source; AGA_016 records
    that the seed's pointer named a sibling that does not carry them.
    Distinctive terms only: a bare '40%' matches the Komatsu tire figure,
    a different quantity (see AGA_030)."""
    terms = ["observer", "roadside", "Paccar", "Fort Worth"]
    docs = sorted(f for f in os.listdir(HERE) if f.endswith(".md"))
    where = {}
    for t in terms:
        hits = []
        for d in docs:
            with open(os.path.join(HERE, d)) as fh:
                if re.search(re.escape(t), fh.read(), re.I):
                    hits.append(d)
        where[t] = hits
    return dict(register_cite=REG.SOURCES["S9"]["cite"],
                register_frame=REG.SOURCES["S9"]["frame"],
                term_locations=where,
                in_demo_corpus=[t for t, v in where.items()
                                if "DEMO_CORPUS_AUDIT.md" in v])


def hos_sizing():
    """AGA_028 -- S9's headline derives a speed; the advantage it names
    cannot be sized, because no driving-hours limit is stated anywhere in
    the register or in any document in this folder."""
    h = REG.SOURCES["S9"]["holds"][0]
    mi = float(re.search(r"([\d,]+) mi", h).group(1).replace(",", ""))
    hr = float(re.search(r"([\d.]+) h\b", h).group(1))
    blob = repr(REG.SOURCES) + REG.__doc__ + repr(REG.QUESTIONS) + repr(REG.RULES)
    limit = re.compile(r"\b11[- ]hour|\b11 h\b|driving limit|"
                       r"maximum driving", re.I)

    # The DELIVERED corpus and this audit's own output are scanned apart.
    # Writing AGA_028 down put the phrase "driving-hours limit" into a .md
    # file in this folder, and the next run read it back as a presence --
    # the audit reading its own writing as evidence. An exclude list would
    # hide that; two columns print it. The delivered list is IMPORTED from
    # audit.DOC, not retyped.
    import audit as _AUD
    delivered = set(_AUD.DOC.values())
    corpus, authored = "", {}
    for d in sorted(f for f in os.listdir(HERE) if f.endswith(".md")):
        with open(os.path.join(HERE, d)) as fh:
            text = fh.read()
        if d in delivered:
            corpus += text
        elif limit.search(text):
            authored[d] = len(limit.findall(text))
    return dict(miles=mi, hours=hr, mph=round(mi / hr, 1),
                hos_mentions=len(re.findall(r"\bHOS\b", blob)),
                off_duty_figure_stated=bool(re.search(r"< 10 h off", blob)),
                driving_limit_in_register=bool(limit.search(blob)),
                driving_limit_in_delivered=bool(limit.search(corpus)),
                n_delivered_scanned=len(delivered),
                limit_phrase_in_audit_files=authored)


def self_date():
    """AGA_029 -- the register's own date against AGA_008's six."""
    d = re.search(r"Built (\d{4}-\d{2}-\d{2})", REG.__doc__).group(1)
    dated = {}
    for f in sorted(x for x in os.listdir(HERE) if x.endswith(".md")):
        with open(os.path.join(HERE, f)) as fh:
            m = re.findall(r"20\d\d-\d\d-\d\d", fh.read())
        if m:
            dated[f] = max(m)
    return dict(register=d, documents=dated,
                matches_documents=d in set(dated.values()))


def headline_count():
    """The register's own closing number, recomputed, plus the two cells
    that are UNMEASURED and sourced at once."""
    un = [q[0] for q in REG.QUESTIONS if q[3].startswith("UNMEASURED")]
    sourced = [q[0] for q in REG.QUESTIONS if q[2]]
    return dict(unmeasured=un, n_unmeasured=len(un),
                n_questions=len(REG.QUESTIONS),
                sourced=sourced,
                unmeasured_and_sourced=[q for q in un if q in sourced])


def findings():
    return {
        "AGA_020_status_vocabulary": status_vocabulary(),
        "AGA_021_author_overlap": author_overlap(),
        "AGA_021_question_n_eff": question_n_eff(),
        "AGA_022_frame_vocabulary": frame_vocabulary(),
        "AGA_023_qe_scope": qe_scope(),
        "AGA_024_frame_definition_fit": frame_definition_fit(),
        "AGA_025_holds_kinds": holds_kinds(),
        "AGA_026_nested_rates": nested_rates(),
        "AGA_027_aurora_provenance": aurora_provenance(),
        "AGA_028_hos_sizing": hos_sizing(),
        "AGA_029_self_date": self_date(),
        "question_refs": question_refs(),
        "headline_count": headline_count(),
    }


# ---------------------------------------------------------------- render

def render(f):
    out = []
    p = out.append
    p("REGISTER AUDIT -- driver_hours_evidence_register.py")
    p("Imported, not parsed. Nothing below reads a primary source.\n")

    sv = f["AGA_020_status_vocabulary"]
    p("AGA_020  status scale: %d declared, %d in SOURCES, %d in QUESTIONS"
      % (len(sv["declared"]), len(sv["in_sources"]), len(sv["in_questions"])))
    p("    declared        : %s" % ", ".join(sv["declared"]))
    p("    used in sources : %s" % ", ".join(sv["in_sources"]))
    p("    used nowhere    : %s" % (", ".join(sv["unused_anywhere"]) or "none"))
    p("    undeclared      : %s\n" % (", ".join(sv["undeclared"]) or "none"))

    p("AGA_021  citation strings sharing name tokens")
    for pr in f["AGA_021_author_overlap"]:
        p("    %s & %s share %s   subset: %s   same frame: %s"
          % (pr["a"], pr["b"], ", ".join(pr["shared"]),
             pr["subset"], pr["frames_equal"]))
    p("    nominal sources vs n_eff, per question (n_eff imported):")
    for qid, v in f["AGA_021_question_n_eff"].items():
        if v["n_nominal"]:
            p("      %-3s n_nominal %d -> n_eff %s   collapsed: %s"
              % (qid, v["n_nominal"], v["n_eff"],
                 ", ".join(v["collapsed"]) or "none"))
    p("")

    fv = f["AGA_022_frame_vocabulary"]
    p("AGA_022  frame flags: rule is '%s'" % fv["stated_rule"])
    p("    declared: %s" % ", ".join(fv["declared"]))
    p("    sources carrying no flag: %s"
      % (", ".join(fv["sources_without_a_flag"]) or "none"))
    p("    an UNKNOWN member exists: %s\n" % fv["unknown_member_exists"])

    qe = f["AGA_023_qe_scope"]
    p("AGA_023  QE states: %s" % qe["claim"])
    p("    as written    : %d of %d sources carry ON_ROAD" % qe["as_written"])
    p("    not a sample  : %s" % ", ".join(qe["not_a_sample"]))
    p("    over samples  : %d of %d" % qe["over_samples"])
    p("    what stops it being all of them: %s\n"
      % (", ".join(qe["blocked_by"]) or "nothing"))

    fd = f["AGA_024_frame_definition_fit"]
    p("AGA_024  ON_ROAD is defined as: %s" % fd["definition"])
    for r in fd["rows"]:
        fit = ("where UNKNOWN" if r["where_unknown"]
               else ("yes" if r["matches_definition"] else "NO"))
        p("    %-3s %-46s fits definition: %s"
          % (r["src"], r["where"][:46], fit))
    p("    carries the flag, does not fit the definition: %s\n"
      % (", ".join(fd["mismatched"]) or "none"))

    hk = f["AGA_025_holds_kinds"]
    p("AGA_025  holds entries: %d findings, %d reading-state notes, %d total"
      % (hk["findings"], hk["state_notes"], hk["total_holds"]))
    p("    sources whose holds are ALL reading-state: %s\n"
      % (", ".join(hk["sources_with_no_finding"]) or "none"))

    nr = f["AGA_026_nested_rates"]
    p("AGA_026  S2 rates: ever %.1f%%, past-year %.1f%%, nested %s (ratio %.3f)\n"
      % (nr["ever"], nr["past_year"], nr["nested"], nr["ratio"]))

    ap = f["AGA_027_aurora_provenance"]
    p("AGA_027  S9 cite: %s  [%s]"
      % (ap["register_cite"], ", ".join(ap["register_frame"])))
    for t, v in ap["term_locations"].items():
        p("    %-11s in: %s" % (t, ", ".join(v) or "(no folder document)"))
    p("    in DEMO_CORPUS_AUDIT: %s\n"
      % (", ".join(ap["in_demo_corpus"]) or "none of them"))

    hs = f["AGA_028_hos_sizing"]
    p("AGA_028  S9 headline: %g mi in %g h -> %.1f mph sustained"
      % (hs["miles"], hs["hours"], hs["mph"]))
    p("    'HOS' named %d times; off-duty figure stated: %s"
      % (hs["hos_mentions"], hs["off_duty_figure_stated"]))
    p("    a driving-hours limit in the register: %s"
      % hs["driving_limit_in_register"])
    p("    a driving-hours limit in any of the %d delivered documents: %s"
      % (hs["n_delivered_scanned"], hs["driving_limit_in_delivered"]))
    p("    the phrase in this audit's own output: %s  (UNI_010, printed "
      "rather than excluded)\n"
      % (", ".join("%s x%d" % (k, v)
                   for k, v in hs["limit_phrase_in_audit_files"].items())
         or "none"))

    sd = f["AGA_029_self_date"]
    p("AGA_029  register dates itself %s; documents date %s"
      % (sd["register"], ", ".join(sorted(set(sd["documents"].values())))))
    p("    register shares a date with the documents: %s\n"
      % sd["matches_documents"])

    qr = f["question_refs"]
    p("refs     %d sources, %d questions; unresolvable ids: %s"
      % (qr["n_sources"], qr["n_questions"], qr["unresolvable"] or "none"))
    p("    named by no question: %s" % ", ".join(qr["unreferenced"]))

    hc = f["headline_count"]
    p("count    %d of %d questions UNMEASURED (%s)"
      % (hc["n_unmeasured"], hc["n_questions"], ", ".join(hc["unmeasured"])))
    p("    UNMEASURED and sourced at once: %s"
      % ", ".join(hc["unmeasured_and_sourced"]))
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv[1:]:
        import test_register
        return test_register.main()
    f = findings()
    if "--json" in argv[1:]:
        print(json.dumps(f, indent=2))
    else:
        print(render(f))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
