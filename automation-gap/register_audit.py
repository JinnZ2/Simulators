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


def rest_block_provenance():
    """AGA_039 -- the two parameter blocks the G0 gate runs on carry
    provenance by different means, and only one survives import.
    EVENT_CLASSES (the RATE, the gate's denominator) carries a source
    string as a fourth tuple element, reachable from the object.
    REST_BLOCK (the WINDOW, the gate's numerator) carries it in
    comments, which are not in the object at all: a consumer importing
    the register gets four bare numbers."""
    src = open(os.path.join(HERE, "driver_hours_evidence_register.py")).read()
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
