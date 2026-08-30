#!/usr/bin/env python3
# wo3_return.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The return for WORK_ORDER_F5_3.md. Same-builder pair; every value is
# a same-node computation; nothing is labeled verified or P3-passed.
#
# The split the order's typing rule forces, honored the way this
# folder's audits honor it everywhere: the CLASS assigned to each
# provision is a declared reading, held in a table anyone can disagree
# with line by line -- and the evidence under each reading is
# mechanical. A DERIVED row must carry quotes that are PRESENT in the
# named delivered file; an ASSUMPTION row must have an extracted block
# in which every incident marker is ABSENT. Both directions are
# checked at run time, so a misfiled row turns the check red rather
# than surviving as prose (the DBK_027 rule: credit no incident that
# lives only in a work order).
#
# Class rule, stated because two rows turn on it: a CARRIES load-case
# letter alone does not name an incident (every provision has one, so
# crediting letters would make the audit vacuous). A provision that
# carries the incident's own number and description (5.7 m, the
# written-and-auditable design-basis figure) names the failure case in
# substance; the identification with the seed table's Fukushima row is
# a DECLARED READING and is marked as such in the row.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wo2_return as W2  # noqa: E402

RUN_DATE = "2026-08-30"

R1F = "SOURCE_DROP.md"
V2F = "R2_OUTLINE_V2.md"
SEEDF = os.path.join(ROOT, "effective-redundancy-audit",
                     "SOURCE_DROP.md")

# The order names the artifacts as ai_infrastructure_design_basis.md
# and design_basis_R2_outline.md; neither filename exists in the tree.
# Resolved by content: R1 is SOURCE_DROP.md, the outline is
# R2_OUTLINE_V2.md (the standing revision; v1 sits beside it). The
# UNI_060 filename-mismatch shape, recorded not repaired.
NAME_MISMATCH = ("ai_infrastructure_design_basis.md -> SOURCE_DROP.md",
                 "design_basis_R2_outline.md -> R2_OUTLINE_V2.md")

INCIDENT_MARKERS = ("Katrina", "East Palestine", "Kerr County",
                    "BP Texas City", "Fukushima", "AOA", "5.7",
                    "aviation")


def _read(name):
    p = name if os.path.isabs(name) else os.path.join(HERE, name)
    return io.open(p, encoding="utf-8").read()


def _block(name, start, end):
    doc = _read(name)
    return doc.split(start)[1].split(end)[0]


# ------------------------------------------------ the typing table
# Each row: (id, class, evidence). Evidence for DERIVED: the failure
# case plus (file, quote) pairs checked for presence. For PROVISIONAL:
# the path plus pending-marker quotes. For ASSUMPTION: the block
# bounds checked for marker absence, plus the spec line the provision
# should carry instead.

DERIVED = {
    "P1": {"case": "the written 5.7 m design-basis figure, exceeded "
                   "(seed row: Fukushima 1-4, basement elevation < "
                   "design basis)",
           "quotes": [(R1F, "5.7 m"),
                      ("SEED", "Fukushima 1-4"),
                      ("SEED", "basement elevation < design basis")],
           "link": "declared reading (number+description <-> seed "
                   "row; the doc never writes 'Fukushima' beside "
                   "5.7)"},
    "P3": {"case": "the aviation AOA case, cited in-doc",
           "quotes": [(R1F, "two AOA vanes existed; one system "
                            "reading one")],
           "link": "textual"},
    "P4": {"case": "the AOA-disagree annunciator, same incident",
           "quotes": [(R1F, "AOA-DISAGREE light")],
           "link": "textual"},
    "P6": {"case": "the 5.7 m figure as a budget decision "
                   "(same incident as P1)",
           "quotes": [(R1F, "budget decision wearing a length")],
           "link": "declared reading (as P1)"},
    "P0.1": {"case": "the Fable 5 audit's blocked-access run (in-doc) "
                     "plus Kerr County (seed table)",
             "quotes": [(V2F, "= the worked NEGATIVE"),
                        (V2F, "Kerr County"),
                        ("SEED", "Kerr County 2025")],
             "link": "textual"},
}

PROVISIONAL = {
    "P7": {"path": "the pre-registered replication study: failed "
                   "replications vs independence_ratio, on public "
                   "metadata",
           "pending": [(R1F, "prediction to pre-register, testable "
                             "on public metadata")]},
    "P0.3": {"path": "the operational retention+verification spec "
                     "that adds no provider term, plus the declared "
                     "accounting (Task 2 / DBK_029)",
             "pending": [(V2F, "OPEN spec, QUALIFIED by Task 2"),
                         (V2F, "still needs the")]},
    "P0.4": {"path": "a physics channel whose selection step is also "
                     "closed (the post-Task-6 gap)",
             "pending": [(V2F, "OPEN, one candidate KILLED (Task 6)"),
                         (V2F, "SELECTION step is also closed")]},
}

ASSUMPTION = {
    "P2": {"block": (R1F, "### P2", "### P3"),
           "spec": "PROVISIONAL, pending a traced-claim sample on a "
                   "deployed system: each load-bearing claim resolves "
                   "to {source | marked-pattern | neither}, the "
                   "neither-rate as the derivation datum."},
    "P5": {"block": (R1F, "### P5", "### P6"),
           "spec": "PROVISIONAL, pending the calibration study its "
                   "own FALSIFY names: does point-output accuracy "
                   "match implied confidence, measured at the "
                   "envelope edge."},
    "P8": {"block": (R1F, "### P8", "## 3."),
           "spec": "PROVISIONAL, pending an edge-case-vs-average "
                   "eval: does population-average performance bound "
                   "declared-envelope edge performance anywhere."},
    "P0.2": {"block": (V2F, "P0.2  THE GATE", "## 3."),
             "spec": "PROVISIONAL, pending one logged instance of a "
                     "silent authorization-layer change altering "
                     "results between runs -- the record the "
                     "pinned-probe channel would produce."},
    "P0.5": {"block": (V2F, "P0.5 COARSE", "DISJOINTNESS CHECK"),
             "spec": "PROVISIONAL, pending the four structural "
                     "answers checked against externally observable "
                     "configuration on a deployed instance; one "
                     "uncontrolled worked instance exists and "
                     "nothing yet shows self-location tracks "
                     "position."},
    "AX1": {"block": (V2F, "AX1", "AX2"),
            "spec": "PROVISIONAL, pending band boundaries derived "
                    "from an exposure sample (§8[5]'s own "
                    "condition)."},
    "AX2": {"block": (V2F, "AX2", "AX3"),
            "spec": "PROVISIONAL, pending a substrate-neutral "
                    "criterion set whose null return is "
                    "distinguishable from instrument-mismatch."},
    "AX3": {"block": (V2F, "AX3", "AX4"),
            "spec": "PROVISIONAL, pending an operationalization: "
                    "what observation separates physics-anchored "
                    "from persuasion-anchored output."},
    "AX4": {"block": (V2F, "AX4", "## 5."),
            "spec": "PROVISIONAL, pending one run of the "
                    "substitution test with declared economics pairs "
                    "and a recorded moves/survives verdict per "
                    "component."},
    "S5": {"block": (V2F, "## 5. LOAD POSITION", "## 6."),
           "spec": "PROVISIONAL, pending one documented misload: a "
                   "system rated for one position carrying "
                   "another's load and failing in the classified "
                   "direction."},
    "S6": {"block": (V2F, "## 6. CONSTRUCTION", "## 7."),
           "spec": "PROVISIONAL, pending a documented "
                   "accommodation-first instance failing on first "
                   "real load beside a foundation-first counterpart "
                   "that held."},
    "S7": {"block": (V2F, "## 7. TWO MODES", "## 8."),
           "spec": "PROVISIONAL, pending the annunciator study: do "
                   "operators act differently when the mode is "
                   "declared (the section's own crux)."},
}

ORDER = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8",
         "P0.1", "P0.2", "P0.3", "P0.4", "P0.5",
         "AX1", "AX2", "AX3", "AX4", "S5", "S6", "S7")


def _text_for(tag):
    if tag == "SEED":
        return io.open(SEEDF, encoding="utf-8").read()
    return _read(tag)


def verify_rows():
    """Both directions: DERIVED/PROVISIONAL quotes present, ASSUMPTION
    blocks free of every incident marker."""
    out = {}
    for pid, row in DERIVED.items():
        out[pid] = all(q in _text_for(f) for f, q in row["quotes"])
    for pid, row in PROVISIONAL.items():
        out[pid] = all(q in _text_for(f) for f, q in row["pending"])
    for pid, row in ASSUMPTION.items():
        blk = _block(*row["block"])
        out[pid] = not any(m in blk for m in INCIDENT_MARKERS)
    return out


def t1():
    v = verify_rows()
    table = []
    for pid in ORDER:
        if pid in DERIVED:
            table.append((pid, "DERIVED", DERIVED[pid]["case"],
                          v[pid]))
        elif pid in PROVISIONAL:
            table.append((pid, "PROVISIONAL", PROVISIONAL[pid]["path"],
                          v[pid]))
        else:
            table.append((pid, "ASSUMPTION", ASSUMPTION[pid]["spec"],
                          v[pid]))
    n_assume = sum(1 for _p, c, _e, _v in table if c == "ASSUMPTION")
    # the honest split of the headline
    self_tagged = ["AX1", "AX2", "AX3", "AX4"]   # §8[5] KILLED-VACUOUS
    deferred = ["S5", "S6", "S7"]  # outline defers provision-form
    unmarked = [p for p, c, _e, _v in table if c == "ASSUMPTION"
                and p not in self_tagged and p not in deferred]
    return {"table": table, "n_assumption": n_assume,
            "n_derived": sum(1 for _p, c, _e, _v in table
                             if c == "DERIVED"),
            "n_provisional": sum(1 for _p, c, _e, _v in table
                                 if c == "PROVISIONAL"),
            "self_tagged": self_tagged, "deferred": deferred,
            "unmarked": unmarked,
            "all_rows_verified": all(v.values()),
            "result": "ENUMERATED"}


def falsify_parentheticals():
    """The FALSIFY column's own assumptions: four of eight arrive with
    the outcome asserted in a parenthesis, one cites its incident, and
    three carry no parenthetical."""
    doc = _read(R1F)
    out = {}
    for i in range(1, 9):
        pid = "P%d" % i
        end = "### P%d" % (i + 1) if i < 8 else "## 3."
        blk = doc.split("### %s" % pid)[1].split(end)[0]
        fal = blk.split("FALSIFY")[1]
        asserted = bool(re.search(r"\((they do not|it does( not)?)",
                                  fal))
        backed = "aviation" in fal
        out[pid] = ("incident-backed" if backed
                    else "asserted" if asserted else "none")
    return out


# ---------------------------------------------------------------- T2

def t2():
    seed_doc = io.open(SEEDF, encoding="utf-8").read()
    r1 = _read(R1F)
    b_row = [ln for ln in seed_doc.splitlines()
             if "East Palestine" in ln][0].strip()
    b1_line = [ln for ln in r1.splitlines()
               if ln.startswith("B1 INFORMATION")][0].strip()
    b2_line = [ln for ln in r1.splitlines()
               if ln.startswith("B2 INFORMATION")][0].strip()
    rows = W2.seed_table()
    b2_seed_rows = [r["name"] for r in rows
                    if any(x == "B2" for x in r["letters"])]
    p3_falsify = ("aviation found it does not" in r1
                  and "two AOA vanes existed; one system reading one"
                  in r1)
    sec5 = "aviation's AOA case" in r1
    provenance = ("From cross-domain investigation of redundancy "
                  "failures" in r1)
    pool_has_aviation = "aviation" in W2.r1_domain_pool()
    name_only_in_order = not any(
        "737" in _text_for(f) for f in (R1F, V2F, "SEED"))
    return {"seed_b_row": b_row, "b1_line": b1_line,
            "b2_line_head": b2_line.split("→")[0].strip(),
            "b2_in_seed_rows": b2_seed_rows,
            "p3_falsify_cites_incident": p3_falsify,
            "sec5_cites_incident": sec5,
            "provenance_sentence_present": provenance,
            "pool_has_aviation": pool_has_aviation,
            "incident_name_only_in_order": name_only_in_order,
            "branch": 2,
            "result": "RESOLVED (branch 2)"}


# ---------------------------------------------------------------- T3

LOSS_EVENT = ("L_ret: the provider deletes, fails, or reprices its "
              "stored history -- the record stops being retrievable "
              "from the provider side. Observable: which channels "
              "still return their reading.")


def t3():
    acc = W2.t4()["rows"]
    statements, predictions = [], {}
    for name, val, status in acc:
        if val is None:
            continue
        k = 3 if name.startswith("held") else 2
        predictions[name] = k
        statements.append((name, val,
                           "under L_ret, surviving channels = %d" % k))
    # partition by the survivor prediction vector (one event suffices
    # to separate the classes; within a class the vectors are equal
    # under every candidate event)
    part = {}
    for name, k in predictions.items():
        part.setdefault(k, []).append(name)
    partition = [sorted(v) for _k, v in sorted(part.items(),
                                               reverse=True)]
    inexpressible = [(n, s) for n, v, s in acc if v is None][0]
    return {"loss_event": LOSS_EVENT, "statements": statements,
            "partition": partition,
            "within_class_note":
                "within the not-held class the three texts describe "
                "one physical configuration -- two independent "
                "channels plus one provider-dependent one -- and "
                "predict identical survivor counts under every "
                "candidate event (retention loss, tamper, "
                "audited-system failure), so they are one physical "
                "claim in three texts. What differs is which question "
                "the REPORTED number answers: the collapsed texts' 3 "
                "counts channels flowing absent any loss; the void "
                "text's 2 counts channels surviving L_ret. A design "
                "basis about surviving shared-node failure is asking "
                "the second question -- stating which question a "
                "number answers is not selecting the accounting, "
                "which stays the author's P0.2 declaration.",
            "inexpressible_row": inexpressible[0],
            "inexpressible_typed":
                "OUT-OF-RANGE sensor reading, not a missing value: "
                "the configuration (channel flowing, dependency "
                "shared with the audited thing) is inside the world "
                "and outside the inherited metric's state space. "
                "Handed it and asked the survival question under "
                "L_ret, the metric returns 3 where the count is 2, "
                "with no flag -- data about the instrument's "
                "envelope, which is P1 applied to the metric itself: "
                "it extrapolates silently outside its declared "
                "domain.",
            "result": "RE-TYPED"}


# ---------------------------------------------------------------- render

def _blk(n, title, result, evidence_lines, notes_lines):
    out = ["T%d — %s" % (n, title), "  RESULT   : %s" % result,
           "  EVIDENCE :"]
    for ln in evidence_lines:
        out.append("    %s" % ln)
    out.append("  NOTES    :")
    for ln in notes_lines:
        out.append("    %s" % ln)
    out.append("")
    return out


def _wrap(s, n=64):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("RETURN — FABLE WORK ORDER 3 (provision typing + evidence pulls)")
    w("")
    w("Standing constraint honored: same-builder pair, same-node")
    w("computations, nothing labeled verified or P3-passed. Findings")
    w("dated %s; claims append as DBK_030.. and no prior id is"
      % RUN_DATE)
    w("re-rated. The order's two filenames resolve by content")
    w("(%s; %s). No task required REFUSED-BY-§3: the class"
      % NAME_MISMATCH)
    w("assignments are declared readings checked mechanically in both")
    w("directions, not author decisions.")
    w("")

    r1 = t1()
    ev = ["%-5s %-11s %s" % ("id", "class", "failure case / path / "
                             "spec line")]
    for pid, klass, evd, ok in r1["table"]:
        for i, ln in enumerate(_wrap(evd, 56)):
            ev.append("%-5s %-11s %s" % (pid if i == 0 else "",
                                         klass if i == 0 else "", ln))
        if not ok:
            ev.append("%-5s %-11s ^ EVIDENCE CHECK RED" % ("", ""))
    ev += ["counts: DERIVED %d / PROVISIONAL %d / ASSUMPTION %d of 20"
           % (r1["n_derived"], r1["n_provisional"],
              r1["n_assumption"]),
           "every row's evidence check green: %s"
           % r1["all_rows_verified"],
           "of the %d ASSUMPTION rows:" % r1["n_assumption"],
           "  4 already self-tagged by the doc (§8[5] KILLED-VACUOUS:"
           " AX1-AX4)",
           "  3 outline sections the doc defers from provision-form "
           "(S5-S7)",
           "  5 unmarked assumptions in provision-form text: %s"
           % ", ".join(r1["unmarked"])]
    fp = falsify_parentheticals()
    ev.append("the FALSIFY column's own parentheticals: %s"
              % ", ".join("%s=%s" % (p, fp[p]) for p in
                          ("P1", "P2", "P3", "P4", "P5", "P6", "P7",
                           "P8")))
    out += _blk(1, "PROVISION TYPING AUDIT", r1["result"], ev, _wrap(
        "Headline: 12 of 20 provisions are ASSUMPTION-class under the "
        "order's rule, and the load-bearing subset is the 5 unmarked "
        "ones -- provision-form text naming neither an incident nor a "
        "pending path. A second assumption layer sits inside the "
        "falsification apparatus itself: four of eight FALSIFY "
        "clauses arrive with their outcome asserted in a parenthesis "
        "and no study behind it, one (P3) cites its incident, three "
        "are clean. CARRIES letters were not credited as incident "
        "names (crediting them would make the audit vacuous); the "
        "5.7-m rows are DERIVED with the number-to-Fukushima link "
        "marked as a declared reading, since the doc never writes the "
        "incident's name beside its number."))

    r2 = t2()
    ev = ["seed B row (verbatim):", "  " + r2["seed_b_row"],
          "R1 §1 lines:", "  " + r2["b1_line"],
          "  " + r2["b2_line_head"] + " ...", ""]
    ev += _wrap("The seed row's structure -- one mediated hazard "
                "input, six deciding agencies -- is B1's definition "
                "('one source feeds all deciders'). B2's shape "
                "('sources exist, architecture doesn't compare') is "
                "the in-doc aviation citation: P3's FALSIFY, 'two AOA "
                "vanes existed; one system reading one', present: %s;"
                " §5's 'aviation's AOA case', present: %s."
                % (r2["p3_falsify_cites_incident"],
                   r2["sec5_cites_incident"]))
    ev += ["seed rows naming B2: %s (none -- the table predates the "
           "split)" % (r2["b2_in_seed_rows"] or "[]"),
           "provenance sentence present, pool includes aviation: %s"
           % (r2["provenance_sentence_present"]
              and r2["pool_has_aviation"]),
           "'737' appears in R1, the outline, or the seed table: %s "
           "-- the incident NAME lives only in the order; the doc "
           "cites it by description"
           % (not r2["incident_name_only_in_order"])]
    out += _blk(2, "B FORK RESOLUTION", r2["result"], ev, _wrap(
        "Branch 2 confirmed by reading: B2 rests on no seed-table "
        "incident and is derived from the AOA-disagree logic the doc "
        "itself cites. No over-claim kill: the provenance sentence "
        "assigns the loads to a six-domain pool that includes "
        "aviation, and the aviation incident is cited in the body, "
        "so B2's source is claimed and present -- it is simply in "
        "the doc rather than the seed table, which is one incident "
        "short of the doc's own pool. DBK_027's fork closes on the "
        "reading its branch-2 text anticipated: a derived provision, "
        "legal, and stated. B1 inherits East Palestine alone, so no "
        "second shared node exists in provenance and no dissent_"
        "alarm run is owed."))

    r3 = t3()
    ev = _wrap("Loss event " + r3["loss_event"]) + [""]
    for name, stated, stmt in r3["statements"]:
        ev.append("%-42s stated N_eff %d" % (name, stated))
        ev.append("    -> %s" % stmt)
    ev += ["distinguishability partition: %s" % r3["partition"],
           "one observable event separates the classes; within each,"
           " none does"]
    out += _blk(3, "RETENTION RE-TYPED AS SURVIVAL", r3["result"], ev,
                _wrap(r3["within_class_note"]) + [""] +
                _wrap("Inexpressible row (%s): %s"
                      % (r3["inexpressible_row"],
                         r3["inexpressible_typed"])))

    for ln in _wrap(
            "AFTER RETURN: T1 hands the render step its typing table "
            "with 5 unmarked assumptions and 12 spec lines; T2 closes "
            "DBK_027's fork with no kill and no second shared node; "
            "T3 dissolves the accounting question at the physics "
            "layer into one binary (retention held or not, "
            "adjudicated by L_ret) plus one reporting declaration "
            "that stays the author's, per the order."):
        w(ln)
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "wo3_return.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
