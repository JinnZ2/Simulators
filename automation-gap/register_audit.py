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

import ast
import importlib.util
import inspect
import json
import math
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
    """Pull a declared vocabulary out of the register's own docstring.

    The separator is ONE OR MORE spaces, not two. The rung names are
    padded to a column, so the LONGEST name sits one space from its
    description -- and a `\s{2,}` rule silently drops exactly the longest
    entry, which is the one most likely to be the newest. It did: the
    revision adding EXPLORATION (11 chars, the longest rung) read as six
    rungs against a docstring declaring seven, which would have reported
    AGA_044 as still open. Recorded at AGA_051.

    Continuation lines are excluded by requiring the token to be followed
    by lower-case prose on the same line rather than by end-of-line."""
    block = re.search(heading + r".*?\n\n", REG.__doc__, re.S)
    if not block:
        raise AssertionError("vocabulary block not found: " + heading)
    return re.findall(r"^  ([A-Z_0-9]+) +(?=\S)", block.group(0), re.M)


def _surnames(cite):
    """Name tokens ahead of the year. A citation string, not a name index:
    two different people sharing a surname read as one, and one person
    spelled two ways reads as two. Stated because the only positive this
    returns is a SUBSET relation over three tokens, which survives both."""
    return set(x.strip() for x in cite.split("(")[0].split(",") if x.strip())


# ---------------------------------------------------------------- checks

_SRC = None


def _source():
    """The delivered file's own text, read once and closed. Five checks
    read it; five bare open().read() calls leaked five handles and printed
    five ResourceWarnings into the suite's output."""
    global _SRC
    if _SRC is None:
        with open(os.path.join(HERE, "driver_hours_evidence_register.py")) as fh:
            _SRC = fh.read()
    return _SRC


def _rung_on_an_entry(rung):
    """Is a declared status rung carried by any FIELD, anywhere in the
    register -- a status slot, an inline [TAG], a list entry? A rung a
    reader can find only in the docstring is declared and not applied,
    and the two are different states."""
    blob = " ".join([str(getattr(REG, n, ""))
                     for n in dir(REG) if not n.startswith("_")])
    return bool(re.search(r"\b%s\b" % re.escape(rung), blob))


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

    # Two further sites the scale reaches, by a different MECHANISM: an
    # inline [TAG] inside free-text prose, in a `holds` entry or a
    # TERM_NOTES field. A `status` field is a slot; a bracket in a
    # sentence is not, and a reader looking at the declared scale has no
    # way to know the second exists.
    tag = re.compile(r"\[([A-Z_]{4,})[^\]]*\]")
    in_holds, in_term_notes = set(), set()
    for s in REG.SOURCES.values():
        for h in s["holds"]:
            in_holds |= set(tag.findall(h))
    for t in getattr(REG, "TERM_NOTES", {}).values():
        for v in t.values():
            in_term_notes |= set(tag.findall(str(v)))

    # The addenda added more prose-tag sites: an addendum question status,
    # a control-loop failure mode, the transfer note, a function docstring.
    in_addendum = set()
    for obj in ("ADDENDUM_QUESTIONS", "CONTROL_LOOPS", "TRANSFER_NOTE"):
        in_addendum |= set(tag.findall(str(getattr(REG, obj, ""))))
    doc = getattr(REG, "p_uninterrupted", None)
    if doc is not None and doc.__doc__:
        in_addendum |= set(tag.findall(doc.__doc__))

    everywhere = (in_sources | in_questions | in_holds | in_term_notes
                  | in_addendum)
    return dict(declared=declared,
                in_sources=sorted(in_sources),
                in_questions=sorted(in_questions),
                in_holds_tags=sorted(in_holds),
                in_term_notes=sorted(in_term_notes),
                in_addendum=sorted(in_addendum),
                n_sites=sum(1 for x in (in_sources, in_questions, in_holds,
                                        in_term_notes, in_addendum) if x),
                unused_in_a_status_slot=[d for d in declared
                                         if d not in in_sources | in_questions],
                unused_anywhere=[d for d in declared if d not in everywhere],
                undeclared=sorted(everywhere - set(declared)))


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


def relay_provenance():
    """AGA_033 -- a source whose provenance is ANOTHER source in the
    register. The relation is stated in prose after the year, so the
    surname overlap in author_overlap() cannot see it: S11 and the source
    that summarises it share every author S11 has, which is none of its
    own. A second shared node, invisible to the mechanical check."""
    rel = re.compile(r"as (?:summaris|summariz|report|relay|cit)ed in\s+"
                     r"([A-Z][A-Za-z]+)", re.I)
    out = []
    for k, s in REG.SOURCES.items():
        m = rel.search(s["cite"])
        if not m:
            continue
        lead = m.group(1)
        through = [o for o, t in REG.SOURCES.items()
                   if o != k and t["cite"].split("(")[0].strip().startswith(lead)]
        seen_by_surname = any(
            {lead} & _surnames(REG.SOURCES[o]["cite"]) and
            _surnames(s["cite"]) & _surnames(REG.SOURCES[o]["cite"])
            for o in through)
        out.append(dict(src=k, relayed_through=through, named=lead,
                        caught_by_author_overlap=seen_by_surname))
    return out


def term_note_scope():
    """AGA_034 -- the TERM_DRIFT flag against the sources the note's own
    `fix` field says are affected."""
    notes = getattr(REG, "TERM_NOTES", {})
    flagged = [k for k, s in REG.SOURCES.items() if "TERM_DRIFT" in s["frame"]]
    named = set()
    for t in notes.values():
        named |= set(re.findall(r"\bS\d+\b", str(t.get("fix", ""))))
    qi = [q for q in REG.QUESTIONS if q[0] == "QI"]
    return dict(n_notes=len(notes), flagged=flagged,
                named_in_fix=sorted(named, key=lambda x: int(x[1:])),
                named_but_unflagged=sorted(named - set(flagged),
                                           key=lambda x: int(x[1:])),
                flagged_but_unnamed=sorted(set(flagged) - named),
                qi_sources=(qi[0][2] if qi else None))


def open_but_uncounted():
    """AGA_035 -- the register's closing number counts one token, and the
    revision added two open questions under tokens it does not count. The
    headline falls as a fraction because open cells were added."""
    counted, open_other, answered = [], [], []
    for q in REG.QUESTIONS:
        st = q[3]
        if st.startswith("UNMEASURED"):
            counted.append(q[0])
        elif st.startswith("SUPPORTED"):
            answered.append(q[0])
        else:
            open_other.append((q[0], st.split()[0].rstrip("-").strip()))
    n = len(REG.QUESTIONS)
    # The addenda put further questions in a SEPARATE list, which main()
    # does not count and question_refs() does not reach.
    outside = [(q[0], q[3].split()[0].rstrip("-").strip())
               for q in getattr(REG, "ADDENDUM_QUESTIONS", [])]
    total = n + len(outside)
    return dict(counted=counted, answered=answered, open_uncounted=open_other,
                n_questions=n, outside_the_counted_list=outside,
                n_all_questions=total,
                headline="%d of %d" % (len(counted), n),
                not_answered="%d of %d" % (total - len(answered), total))


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


# --------------------------------------------------------- ADDENDUM_3.md
# A second DELIVERED document, in notes rather than Python. It is read as
# delivered and the register is read as delivered; where the two disagree
# that is reported, not resolved. Nothing here transcribes one into the
# other.

NOTE3 = os.path.join(HERE, "ADDENDUM_3.md")


def _note3():
    with open(NOTE3, encoding="utf-8") as fh:
        return fh.read()


def _x1_fields():
    body = _note3().split("ADDENDUM 3")[-1]
    out = {}
    for line in body.splitlines():
        m = re.match(r"\s{2,}(\w+)\s{2,}(.+)", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def delivered_tail():
    """AGA_052 -- the delivered file carries a duplicated tail: the
    addendum3 body appears a second time inside the first __main__ block,
    followed by a second __main__ block. Landed as delivered and reported
    rather than repaired. The duplication is entirely inside __main__, so
    the IMPORTABLE surface is untouched -- every object is defined once
    and this audit, which imports, is unaffected."""
    import subprocess
    src = _source()
    tree = ast.parse(src)
    top = [n.targets[0].id for n in tree.body
           if isinstance(n, ast.Assign) and len(n.targets) == 1
           and isinstance(n.targets[0], ast.Name)]
    funcs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    out = subprocess.run([sys.executable,
                          os.path.join(HERE,
                                       "driver_hours_evidence_register.py")],
                         capture_output=True, text=True, timeout=60).stdout
    return dict(
        main_blocks=src.count('if __name__ == "__main__":'),
        register_header_printed=out.count(
            "DRIVER HOURS / FATIGUE / TENURE -- evidence register"),
        addendum3_header_printed=out.count(
            "ADDENDUM 3 -- EXPLORATION TERRITORY (relevance unknown)"),
        top_level_objects=len(top), duplicate_objects=len(top) - len(set(top)),
        duplicate_functions=len(funcs) - len(set(funcs)),
        importable_surface_intact=(len(top) == len(set(top))
                                   and len(funcs) == len(set(funcs))))


def exploration_rung_site():
    """AGA_053 + the rung's own application site. The section is titled
    EXPLORATION in a COMMENT and the rung reaches no entry field; the
    list's NAME is where it is applied. And X2's own relevance field
    contradicts the rung's definition and the section header."""
    src = _source()
    defn = re.search(r"EXPLORATION (.*?)\n\nSampling", REG.__doc__,
                     re.S).group(1)
    defn = " ".join(defn.split())
    hdr = re.search(r"# ADDENDUM 3 -- EXPLORATION TERRITORY.*?\n# ={10,}",
                    src, re.S).group(0)
    rows = []
    for x in getattr(REG, "EXPLORATION", []):
        rel = x.get("relevance", "")
        rows.append(dict(xid=x.get("xid"), relevance=rel,
                         says_unknown=rel.strip().upper().startswith("UNKNOWN"),
                         says_direct="DIRECT" in rel.upper(),
                         fields=sorted(x)))
    return dict(rung_definition=defn,
                definition_says_unknown="UNKNOWN" in defn,
                definition_says_not_load_bearing="load-bearing" in defn,
                header_says_unknown="UNKNOWN" in hdr,
                header_says_not_load_bearing="Not load-bearing" in hdr,
                entries=rows,
                contradicting=[r["xid"] for r in rows if r["says_direct"]],
                rung_on_any_entry_field=any(
                    "EXPLORATION" in str(v) for x in getattr(REG, "EXPLORATION", [])
                    for v in x.values()),
                applied_by_the_list_name=hasattr(REG, "EXPLORATION"))


def per_operator_term():
    """AGA_054 -- successor to AGA_045. The per-operator term is now
    DECLARED in the file and reaches no arithmetic: only a print reads
    the list it lives in, and the gate's own window function reads the
    four constants."""
    src = _source()
    tree = ast.parse(src)
    readers = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            for m in ast.walk(n):
                if isinstance(m, ast.Name) and m.id == "SLEEP_QUALITY_FACTORS":
                    readers.add(n.name)
    win = [n for n in tree.body if isinstance(n, ast.FunctionDef)
           and n.name == "g0_window_needed"][0]
    win_src = ast.get_source_segment(src, win)
    gate = [t for t in REG.GATE_MAP if t[0] == "G0"][0]
    return dict(
        factors=[f[0] for f in REG.SLEEP_QUALITY_FACTORS],
        n_factors=len(REG.SLEEP_QUALITY_FACTORS),
        every_factor_states_a_status=all(
            isinstance(f[2], str) and f[2] for f in REG.SLEEP_QUALITY_FACTORS),
        operator_in_gate_entry=bool(re.search(r"\boperator\b",
                                              " ".join(gate), re.I)),
        operator_in_notes=bool(re.search(r"\boperator\b",
                                         " ".join(REG.G0_NOTES), re.I)),
        operator_in_factors=bool(re.search(r"\boperator\b",
                                           str(REG.SLEEP_QUALITY_FACTORS), re.I)),
        readers=sorted(readers),
        reaches_arithmetic=bool(readers - {"addendum2"}),
        window_reads_rest_block_only=("SLEEP_QUALITY" not in win_src
                                      and "REST_BLOCK" in win_src))


def untagged_claim():
    """AGA_055 -- the strongest statement in G0 note 1 carries no tag,
    sitting between one marked OBSERVED and one marked DERIVED."""
    rows = []
    for i, n in enumerate(REG.G0_NOTES):
        for sent in re.split(r"(?<=\.)\s+", n):
            tags = re.findall(r"\[([A-Z_]+)\]", sent)
            rows.append(dict(note=i, tags=tags, text=sent.strip()))
    n1 = [r for r in rows if r["note"] == 0]
    untagged = [r for r in n1 if not r["tags"]]
    return dict(note1_sentences=len(n1),
                note1_tags=[r["tags"] for r in n1],
                untagged=[r["text"] for r in untagged],
                sits_between_tagged=bool(len(n1) >= 3 and n1[0]["tags"]
                                         and not n1[1]["tags"]
                                         and n1[2]["tags"]),
                claim_is_causal=any("not motion itself" in r["text"]
                                    for r in untagged))


def ceiling_split():
    """AGA_056 -- the good-sleeper ceiling is a stated LIMIT in one
    delivered document and a DATUM in the other, and neither carries both.

    The word collides three ways and produced two false positives in this
    check before it was separated (AGA_051):
      "treat as ceiling"          the POISSON bound, a different quantity
      "null in good sleepers"     a description of a study's SAMPLE
      "room to improve / Omlin"   the interpretive LIMIT, the one that
                                  confounds X1's own prediction
    All three are counted apart and printed, and the conclusion is
    computed from the two that matter rather than asserted."""
    note = _note3()
    src = _source()
    x1 = [x for x in getattr(REG, "EXPLORATION", []) if x.get("xid") == "X1"]
    x1 = x1[0] if x1 else {}

    limit = re.compile(r"room to improve|Omlin|only show in|"
                       r"baseline must be recorded", re.I)
    sample = re.compile(r"good sleeper", re.I)
    figure = re.compile(r"\b96%|baseline efficiency", re.I)

    def read(text):
        return dict(states_the_limit=bool(limit.search(text)),
                    mentions_good_sleepers=bool(sample.search(text)),
                    carries_the_figure=bool(figure.search(text)))

    n, r = read(note), read(src)
    return dict(
        note=n, register=r,
        poisson_ceiling_in_register=(
            "Poisson overstates usable windows -- treat as ceiling" in src),
        word_ceiling_in_register=src.count("ceiling"),
        register_figure=(re.search(r"overnight null[^;]*",
                                   str(x1.get("half_a", ""))).group(0)
                         if "overnight null" in str(x1.get("half_a", ""))
                         else None),
        x1_scope_carries_the_limit=bool(limit.search(str(x1.get("scope", "")))),
        note_has_both=(n["states_the_limit"] and n["carries_the_figure"]),
        register_has_both=(r["states_the_limit"] and r["carries_the_figure"]),
        neither_has_both=not (
            (n["states_the_limit"] and n["carries_the_figure"])
            or (r["states_the_limit"] and r["carries_the_figure"])))


def x1_drift():
    """AGA_057 -- one record, two delivered documents, different field
    names and different content."""
    note = _note3()
    body = note.split("ADDENDUM 3")[-1]
    nf = set(re.findall(r"\s{2,}(\w+)\s{2,}", body))
    x1 = [x for x in getattr(REG, "EXPLORATION", []) if x.get("xid") == "X1"]
    x1 = x1[0] if x1 else {}
    note_fields = {}
    for line in body.splitlines():
        m = re.match(r"\s{2,}(\w+)\s{2,}(.+)", line)
        if m:
            note_fields[m.group(1)] = m.group(2).strip()
    return dict(note_fields=sorted(nf), register_fields=sorted(x1),
                only_in_note=sorted(nf - set(x1)),
                only_in_register=sorted(set(x1) - nf),
                half_a_note_chars=len(note_fields.get("half_a", "")),
                half_a_register_chars=len(str(x1.get("half_a", ""))),
                register_names_studies=bool(
                    re.search(r"\b(19|20)\d\d\b", str(x1.get("half_a", "")))),
                note_names_studies=bool(
                    re.search(r"\b(19|20)\d\d\b", note_fields.get("half_a", ""))))


def x2_disciplines():
    """AGA_058 -- what holds in X2: a consent limit, and a prediction that
    is this tree's observer-exclusion shape stated in the author's own
    words."""
    x2 = [x for x in getattr(REG, "EXPLORATION", []) if x.get("xid") == "X2"]
    x2 = x2[0] if x2 else {}
    return dict(
        scope=x2.get("scope"),
        scope_is_a_consent_limit=("choose to share" in str(x2.get("scope", ""))),
        first_consent_limit_in_the_register=not any(
            "consent" in str(v).lower() or "choose to share" in str(v).lower()
            for s in REG.SOURCES.values() for v in s.values()),
        prediction=x2.get("prediction"),
        prediction_is_selection_on_the_outcome=(
            "had trouble" in str(x2.get("prediction", ""))
            and "got studied" in str(x2.get("prediction", ""))),
        half_a_frame=("settler" in str(x2.get("half_a", ""))
                      and "DISRUPTION" in str(x2.get("half_a", ""))),
        join=x2.get("join"))


def falsifier_wording():
    """AGA_059 -- a defect in this audit's own claim table. AGA_020's
    falsifier reads *a source carrying DERIVED*. The v7 revision put
    `[DERIVED]` inside a SOURCE's `holds` list, so the wording fires -- for
    the SECOND time, by the same mechanism, in a claim whose own body
    records the first firing and then restates the ambiguous wording
    verbatim rather than sharpening it. What the claim means is a status
    SLOT; what it asks for is a token, and a token is cheap."""
    tag = re.compile(r"\[([A-Z_]{4,})[^\]]*\]")
    slot, in_holds = set(), {}
    for sid, s in REG.SOURCES.items():
        slot |= set(re.findall(r"\b[A-Z_]{4,}\b", s["status"]))
        hits = set()
        for h in s["holds"]:
            hits |= set(tag.findall(h))
        if "DERIVED" in hits:
            in_holds[sid] = [h for h in s["holds"] if "[DERIVED]" in h]
    def block(text):
        if "**AGA_020" not in text:
            return "", ""
        b = text.split("**AGA_020")[1].split("**AGA_021")[0]
        f = b.rsplit("*Falsifier:*", 1)[-1] if "*Falsifier:*" in b else ""
        return b, f

    now, _ = _claim_table()
    body, fals = block(now)
    before, fals_before = block(_claim_table_at_head())
    def names_the_field(t):
        return "`status` field" in t
    return dict(
        a_source_carries_derived_as_a_tag=sorted(in_holds),
        derived_in_any_status_slot="DERIVED" in slot,
        entries=[h for v in in_holds.values() for h in v],
        # The fault is in HISTORY, so it is read out of git rather than
        # asserted: the falsifier AS IT STOOD when v7 arrived, against the
        # falsifier now. The repair turns the first three False.
        claim_notes_the_ambiguity=("what arrived was a new kind of entry"
                                   in before),
        falsifier_before=" ".join(fals_before.split())[:120],
        falsifier_named_the_token_only=(bool(fals_before)
                                        and not names_the_field(fals_before)),
        falsifier_now=" ".join(fals.split())[:160],
        falsifier_names_the_field_now=names_the_field(fals),
        repaired=(bool(fals_before) and not names_the_field(fals_before)
                  and names_the_field(fals)),
        fires_on_the_wording=bool(in_holds),
        fires_on_the_meaning="DERIVED" in slot)


def _claim_table():
    ct = os.path.join(HERE, "CLAIM_TABLE.md")
    if not os.path.exists(ct):
        return "", ct
    with open(ct) as fh:
        return fh.read(), ct


def _claim_table_at_head():
    """The claim table as committed. A claim about a wording that has since
    been repaired is checkable only against history; reading it out of git
    makes it a measurement rather than a recollection. Empty string if git
    is unreachable -- then the check reports the repair and not the fault."""
    import subprocess
    try:
        rel = os.path.relpath(os.path.join(HERE, "CLAIM_TABLE.md"),
                              os.path.join(HERE, ".."))
        out = subprocess.run(["git", "show", "HEAD:" + rel],
                             cwd=os.path.join(HERE, ".."),
                             capture_output=True, text=True, timeout=20)
        return out.stdout if out.returncode == 0 else ""
    except Exception:
        return ""


def exploration_tag_site():
    """AGA_061 -- EXPLORATION is a SIXTH inline-tag site and the vocabulary
    check does not scan it. One field carries two rungs."""
    tag = re.compile(r"\[([A-Z_]{4,})[^\]]*\]")
    per_field, multi = {}, []
    for x in getattr(REG, "EXPLORATION", []):
        for k, v in x.items():
            t = tag.findall(str(v))
            if t:
                per_field["%s.%s" % (x["xid"], k)] = t
                if len(set(t)) > 1:
                    multi.append("%s.%s" % (x["xid"], k))
    scanned = set()
    for obj in ("ADDENDUM_QUESTIONS", "CONTROL_LOOPS", "TRANSFER_NOTE"):
        scanned |= set(tag.findall(str(getattr(REG, obj, ""))))
    here = set(t for v in per_field.values() for t in v)
    return dict(fields_carrying_a_tag=sorted(per_field),
                tags=per_field,
                two_rungs_in_one_field=multi,
                tokens_here=sorted(here),
                site_scanned=("EXPLORATION" in _scanned_objects()),
                scanned_objects=_scanned_objects(),
                # every token here also occurs at a site that IS scanned,
                # so the omission changes no reported number today -- which
                # is what makes it silent. A rung appearing only here would
                # read as unused anywhere.
                tokens_new_to_the_file=sorted(
                    here - set(status_vocabulary()["in_addendum"])
                    - set(status_vocabulary()["in_term_notes"])),
                omission_is_silent_today=not (
                    here - set(status_vocabulary()["in_addendum"])
                    - set(status_vocabulary()["in_term_notes"])),
                n_sites_reported=status_vocabulary()["n_sites"])


def _scanned_objects():
    """Which register objects `status_vocabulary` walks for inline tags --
    read off its own source, so a widening there closes this by itself."""
    src = inspect.getsource(status_vocabulary)
    for n in ast.walk(ast.parse(src.lstrip())):
        if isinstance(n, ast.Tuple) and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str)
                for e in n.elts) and len(n.elts) > 1:
            names = [e.value for e in n.elts]
            if any(nm.isupper() for nm in names):
                return names
    return []


def exploration_field_sets():
    """AGA_062 -- two entries in one list, different field sets, no schema.
    The renderer guards with `if k in x`, so an absent field prints exactly
    like a field nobody thought to fill."""
    xs = getattr(REG, "EXPLORATION", [])
    sets = {x["xid"]: set(x) for x in xs}
    union = set().union(*sets.values()) if sets else set()
    src = _source()
    a3 = [n for n in ast.parse(src).body
          if isinstance(n, ast.FunctionDef) and n.name == "addendum3"]
    guarded = bool(a3) and "if k in x" in ast.get_source_segment(src, a3[0])
    # the substantive overlap: X2's new field names X1's whole subject
    x1 = next((x for x in xs if x["xid"] == "X1"), {})
    x2 = next((x for x in xs if x["xid"] == "X2"), {})
    def blob(x):
        return " ".join(str(v) for v in x.values()).lower()
    return dict(
        field_sets={k: sorted(v) for k, v in sets.items()},
        only_in_one=sorted(set().union(
            *[union - v for v in sets.values()]) if sets else []),
        renderer_is_guarded=guarded,
        x2_channels_names_motion="motion" in str(x2.get("channels", "")).lower(),
        x1_is_about_motion=blob(x1).count("motion") >= 3,
        x1_has_a_channels_field="channels" in x1,
        x2_names_x1=bool(re.search(r"\bX1\b", blob(x2).upper())),
        x1_names_x2=bool(re.search(r"\bX2\b", blob(x1).upper())))


def consent_record():
    """AGA_063 -- X2's anchor records what was NOT asked for. The scope
    field declares a consent limit; the anchor records it being honoured,
    which is a different statement and has no precedent here."""
    xs = getattr(REG, "EXPLORATION", [])
    x2 = next((x for x in xs if x["xid"] == "X2"), {})
    anchor = str(x2.get("anchor", ""))
    src = _source()
    return dict(
        anchor=anchor,
        names_the_channels=bool(re.search(r"SCENT and BODY MOTION", anchor)),
        records_categories_only=("categories only" in anchor),
        records_specifics_withheld=("specifics not shared" in anchor),
        records_the_ask_not_made=("none requested" in anchor),
        occurrences_in_the_file=dict(
            (pat, src.lower().count(pat))
            for pat in ("none requested", "not shared", "choose to share")),
        scope_declares_the_limit=("choose to share" in str(x2.get("scope", ""))),
        first_in_the_register=src.lower().count("none requested") == 1)


def imported_skill_arm():
    """AGA_064 -- QE's third arm, against the register's own N_OF_1 rule.
    The rule: an N=1 record BOUNDS WHAT IS POSSIBLE and does not estimate a
    rate. The arm states a possibility, carries a tag, and estimates
    nothing -- so it is inside the rule the register wrote for itself.

    The cost is in the slot, not the claim: S10 carries the arm and QE's
    source list is empty, so the arm reaches the prose and not the map."""
    qe = [q for q in REG.QUESTIONS if q[0] == "QE"][0]
    arm = qe[4].split("Third arm:", 1)[1] if "Third arm:" in qe[4] else ""
    rule = [r for r in REG.RULES if "N_OF_1" in r]
    slot, prose = [], []
    for row in list(REG.QUESTIONS) + list(getattr(REG, "ADDENDUM_QUESTIONS", [])):
        qid, q, srcs, st, nxt = row
        if "S10" in srcs:
            slot.append(qid)
        if re.search(r"\bS10\b", " ".join([q, st, nxt])):
            prose.append(qid)
    return dict(
        arm_present=bool(arm),
        arm_states_a_rate=bool(re.search(r"\d+\s*%|\brate\b|\bof drivers\b", arm)),
        arm_states_a_possibility=bool(re.search(r"\bcan be\b|\bmay\b", arm)),
        arm_tags=re.findall(r"\[([A-Z_]+)\]", arm),
        rule_present=bool(rule),
        obeys_the_rule=(bool(arm) and not
                        re.search(r"\d+\s*%|\brate\b|\bof drivers\b", arm)),
        s10_in_a_source_slot=slot,
        s10_in_free_text=prose,
        leans_without_recording=sorted(set(prose) - set(slot)),
        new_holds=[h for h in REG.SOURCES["S10"]["holds"]
                   if "IMPORTED" in h or "TRAINEE" in h])


def note3_status_rung():
    """AGA_044 -- the note declared a status rung the register's scale did
    not carry. Two delivered documents, one scale, and the scale lived in
    only one of them.

    The check reports the STATE rather than asserting the old one: the
    next revision put EXPLORATION into the docstring scale, so
    `in_register_scale` goes False -> True and the claim closes by
    arrival. What it closes on is discoverability -- a reader of the
    register alone can now find the rung. `carried_by_an_entry` is the
    second half and is still False: the rung is applied by the section
    header the entries sit under, and no entry field states it."""
    note = _note3()
    declared_here = re.findall(r"^\s{2,}([A-Z_]{4,})\s{2,}", note, re.M)
    scale = _declared("Status scale")
    x1 = _x1_fields()
    return dict(note_declares=sorted(set(declared_here) & {"EXPLORATION"}),
                register_scale=scale,
                in_register_scale="EXPLORATION" in scale,
                carried_by_an_entry=_rung_on_an_entry("EXPLORATION"),
                note_says=re.search(r"EXPLORATION\s+(.+)", note).group(1).strip(),
                x1_relevance=x1.get("relevance"),
                x1_fields=sorted(x1))


def note3_gate_axis():
    """AGA_045 -- motion_sleep_history makes G0 a per-OPERATOR gate. The
    register's G0 entry names route and season.

    The two sites are read APART. AGA_045 is a claim about the GATE's own
    axes, so `register_names_operator` reads the gate entry and nothing
    else; the revision then put the operator into the NOTES beside it,
    which is a different statement and is reported as its own field. A
    blob over both would have read the arrival of a note as a change to
    the gate. Where the term goes from there is AGA_054."""
    note = _note3()
    g0 = [t for t in REG.GATE_MAP if t[0] == "G0"][0]
    entry = " ".join(g0)
    blob = entry + " " + " ".join(REG.G0_NOTES)
    return dict(
        note_claims_per_operator=("PASS for one operator" in note
                                  and "FAIL" in note),
        factor="motion_sleep_history" in note,
        register_names_route="route" in blob.lower(),
        register_names_season="season" in blob.lower(),
        register_names_operator=bool(re.search(r"\boperator\b", entry, re.I)),
        operator_in_notes=bool(re.search(r"\boperator\b",
                                         " ".join(REG.G0_NOTES), re.I)),
        rest_block_is_a_constant=isinstance(REG.REST_BLOCK["cycle_min"], int))


def lcd_forfeit():
    """AGA_046 -- 'a blanket rule written to the lowest sleeper forfeits
    the capacity of everyone above it', made a number on the register's
    own placeholder rate. Nothing here is a statement about any operator
    or fleet; the window set is the register's four combinations and the
    mix of operators is unmeasured, so no aggregate is emitted."""
    lam = REG.interrupt_rate(REG.EVENT_CLASSES)
    ws = [(b, i, REG.g0_window_needed(b, i))
          for b in ("nap_min", "cycle_min") for i in ("low", "high")]
    lcd = max(w for _, _, w in ws)
    fleet = REG.p_uninterrupted(lam, lcd)
    rows = []
    for b, i, w in ws:
        own = REG.p_uninterrupted(lam, w)
        rows.append(dict(window="%s/%s" % (b, i), minutes=w, own=own,
                         fleet=fleet, forfeit=own - fleet,
                         share_of_own=(own - fleet) / own if own else None))
    w1 = min(w for _, _, w in ws)
    # d/dlam of exp(-lam*w1/60) - exp(-lam*w2/60) = 0
    lam_star = 60.0 * math.log(lcd / w1) / (lcd - w1)
    gap = lambda L: REG.p_uninterrupted(L, w1) - REG.p_uninterrupted(L, lcd)
    return dict(lam_per_h=lam, lcd_minutes=lcd, rows=rows,
                worst_forfeit=max(r["forfeit"] for r in rows),
                worst_share=max(r["share_of_own"] for r in rows),
                peak_lam=lam_star, peak_forfeit=gap(lam_star),
                share_of_peak=gap(lam) / gap(lam_star),
                sweep=[(L, gap(L)) for L in (0.05, 0.2, lam, lam_star, 1.5, 4.0)],
                vanishes_at_both_ends=(gap(0.01) < gap(lam)
                                       and gap(20.0) < gap(lam)),
                aggregate_emitted=False)


def note3_confound():
    """AGA_047 -- the note carries its own confound and its own repair in
    adjacent sections, and the compressed X1 record drops the one that
    confounds its own prediction."""
    note = _note3()
    scope_sec = note.split("SCOPE LIMITS")[1].split('"not applicable')[0]
    instrument = note.split("CHEAPEST INSTRUMENT")[1].split("SCOPE LIMITS")[0]
    x1 = _x1_fields()
    return dict(
        scope_section_names_stimulus=("lab rocking" in scope_sec
                                      and "truck cab" in scope_sec),
        scope_section_names_ceiling="ceiling" in scope_sec,
        scope_section_names_the_repair="baseline must be recorded" in scope_sec,
        x1_scope=x1.get("scope"),
        x1_scope_carries_stimulus="lab rocking" in (x1.get("scope") or ""),
        x1_scope_carries_ceiling=any(t in (x1.get("scope") or "")
                                     for t in ("ceiling", "baseline")),
        x1_prediction=x1.get("prediction"),
        x1_probe=x1.get("probe"),
        probe_names_baseline="baseline" in (x1.get("probe") or ""),
        instrument_section_names_baseline="baseline" in instrument,
        both_predict_smaller_effect=True,
        repair_is_one_section_above=("baseline must be recorded" in scope_sec
                                     and "baseline" not in instrument))


def note3_halves():
    """AGA_048 -- X1's two halves are both OUTSIDE the register, and the
    frame vocabulary has no flag for the sampling limit it names."""
    note = _note3()
    cites = " ".join(s["cite"].lower() for s in REG.SOURCES.values())
    frames = _declared("Sampling-frame flags")
    return dict(n_sources=len(REG.SOURCES),
                rocking_lab_in_register=any(t in cites
                                            for t in ("rocking", "rock ")),
                infant_carrying_in_register="infant" in cites,
                both_halves_external=not ("rocking" in cites
                                          or "infant" in cites),
                sampling_limit_stated=("young males, lab, Swiss" in note),
                declared_frames=frames,
                a_flag_for_a_narrow_lab_sample=any(
                    t in " ".join(frames).upper()
                    for t in ("LAB", "NARROW", "WEIRD", "DEMOGRAPH")),
                contrast_qj=[q[0] for q in REG.QUESTIONS
                             if q[0] == "QJ" and len(q[2]) > 1])


def note3_crossrefs():
    """AGA_049 -- the note's one wiki-style pointer."""
    note = _note3()
    links = re.findall(r"\[\[([^\]]+)\]\]", note)
    out = {}
    for link in links:
        found = []
        for root, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for f in files:
                if link in f:
                    found.append(os.path.relpath(os.path.join(root, f), ROOT))
        out[link] = found
    return dict(links=links, resolves=out,
                unresolved=[k for k, v in out.items() if not v])


def note3_fencing():
    """AGA_050 -- the flip rests on the operator's own record and is
    fenced four ways rather than promoted."""
    note = _note3()
    flip = note.split("PROPOSED flip")[1].split("STATUS ADDED")[0]
    x1 = _x1_fields()
    return dict(
        flip_rests_on_n_of_1=("your history" in flip),
        labelled_proposed="PROPOSED flip" in note,
        status_is_exploration="EXPLORATION" in note,
        relevance_unknown="UNKNOWN" in (x1.get("relevance") or ""),
        declared_not_load_bearing="not load-bearing" in note,
        anchor_declares_n=("N=1" in (x1.get("anchor") or "")),
        fences=sum([("PROPOSED flip" in note), ("EXPLORATION" in note),
                    "UNKNOWN" in (x1.get("relevance") or ""),
                    "not load-bearing" in note]))


def rest_block_provenance():
    """AGA_039 -- the two parameter blocks the G0 gate runs on carry
    provenance by different means, and only one survives import.
    EVENT_CLASSES (the RATE, the gate's denominator) carries a source
    string as a fourth tuple element, reachable from the object.
    REST_BLOCK (the WINDOW, the gate's numerator) carries it in
    comments, which are not in the object at all: a consumer importing
    the register gets four bare numbers."""
    src = _source()
    block = re.search(r"REST_BLOCK = dict\((.*?)\n\)", src, re.S).group(1)
    rows = {}
    for line in block.splitlines():
        m = re.match(r"\s*(\w+)\s*=", line)
        if m:
            rows[m.group(1)] = []
        if rows:
            c = line.split("#", 1)
            if len(c) == 2:
                rows[list(rows)[-1]].append(c[1].strip())
    graded = {k: (" ".join(v) or None) for k, v in rows.items()}
    placeholder = [k for k, v in graded.items() if v and "PLACEHOLDER" in v]
    unverified = [k for k, v in graded.items()
                  if v and "PLACEHOLDER" not in v and "NOT VERIFIED" in v]
    other = [k for k in graded if k not in placeholder + unverified]
    return dict(fields=sorted(REG.REST_BLOCK),
                comments=graded,
                placeholder=sorted(placeholder),
                literature_unverified=sorted(unverified),
                unclassified=sorted(other),
                provenance_in_the_object=any(
                    isinstance(v, str) for v in REG.REST_BLOCK.values()),
                event_classes_carry_a_source_field=all(
                    isinstance(c[3], str) and c[3] for c in REG.EVENT_CLASSES))


def g0_arithmetic():
    """AGA_040 -- the addendum's G0 block recomputed, and which class the
    rate is carried by. Every input is declared PLACEHOLDER by the
    register itself; nothing here is a statement about any route."""
    classes = REG.EVENT_CLASSES
    lam = REG.interrupt_rate(classes)
    by_class = sorted(((r * pm, name) for name, r, pm, _ in classes),
                      reverse=True)
    raw = sorted(((r, name) for name, r, pm, _ in classes), reverse=True)
    windows = []
    for block in ("nap_min", "cycle_min"):
        for inertia in ("low", "high"):
            w = REG.g0_window_needed(block, inertia)
            windows.append(dict(block=block, inertia=inertia, minutes=w,
                                p=REG.p_uninterrupted(lam, w)))
    worst = min(windows, key=lambda d: d["p"])
    # removing the top contributor: the design lever the notes name
    top = by_class[0][1]
    lam_wo = REG.interrupt_rate([c for c in classes if c[0] != top])
    return dict(lam_per_h=lam, mean_gap_min=60.0 / lam,
                by_contribution=[(n, round(v, 4)) for v, n in by_class],
                highest_raw_rate=raw[0][1], top_contributor=top,
                note_3_holds=(raw[0][1] != top),
                windows=windows, worst=worst,
                lam_without_top=lam_wo,
                p_worst_without_top=REG.p_uninterrupted(lam_wo,
                                                        worst["minutes"]),
                all_placeholder=all("PLACEHOLDER" in c[3] for c in classes))


def clustering_direction():
    """AGA_041 -- the G0 note and the function docstring state the SAME
    caveat under DIFFERENT conditions, and the two run opposite ways.

    Shown exactly, no simulation. Both are Poisson integrals:

      A  clustering alone, in the limit where a burst of k arrives at one
         instant: the process of BURSTS is Poisson at lam/k, so
         P = exp(-lam*w/(60k)) > exp(-lam*w/60) for every k > 1.
         Poisson is a FLOOR.

      B  rate peaking at the hour rest is needed: P over a window started
         at the peak is exp(-integral of the rate), and the integral
         exceeds lam*w whenever the amplitude is positive.
         Poisson is a CEILING.

    The docstring names B ("when events cluster in the same hours as rest
    need"). The G0 note describes A ("interrupters bunch in the same
    hours (weather + traffic + incidents)") and draws B's conclusion."""
    lam = REG.interrupt_rate(REG.EVENT_CLASSES)
    w = REG.g0_window_needed("cycle_min", "high")     # the binding row
    base = REG.p_uninterrupted(lam, w)

    def bursts(k):
        return math.exp(-lam * (w / 60.0) / k)

    def at_peak(amp, period_h=24.0):
        # integral of lam*(1 + amp*cos(2*pi*t/period)) from 0 to w, at the peak
        t = w / 60.0
        integral = lam * (t + amp * period_h / (2 * math.pi)
                          * math.sin(2 * math.pi * t / period_h))
        return math.exp(-integral)

    a = [(k, bursts(k)) for k in (1, 2, 5, 10)]
    b = [(amp, at_peak(amp)) for amp in (0.0, 0.5, 1.0, 1.5)]
    return dict(window_min=w, lam_per_h=lam, poisson=base,
                clustering_only=a, peak_aligned=b,
                clustering_raises=all(v > base for k, v in a if k > 1),
                peak_lowers=all(v < base for amp, v in b if amp > 0),
                note_describes=("A", "interrupters bunch in the same hours"),
                docstring_condition=("B", "in the same hours as rest need"),
                same_caveat_opposite_directions=True)


def probability_domain():
    """AGA_042 -- p_uninterrupted is typed as a probability and has no
    domain guard: a negative window or a negative rate returns a value
    above 1. Reported, not repaired: the file is delivered."""
    lam = REG.interrupt_rate(REG.EVENT_CLASSES)
    probes = [("zero rate", REG.p_uninterrupted(0.0, 125)),
              ("zero window", REG.p_uninterrupted(lam, 0)),
              ("negative window", REG.p_uninterrupted(lam, -60)),
              ("negative rate", REG.p_uninterrupted(-lam, 125))]
    return dict(probes=[(n, v) for n, v in probes],
                out_of_range=[n for n, v in probes if not 0.0 <= v <= 1.0],
                in_range=[n for n, v in probes if 0.0 <= v <= 1.0])


def derived_entry():
    """AGA_043 -- AGA_020's substantive gap: nothing combined two sources
    into a third statement. TRANSFER_NOTE does, and is tagged."""
    note = getattr(REG, "TRANSFER_NOTE", "")
    cites_s5 = "NSTSCE" in note
    cites_term = "fell asleep at the wheel" in note
    s5_holds = any("mentoring" in h.lower() for h in REG.SOURCES["S5"]["holds"])
    return dict(exists=bool(note), tagged_derived="[DERIVED]" in note,
                draws_on_s5=cites_s5, s5_states_the_recommendation=s5_holds,
                draws_on_term_notes=cites_term,
                combines_two=(cites_s5 and cites_term))


def revision(against=None):
    """AGA_036 -- the register was revised after AGA_020..032 were
    published against it. A revision is a copy of its predecessor and
    copies drift, so this reports what moved rather than assuming it.

    `against` resolves to the PREVIOUS VERSION OF THIS FILE, not to a
    position in history: the most recent commit whose blob differs from
    what is on disk. A fixed HEAD~1 would silently compare against the
    same bytes as soon as any other commit lands between them.
    Returns NOT_AVAILABLE where git history is not reachable."""
    import subprocess
    rel = os.path.relpath(os.path.join(HERE, "driver_hours_evidence_register.py"),
                          ROOT)
    with open(os.path.join(HERE, "driver_hours_evidence_register.py")) as fh:
        current = fh.read()

    def _git(args):
        return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True,
                              text=True, timeout=20)

    try:
        if against is None:
            log = _git(["log", "--format=%H", "--", rel])
            if log.returncode:
                return dict(status="NOT_AVAILABLE",
                            reason=log.stderr.strip()[:120])
            prev, against = None, None
            for sha in log.stdout.split():
                blob = _git(["show", "%s:%s" % (sha, rel)])
                if blob.returncode == 0 and blob.stdout != current:
                    prev, against = blob, sha[:7]
                    break
            if prev is None:
                return dict(status="NO_PRIOR_VERSION",
                            reason="no commit of this file differs from disk")
        else:
            prev = _git(["show", "%s:%s" % (against, rel)])
            if prev.returncode:
                return dict(status="NOT_AVAILABLE",
                            reason=prev.stderr.strip()[:120])
    except (OSError, subprocess.SubprocessError) as exc:
        return dict(status="NOT_AVAILABLE", reason=str(exc)[:120])

    import difflib
    old = prev.stdout.splitlines()
    new = current.splitlines()
    ins = dele = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new,
                                                       autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            ins += j2 - j1
        if tag in ("delete", "replace"):
            dele += i2 - i1

    def _objs(lines):
        """Top-level names, and the source of each, for a same/changed split."""
        import ast
        tree = ast.parse("\n".join(lines))
        out = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                    and isinstance(node.targets[0], ast.Name):
                out[node.targets[0].id] = "\n".join(
                    lines[node.lineno - 1:node.end_lineno])
        return out

    a, b = _objs(old), _objs(new)
    same = sorted(k for k in a if k in b and a[k] == b[k])
    changed = sorted(k for k in a if k in b and a[k] != b[k])
    added = sorted(set(b) - set(a))
    return dict(status="OK", against=against, lines_added=ins,
                lines_removed=dele, byte_identical=same, changed=changed,
                added=added, removed=sorted(set(a) - set(b)))


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
        "AGA_033_relay_provenance": relay_provenance(),
        "AGA_034_term_note_scope": term_note_scope(),
        "AGA_035_open_but_uncounted": open_but_uncounted(),
        "AGA_036_revision": revision(),
        "AGA_039_rest_block_provenance": rest_block_provenance(),
        "AGA_044_note3_status_rung": note3_status_rung(),
        "AGA_045_note3_gate_axis": note3_gate_axis(),
        "AGA_046_lcd_forfeit": lcd_forfeit(),
        "AGA_047_note3_confound": note3_confound(),
        "AGA_048_note3_halves": note3_halves(),
        "AGA_049_note3_crossrefs": note3_crossrefs(),
        "AGA_050_note3_fencing": note3_fencing(),
        "AGA_052_delivered_tail": delivered_tail(),
        "AGA_053_exploration_rung_site": exploration_rung_site(),
        "AGA_054_per_operator_term": per_operator_term(),
        "AGA_055_untagged_claim": untagged_claim(),
        "AGA_056_ceiling_split": ceiling_split(),
        "AGA_057_x1_drift": x1_drift(),
        "AGA_058_x2_disciplines": x2_disciplines(),
        "AGA_059_falsifier_wording": falsifier_wording(),
        "AGA_061_exploration_tag_site": exploration_tag_site(),
        "AGA_062_exploration_field_sets": exploration_field_sets(),
        "AGA_063_consent_record": consent_record(),
        "AGA_064_imported_skill_arm": imported_skill_arm(),
        "AGA_040_g0_arithmetic": g0_arithmetic(),
        "AGA_041_clustering_direction": clustering_direction(),
        "AGA_042_probability_domain": probability_domain(),
        "AGA_043_derived_entry": derived_entry(),
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

    rp = f["AGA_033_relay_provenance"]
    p("AGA_033  a source relayed through another source in the register")
    for r in rp:
        p("    %-4s relayed through %s (named: %s); the author-token check "
          "sees it: %s"
          % (r["src"], ", ".join(r["relayed_through"]) or "(not in register)",
             r["named"], r["caught_by_author_overlap"]))
    if not rp:
        p("    none")
    p("")

    tn = f["AGA_034_term_note_scope"]
    p("AGA_034  TERM_DRIFT flag against the sources the note itself names")
    p("    notes: %d   flagged: %s" % (tn["n_notes"], ", ".join(tn["flagged"])))
    p("    named in note  : %s" % ", ".join(tn["named_in_fix"]))
    p("    named, unflagged: %s" % (", ".join(tn["named_but_unflagged"]) or "none"))
    p("    QI's own source list: %s\n"
      % (", ".join(tn["qi_sources"] or []) or "none"))

    ob = f["AGA_035_open_but_uncounted"]
    p("AGA_035  the closing number counts one token")
    p("    counted UNMEASURED : %s  -> headline %s"
      % (", ".join(ob["counted"]), ob["headline"]))
    p("    open, not counted  : %s"
      % (", ".join("%s (%s)" % (a, b) for a, b in ob["open_uncounted"]) or "none"))
    p("    outside the list   : %s  -> %d questions exist, %d are counted"
      % (", ".join("%s (%s)" % (a, b)
                   for a, b in ob["outside_the_counted_list"]) or "none",
         ob["n_all_questions"], ob["n_questions"]))
    p("    answered           : %s  -> not answered %s\n"
      % (", ".join(ob["answered"]), ob["not_answered"]))

    rv = f["AGA_036_revision"]
    p("AGA_036  revision against %s: %s"
      % (rv.get("against", "-"), rv["status"]))
    if rv["status"] == "OK":
        p("    +%d / -%d lines" % (rv["lines_added"], rv["lines_removed"]))
        p("    byte-identical: %s" % (", ".join(rv["byte_identical"]) or "none"))
        p("    changed       : %s" % (", ".join(rv["changed"]) or "none"))
        p("    added         : %s" % (", ".join(rv["added"]) or "none"))
    p("")

    dt = f["AGA_052_delivered_tail"]
    p("AGA_052  the delivered file carries a duplicated tail")
    p("    __main__ blocks: %d   running it prints the register %d times "
      "and\n    the addendum-3 header %d times"
      % (dt["main_blocks"], dt["register_header_printed"],
         dt["addendum3_header_printed"]))
    p("    top-level objects %d, duplicated %d; functions duplicated %d"
      % (dt["top_level_objects"], dt["duplicate_objects"],
         dt["duplicate_functions"]))
    p("    the importable surface is intact, so this audit is unaffected: "
      "%s\n" % dt["importable_surface_intact"])

    er = f["AGA_053_exploration_rung_site"]
    p("AGA_053  the EXPLORATION rung against the entries filed under it")
    p("    rung definition: %s" % er["rung_definition"])
    p("    section header repeats it (UNKNOWN %s, not load-bearing %s)"
      % (er["header_says_unknown"], er["header_says_not_load_bearing"]))
    for e in er["entries"]:
        p("      %-3s relevance %-8s %s"
          % (e["xid"], "UNKNOWN" if e["says_unknown"]
             else ("DIRECT" if e["says_direct"] else "other"),
             e["relevance"][:58]))
    p("    entries whose own field states the opposite of the rung: %s"
      % (", ".join(er["contradicting"]) or "none"))
    p("    the rung on any entry field: %s; applied by the list's name: %s\n"
      % (er["rung_on_any_entry_field"], er["applied_by_the_list_name"]))

    po = f["AGA_054_per_operator_term"]
    p("AGA_054  the per-operator term is declared and reaches no arithmetic")
    p("    %d sleep-quality factors, each stating a status: %s"
      % (po["n_factors"], po["every_factor_states_a_status"]))
    p("    'operator' in the G0 gate entry %s, in G0_NOTES %s, in the "
      "factors %s" % (po["operator_in_gate_entry"], po["operator_in_notes"],
                      po["operator_in_factors"]))
    p("    functions reading the factor list: %s -> reaches arithmetic: %s"
      % (", ".join(po["readers"]), po["reaches_arithmetic"]))
    p("    the window function reads the four constants only: %s\n"
      % po["window_reads_rest_block_only"])

    uc = f["AGA_055_untagged_claim"]
    p("AGA_055  G0 note 1: %d sentences, tags %s"
      % (uc["note1_sentences"],
         " / ".join(",".join(t) or "NONE" for t in uc["note1_tags"])))
    for t in uc["untagged"]:
        p("    untagged: %s" % t)
    p("    it sits between a tagged pair: %s; it is a causal statement: %s\n"
      % (uc["sits_between_tagged"], uc["claim_is_causal"]))

    cs = f["AGA_056_ceiling_split"]
    p("AGA_056  the good-sleeper ceiling: a limit in one document, a datum "
      "in the other")
    p("    %-22s %-12s %-16s %s" % ("", "states limit", "names the sample",
                                    "carries 96%"))
    for name, d in (("ADDENDUM_3.md", cs["note"]), ("the register", cs["register"])):
        p("    %-22s %-12s %-16s %s"
          % (name, d["states_the_limit"], d["mentions_good_sleepers"],
             d["carries_the_figure"]))
    p("    register figure: %s" % cs["register_figure"])
    p("    the word 'ceiling' in the register: %d, and it is the Poisson "
      "sense: %s" % (cs["word_ceiling_in_register"],
                     cs["poisson_ceiling_in_register"]))
    p("    X1's scope field carries the limit: %s"
      % cs["x1_scope_carries_the_limit"])
    p("    computed -- neither document carries both halves: %s\n"
      % cs["neither_has_both"])

    xd = f["AGA_057_x1_drift"]
    p("AGA_057  one record, two delivered documents")
    p("    only in the note    : %s" % ", ".join(xd["only_in_note"]))
    p("    only in the register: %s" % ", ".join(xd["only_in_register"]))
    p("    half_a: %d chars in the note, %d in the register; the register "
      "names\n    dated studies %s, the note %s\n"
      % (xd["half_a_note_chars"], xd["half_a_register_chars"],
         xd["register_names_studies"], xd["note_names_studies"]))

    xs = f["AGA_058_x2_disciplines"]
    p("AGA_058  what holds in X2")
    p("    scope is a consent limit: %s, and the first in the register: %s"
      % (xs["scope_is_a_consent_limit"],
         xs["first_consent_limit_in_the_register"]))
    p("      %s" % xs["scope"])
    p("    the prediction names selection on the outcome: %s"
      % xs["prediction_is_selection_on_the_outcome"])
    p("    half_a declares its own sampling frame: %s\n" % xs["half_a_frame"])

    fw = f["AGA_059_falsifier_wording"]
    p("AGA_059  a fault in this audit's own claim table")
    p("    AGA_020's falsifier: 'a source carrying DERIVED'")
    p("    a source now carries it as an inline tag: %s"
      % (", ".join(fw["a_source_carries_derived_as_a_tag"]) or "none"))
    p("      %s" % (fw["entries"][0] if fw["entries"] else "-"))
    p("    in any status SLOT, the reading the claim intends: %s"
      % fw["derived_in_any_status_slot"])
    p("    the committed claim recorded the first firing (%s) and named the"
      % fw["claim_notes_the_ambiguity"])
    p("    token, not the field (%s):" % fw["falsifier_named_the_token_only"])
    p("      was: %s" % (fw["falsifier_before"] or "history unreachable"))
    p("      now: %s" % fw["falsifier_now"])
    p("    repaired here rather than defended: %s\n" % fw["repaired"])

    ts = f["AGA_061_exploration_tag_site"]
    p("AGA_061  EXPLORATION is a sixth inline-tag site, unscanned")
    p("    scanned for tags: %s" % ", ".join(ts["scanned_objects"]))
    p("    tags here:")
    for k in ts["fields_carrying_a_tag"]:
        p("      %-14s %s" % (k, ", ".join(ts["tags"][k])))
    p("    two rungs in one field: %s"
      % (", ".join(ts["two_rungs_in_one_field"]) or "none"))
    p("    sites reported: %d; this one counted: %s"
      % (ts["n_sites_reported"], ts["site_scanned"]))
    p("    tokens new to the file: %s -> the omission is silent today: %s\n"
      % (ts["tokens_new_to_the_file"] or "none",
         ts["omission_is_silent_today"]))

    fs = f["AGA_062_exploration_field_sets"]
    p("AGA_062  two entries, one list, different field sets, no schema")
    for k in sorted(fs["field_sets"]):
        p("    %s  %d fields" % (k, len(fs["field_sets"][k])))
    p("    present on one entry only: %s" % ", ".join(fs["only_in_one"]))
    p("    the renderer guards with `if k in x`: %s -- so an absent field"
      % fs["renderer_is_guarded"])
    p("    and a field nobody filled print alike")
    p("    X2's new field names motion %s; X1 is about motion %s; X1 has a"
      % (fs["x2_channels_names_motion"], fs["x1_is_about_motion"]))
    p("    channels field %s.  X2 names X1 %s, X1 names X2 %s\n"
      % (fs["x1_has_a_channels_field"], fs["x2_names_x1"], fs["x1_names_x2"]))

    cr = f["AGA_063_consent_record"]
    p("AGA_063  the anchor records what was not asked for")
    p("    channels named %s | categories only %s | specifics withheld %s"
      % (cr["names_the_channels"], cr["records_categories_only"],
         cr["records_specifics_withheld"]))
    p("    the ask not made, recorded: %s" % cr["records_the_ask_not_made"])
    p("    scope declares the limit %s; the anchor records it honoured"
      % cr["scope_declares_the_limit"])
    p("    occurrences in the whole file: %s\n"
      % ", ".join("%s x%d" % kv
                  for kv in cr["occurrences_in_the_file"].items()))

    ia = f["AGA_064_imported_skill_arm"]
    p("AGA_064  QE's third arm against the register's own N_OF_1 rule")
    p("    the arm states a rate %s, a possibility %s, tagged %s"
      % (ia["arm_states_a_rate"], ia["arm_states_a_possibility"],
         ", ".join(ia["arm_tags"]) or "-"))
    p("    -> inside the rule the register wrote for itself: %s"
      % ia["obeys_the_rule"])
    p("    S10 in a source slot: %s" % ", ".join(ia["s10_in_a_source_slot"]))
    p("    S10 in free text    : %s" % ", ".join(ia["s10_in_free_text"]))
    p("    leans on it and records it nowhere: %s\n"
      % ", ".join(ia["leans_without_recording"]))

    n3 = f["AGA_044_note3_status_rung"]
    p("AGA_044  ADDENDUM_3.md declares a rung the register's scale lacks")
    p("    note declares : %s -- %s"
      % (", ".join(n3["note_declares"]), n3["note_says"]))
    p("    in the register's six-rung scale: %s" % n3["in_register_scale"])
    p("    X1 carries %d fields; relevance: %s\n"
      % (len(n3["x1_fields"]), n3["x1_relevance"]))

    ga = f["AGA_045_note3_gate_axis"]
    p("AGA_045  the note makes G0 a per-OPERATOR gate")
    p("    note states one route, two operators, two outcomes: %s"
      % ga["note_claims_per_operator"])
    p("    the register's G0 entry and notes name route %s, season %s, "
      "operator %s" % (ga["register_names_route"], ga["register_names_season"],
                       ga["register_names_operator"]))
    p("    REST_BLOCK holds a constant where the note treats it as a "
      "variable: %s\n"
      % ga["rest_block_is_a_constant"])

    lf = f["AGA_046_lcd_forfeit"]
    p("AGA_046  'a blanket rule ... forfeits the capacity of everyone "
      "above it', as a number")
    p("    fleet rule = the longest window = %d min, at rate %.3f/h"
      % (lf["lcd_minutes"], lf["lam_per_h"]))
    for r in lf["rows"]:
        p("      %-16s %3d min  own %.4f  under the rule %.4f  "
          "gives up %.4f (%.1f%% of own)"
          % (r["window"], r["minutes"], r["own"], r["fleet"], r["forfeit"],
             100 * r["share_of_own"]))
    p("    largest: %.1f%% of that operator's own capacity"
      % (100 * lf["worst_share"]))
    p("    the gap peaks at rate %.4f/h (%.4f) and the placeholder rate "
      "sits at %.0f%% of it" % (lf["peak_lam"], lf["peak_forfeit"],
                                100 * lf["share_of_peak"]))
    p("    sweep: %s"
      % "  ".join("%.2f->%.3f" % (L, g) for L, g in lf["sweep"]))
    p("    it vanishes at both ends -- everyone clears, nobody clears -- "
      "so it\n    is largest where the gate is deciding: %s"
      % lf["vanishes_at_both_ends"])
    p("    no fleet aggregate emitted (the mix of operators is "
      "unmeasured): %s\n" % (not lf["aggregate_emitted"]))

    cf = f["AGA_047_note3_confound"]
    p("AGA_047  the note carries its own confound and the covariate that "
      "separates it")
    p("    SCOPE LIMITS names   stimulus %s   good-sleeper ceiling %s"
      % (cf["scope_section_names_stimulus"], cf["scope_section_names_ceiling"]))
    p("    X1 'scope' carries   stimulus %s   ceiling %s"
      % (cf["x1_scope_carries_stimulus"], cf["x1_scope_carries_ceiling"]))
    p("    prediction: %s" % cf["x1_prediction"])
    p("    the ceiling predicts the same direction, so the probe as "
      "written\n    cannot separate them: probe names baseline %s, "
      "CHEAPEST INSTRUMENT %s,"
      % (cf["probe_names_baseline"], cf["instrument_section_names_baseline"]))
    p("    SCOPE LIMITS %s -- the second covariate is one section above "
      "the probe\n" % cf["scope_section_names_the_repair"])

    hv = f["AGA_048_note3_halves"]
    p("AGA_048  X1's two halves are both outside the register")
    p("    %d sources; a rocking lab %s, an infant-carrying study %s"
      % (hv["n_sources"], hv["rocking_lab_in_register"],
         hv["infant_carrying_in_register"]))
    p("    the note states a sampling limit (%s) and the frame "
      "vocabulary\n    has a member for it: %s   [%s]\n"
      % (hv["sampling_limit_stated"], hv["a_flag_for_a_narrow_lab_sample"],
         ", ".join(hv["declared_frames"])))

    cr = f["AGA_049_note3_crossrefs"]
    p("AGA_049  pointers in the note: %d, resolving to a file: %d"
      % (len(cr["links"]), len(cr["links"]) - len(cr["unresolved"])))
    for u in cr["unresolved"]:
        p("    [[%s]] -- nothing in the tree" % u)
    p("")

    fe = f["AGA_050_note3_fencing"]
    p("AGA_050  the flip rests on the operator's own record and is "
      "fenced %d ways" % fe["fences"])
    p("    labelled PROPOSED %s | status EXPLORATION %s | relevance "
      "UNKNOWN %s" % (fe["labelled_proposed"], fe["status_is_exploration"],
                      fe["relevance_unknown"]))
    p("    declared not load-bearing %s | anchor states its own n %s\n"
      % (fe["declared_not_load_bearing"], fe["anchor_declares_n"]))

    rb = f["AGA_039_rest_block_provenance"]
    p("AGA_039  the two G0 parameter blocks carry provenance differently")
    p("    REST_BLOCK (the window): comments only; in the object: %s"
      % rb["provenance_in_the_object"])
    p("      PLACEHOLDER           : %s" % ", ".join(rb["placeholder"]))
    p("      literature, unverified: %s" % ", ".join(rb["literature_unverified"]))
    p("      neither stated        : %s" % (", ".join(rb["unclassified"]) or "none"))
    p("    EVENT_CLASSES (the rate): a source field on every row: %s\n"
      % rb["event_classes_carry_a_source_field"])

    g0 = f["AGA_040_g0_arithmetic"]
    p("AGA_040  G0 recomputed -- every input declared PLACEHOLDER: %s"
      % g0["all_placeholder"])
    p("    human-required interrupts/h %.3f   mean gap %.1f min"
      % (g0["lam_per_h"], g0["mean_gap_min"]))
    p("    by contribution: %s"
      % ", ".join("%s %.2f" % (n, v) for n, v in g0["by_contribution"]))
    p("    highest raw rate is %s, top contributor is %s -> note 3 holds: %s"
      % (g0["highest_raw_rate"], g0["top_contributor"], g0["note_3_holds"]))
    for w in g0["windows"]:
        p("      %-9s %-4s %3d min -> P %.3f"
          % (w["block"], w["inertia"], w["minutes"], w["p"]))
    p("    binding row %s/%s at P %.3f; removing %s -> rate %.2f, P %.3f\n"
      % (g0["worst"]["block"], g0["worst"]["inertia"], g0["worst"]["p"],
         g0["top_contributor"], g0["lam_without_top"],
         g0["p_worst_without_top"]))

    cd = f["AGA_041_clustering_direction"]
    p("AGA_041  one caveat, two conditions, opposite directions "
      "(exact, no simulation)")
    p("    window %d min, Poisson P %.3f" % (cd["window_min"], cd["poisson"]))
    p("    A  bursting alone, k per burst : %s"
      % ", ".join("k=%d %.3f" % (k, v) for k, v in cd["clustering_only"]))
    p("       -> Poisson is a FLOOR. raises at every k > 1: %s"
      % cd["clustering_raises"])
    p("    B  rate peaking at rest time   : %s"
      % ", ".join("amp=%.1f %.3f" % (a, v) for a, v in cd["peak_aligned"]))
    p("       -> Poisson is a CEILING. lowers at every amplitude: %s"
      % cd["peak_lowers"])
    p("    the docstring names %s (%s); the G0 note describes %s (%s)\n"
      % (cd["docstring_condition"][0], cd["docstring_condition"][1],
         cd["note_describes"][0], cd["note_describes"][1]))

    pd = f["AGA_042_probability_domain"]
    p("AGA_042  p_uninterrupted is typed as a probability, domain unguarded")
    for n, v in pd["probes"]:
        p("      %-16s %.4f%s" % (n, v, "   <- not a probability"
                                  if n in pd["out_of_range"] else ""))
    p("")

    de = f["AGA_043_derived_entry"]
    p("AGA_043  a DERIVED entry now exists: %s" % de["combines_two"])
    p("    TRANSFER_NOTE draws on S5 (%s, which states it: %s) and on "
      "TERM_NOTES (%s), tagged DERIVED: %s\n"
      % (de["draws_on_s5"], de["s5_states_the_recommendation"],
         de["draws_on_term_notes"], de["tagged_derived"]))

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
