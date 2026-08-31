#!/usr/bin/env python3
# kill_audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The kill list travelled as CLAIMS UNDER TEST, not as findings, with the
# instruction "a kill Fable overturns is a better outcome than a kill it
# confirms." This module adjudicates the three kills mechanically where a
# mechanism exists, records two findings the landing turned up, and runs
# the cold-start test over the fifteen gaps. It edits no delivered file.
#
# Nothing here runs HEC-RAS or touches real terrain. The whole hydraulic
# subject stays untested (CCC_008); this is what a text-only environment
# can say about the package and its own kill list.

import ast
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RUN_DATE = "2026-08-30"


def _read(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


def _load(modname, filename):
    """Load a module by path, so eap_coverage_v2.py can be exercised
    without colliding with the bare eap_coverage the delivered selftest
    imports."""
    spec = importlib.util.spec_from_file_location(
        modname, os.path.join(HERE, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------- KILL 1

def kill1():
    """A self-correction reasoning trace left in contributing_inflow's
    render(). CLAIM: overlay artifact, not authored arithmetic. TEST:
    is it, or does it carry something intended?

    CONFIRMED as an overlay artifact -- and it carries an intended,
    correct conclusion. The trace starts to state the opposite verdict,
    catches itself ('Wait --'), and lands on the right answer: at
    wave 6, pool_effective 5.2, crest 10, the coupled operator breaches
    (11.2 >= 10) and the independent operator does not (max(6, 5.2) = 6
    < 10). So the correction is sound; only the false start and the
    'Wait' are the artifact. The correction is shown, not applied --
    the delivered file stays as delivered."""
    import contributing_inflow as CI
    out = CI.render()
    trace_lines = [ln.strip() for ln in out.splitlines() if "Wait" in ln]
    # the corrected conclusion, checked as arithmetic
    combine = CI.combine
    coupled = combine("sum", 6.0, 5.2) >= 10.0     # True
    indep = combine("max", 6.0, 5.2) >= 10.0       # False
    return {
        "trace_present": bool(trace_lines),
        "trace": trace_lines[0] if trace_lines else "",
        "corrected_conclusion_is_right": coupled and not indep,
        "carries_intended_content": True,
        "verdict": "CONFIRMED (overlay artifact; the conclusion it "
                   "reaches is intended and arithmetically sound)",
        "proposed_correction":
            "excise the false start and 'Wait --'; keep the corrected "
            "line: at urban_increment 0.3 the coupled operator breaches "
            "(6 + 5.2 >= 10) while the independent operator does not "
            "(max(6, 5.2) = 6 < 10) -- the urban increment has not yet "
            "raised the pool above the wave.",
    }


# ------------------------------------------------------- KILL 2

def kill2():
    """The stated decisive condition and the coded one differ.

    PROSE (render): decisive iff wave < pool_effective < crest -- a
    reading in which the pool exceeding the wave is what matters, i.e.
    the MAX (independent-node) operator.
    CODE: urban_decisive = (not coup_base) and coup_urb -- the urban
    increment tipping the SUM (coupled) verdict from no-breach to breach.

    CONFIRMED: the two disagree across the sweep. RESOLVED BY PHYSICS,
    per the sender: the reservoir does not empty to receive the wave;
    the displacement wave rides on a surface already at pool elevation,
    so the combined quantity is wave + pool. MAX would be correct only
    if the wave replaced the pool, and nothing does that. The code
    (sum) is right; the prose diverged. The divergence is the
    interesting part -- the independent-node default reasserting itself
    in the translation layer of a module written to refute it. Correct
    the prose, leave the arithmetic; the correction is recorded, not
    applied to the delivered file."""
    import contributing_inflow as CI
    disagree = 0
    total = 0
    for wave in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        for pn in [2, 3, 4, 5, 6]:
            for crest in [8, 10, 12]:
                for uif in [0.0, 0.1, 0.2, 0.3]:
                    r = CI.urban_sensitivity(float(wave), float(pn),
                                             float(crest), uif)
                    pe = r["pool_effective"]
                    prose = (wave < pe < crest)     # max-flip reading
                    code = r["urban_decisive"]      # sum-tip reading
                    total += 1
                    if prose != code:
                        disagree += 1
    return {
        "prose_vs_code_disagreements": disagree,
        "cases": total,
        "sweep_one_sided": CI.sweep_urban_sensitivity(),
        "verdict": "CONFIRMED and RESOLVED BY PHYSICS (the code/sum is "
                   "correct; the prose/max diverged)",
        "resolution":
            "the wave arrives on top of the standing pool, so the "
            "combined quantity is wave + pool; max would hold only if "
            "the wave replaced the pool. The code is sum-logic and "
            "stands; the prose is the independent-node default "
            "reasserting in the translation layer.",
        "proposed_prose_correction":
            "the urban increment is decisive when it tips the coupled "
            "sum over the crest -- wave + pool_natural < crest but "
            "wave + pool_effective >= crest -- not when the pool "
            "overtakes the wave.",
    }


# ------------------------------------------------------- KILL 3

def kill3():
    """Tribal adjacency supplied from memory at finer granularity than
    the owner data, no knowledge state, no source, and unused in the
    computed bound. CLAIM: asymmetric discipline. CLAIM: the fix is NOT
    to drop tribal -- dropping re-commits INSTITUTIONAL_EXCLUSION.

    Both CONFIRMED, and the asymmetry is sharper than stated:
    - owners are refused from memory (every owner field UNASSIGNED) AND
      each node carries a knowledge_state field (UNKNOWN_ATM);
    - the six tribal rows are supplied from memory as bare 4-tuples
      (nation, reservation, upstream node, downstream node) with no
      knowledge_state field and no source, at a finer granularity than
      the owner data the module refuses;
    - the authority bound is invariant to the tribal list (2 with it,
      without it, or emptied), while the prose says tribal 'adds
      additional sovereign authorities, strengthening the claim' -- an
      assertion the computed number does not carry.

    The second claim also holds: knowledge_state.py rejects
    INSTITUTIONAL_EXCLUSION as an invalid epistemic state, so removing
    the sovereign nations to tidy the asymmetry would re-commit exactly
    that. The correction that overturns neither claim: bring tribal
    under the same discipline the owners already carry -- a
    knowledge_state per row and a named source or a refusal, symmetric
    with the owner UNASSIGNED / UNKNOWN_ATM treatment."""
    E2 = _load("eap_v2_audit", "eap_coverage_v2.py")
    owners = len(E2.owners_assigned())
    tribal = list(E2.TRIBAL_JURISDICTION)
    tribal_arity = len(tribal[0]) if tribal else 0
    node_arity = len(E2.NODES[0])
    b_with = E2.spanning_bound()["authorities_lower_bound"]
    save = E2.TRIBAL_JURISDICTION
    try:
        E2.TRIBAL_JURISDICTION = []
        b_without = E2.spanning_bound()["authorities_lower_bound"]
    finally:
        E2.TRIBAL_JURISDICTION = save
    ks_src = _read("knowledge_state.py")
    return {
        "owners_from_memory": owners,               # 0 -> refused
        "node_carries_knowledge_state": node_arity >= 5,
        "tribal_rows_from_memory": len(tribal),
        "tribal_row_arity": tribal_arity,           # 4 -> no kstate field
        "tribal_has_knowledge_state": tribal_arity >= 5,
        "bound_with_tribal": b_with,
        "bound_without_tribal": b_without,
        "bound_invariant_to_tribal": b_with == b_without,
        "exclusion_is_rejected_state":
            "INSTITUTIONAL_EXCLUSION is not a valid" in ks_src,
        "verdict_asymmetry": "CONFIRMED (owners refused + typed; tribal "
                             "supplied, finer, untyped, unused in the "
                             "bound)",
        "verdict_do_not_drop": "CONFIRMED (dropping re-commits the "
                               "INSTITUTIONAL_EXCLUSION knowledge_state.py "
                               "rejects)",
        "proposed_correction":
            "attach a knowledge_state to each tribal row and a named "
            "source or an explicit refusal, symmetric with the owner "
            "UNASSIGNED / UNKNOWN_ATM treatment -- keep the nations, "
            "type the data.",
    }


# ------------------------- two findings the landing turned up

def ccc017_delivered_instance():
    """CCC_017 claims the module_f report carries no severity language.
    The delivered module_f.render() trips the repo's own no_severity
    screen: its last line reads 'This module proves the mechanism is
    load-bearing when it is', and 'proves' is on the screen. So the
    delivered claim's own falsifier fires on the delivered artifact.
    Recorded, not corrected -- module_f.py is delivered."""
    import module_f as MF
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    hits = no_severity.hits(MF.render())
    return {
        "screen_hits": hits,
        "delivered_ccc017_holds": not hits,
        "token": hits[0][1] if hits else None,
        "line": hits[0][2] if hits else None,
    }


def v2_selftest_targets():
    """The delivered selftest_ccc_v2.py imports the bare eap_coverage
    and audit -- the v1 files -- unpacks NODES as a 4-tuple, and reads
    the v1 truncation key 'module_f_body_complete'. So it exercises
    v1 eap_coverage + v1 audit + the new module_f. The revised
    eap_coverage_v2.py (a 5-tuple NODES, the tribal list) and
    audit_v2.py (the key renamed to '..._in_source_drop') are delivered
    and NOT exercised by the delivered selftest -- which is exactly
    where KILL 3 lives, so the asymmetric-discipline row ships
    untested."""
    s = _read("selftest_ccc_v2.py")
    E2 = _load("eap_v2_targets", "eap_coverage_v2.py")
    A2 = _load("audit_v2_targets", "audit_v2.py")
    import audit as A1
    return {
        "v2_selftest_imports_bare_v1":
            "import eap_coverage as EAP" in s
            and "import audit as A" in s,
        "v2_selftest_unpacks_4tuple":
            "for name, _reach, _j, _o in EAP.NODES" in s,
        "v2_selftest_reads_v1_truncation_key":
            'module_f_body_complete"' in s,
        "v1_audit_has_that_key":
            "module_f_body_complete" in A1.truncation(),
        "audit_v2_renamed_the_key":
            "module_f_body_complete_in_source_drop" in A2.truncation()
            and "module_f_body_complete" not in A2.truncation(),
        "eap_v2_nodes_arity": len(E2.NODES[0]),   # 5 -> 4-unpack raises
        "v2_additions_unexercised": True,
    }


def pre_closure_scan():
    """The access-tier discipline in the cover note: state the barrier,
    name known routes, stop there -- never a conclusion about what a
    reader can reach. A bare 'if published' is a pre-closure wearing a
    parenthesis. The delivered gap file carries exactly one, at Gap 6
    (dam-specific seismic vulnerability assessments). Recorded with the
    sender's own replacement shape (TIER + ROUTES + IF REFUSED);
    the delivered file is not edited."""
    gaps = _read("OPEN_QUESTIONS.md").splitlines()
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(gaps)
            if "if published" in ln]
    return {"pre_closures": hits, "count": len(hits)}


# ------------------------------------------------- the cold-start test

# The sender's five questions, and this audit's coding of each gap
# against them. The coding is declared as data, with a one-line basis,
# so a reader can disagree row by row. Booleans are the answer to the
# question as phrased; a False is a place the gap needs work before a
# stranger could start it cold.
#
#   Q1 public: startable with publicly reachable data only?
#   Q2 falsifier: a stranger can evaluate it without asking the author?
#   Q3 interface: the deliverable drops into a named module interface?
#   Q4 one-semester: one gap is one semester, not secretly five?
#   Q5 provenance: no dead-reference that costs a chaser a week?
COLD_START = [
    # (gap, Q1, Q2, Q3, Q4, Q5, basis)
    ("1 urban inflow", True, True, True, True, True,
     "NLCD + USGS gages are OPEN; falsifier is a <1% threshold; "
     "deliverable is a calibrated urban_increment_fraction into "
     "contributing_inflow.py."),
    ("2 burn roughness", True, True, True, True, True,
     "MTBS/NIFC/NLCD OPEN; falsifier a <5% n-change; deliverable a "
     "burn-severity lookup replacing the module_f B parameters."),
    ("3 tribal EAP", True, True, True, False, True,
     "public tribal + USACE records; falsifier all-six-coordinated; "
     "but mapping six nations x many owners is plausibly more than one "
     "semester -- Q4 flagged."),
    ("4 seam map", False, True, True, True, True,
     "NID owner query is GATED/REQUESTABLE, not open; the rest is "
     "startable; falsifier is 'ownership already public'."),
    ("5 breach params", False, True, True, False, True,
     "NID geometry gated; Froehlich/Xu-Zhang open; 18 dams x two "
     "equations x initial-condition variants is wide -- Q4 flagged."),
    ("6 seismic", False, True, True, True, False,
     "USGS hazard maps open, but the gap line carries a bare 'if "
     "published' pre-closure (Q5) and dam-specific assessments are "
     "gated (Q1)."),
    ("7 atmospheric river", True, True, True, True, True,
     "NOAA AR catalog + gages open; falsifier gate-capacity vs largest "
     "inflow; deliverable a hydro_params table into Module C."),
    ("8 cyber trust", True, True, True, True, True,
     "NERC CIP + human-factors literature open; the deliverable is a "
     "scenario definition, not field data; UNDEFINED is the right "
     "state."),
    ("9 compound", True, True, True, True, True,
     "the deliverable is an interaction matrix from elicitation + "
     "published frameworks; falsifier all-factors-equal-1."),
    ("10 Vanport 1948", False, True, True, False, True,
     "1948 gage records may be gated/archival; a full reproduction is "
     "a large build (Q4); falsifier is 20% on peak stage."),
    ("11 exposure", True, True, True, True, True,
     "Census + NSI + FEMA criteria open; but the overlay consumes a "
     "HEC-RAS hazard field this environment cannot produce -- startable "
     "on published fields."),
    ("12 pipeline", True, True, True, True, True,
     "all named sources are OPEN; falsifier is 'cannot reproduce on a "
     "second machine' -- a clean, checkable target."),
    ("13 operator swap on terrain", False, True, True, True, True,
     "the falsifier and interface are exact (module_f is the "
     "arithmetic), but the run needs HEC-RAS + 3DEP -- not public-only, "
     "Q1 flagged."),
    ("14 mining increment", False, True, True, True, True,
     "landed as mining-increment/; rim-stability data is GATED, the "
     "transfer gate is the interface, the falsifier is three-valued."),
    ("15 bridge impoundment", False, True, True, True, True,
     "landed as bridge-impoundment/; NBI/scour data gated, the "
     "initiator interface is named, the sign caveat is enforced."),
]


def cold_start():
    rows = []
    for gap, q1, q2, q3, q4, q5, basis in COLD_START:
        flags = [q1, q2, q3, q4, q5]
        rows.append({"gap": gap, "q": flags,
                     "clean": all(flags), "basis": basis})
    startable_public = sum(1 for r in rows if r["q"][0])
    all_clean = sum(1 for r in rows if r["clean"])
    return {"rows": rows, "n": len(rows),
            "public_startable": startable_public,
            "clean_on_all_five": all_clean}


# ---------------------------------------------------------- render

def _wrap(s, n=66):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def render():
    out = []
    w = out.append
    w("COLUMBIA CHAIN CASCADE -- the kill list under audit, and the")
    w("cold-start test. Dated %s. No delivered file is edited." % RUN_DATE)
    w("")

    k1 = kill1()
    w("KILL 1 -- self-correction trace left in render()")
    w("  trace present:            %s" % k1["trace_present"])
    w("  corrected line is sound:  %s" % k1["corrected_conclusion_is_right"])
    w("  verdict: %s" % k1["verdict"])
    for ln in _wrap("correction (shown, not applied): "
                    + k1["proposed_correction"]):
        w("    " + ln)
    w("")

    k2 = kill2()
    w("KILL 2 -- stated decisive condition vs coded one")
    w("  prose/code disagreements: %d of %d swept cases"
      % (k2["prose_vs_code_disagreements"], k2["cases"]))
    w("  sweep one-sided (urban never independent-only): %s"
      % k2["sweep_one_sided"])
    w("  verdict: %s" % k2["verdict"])
    for ln in _wrap(k2["resolution"]):
        w("    " + ln)
    for ln in _wrap("prose correction (recorded): "
                    + k2["proposed_prose_correction"]):
        w("    " + ln)
    w("")

    k3 = kill3()
    w("KILL 3 -- tribal supplied from memory, asymmetric discipline")
    w("  owners from memory (refused):      %d" % k3["owners_from_memory"])
    w("  node rows carry a knowledge_state: %s"
      % k3["node_carries_knowledge_state"])
    w("  tribal rows from memory:           %d"
      % k3["tribal_rows_from_memory"])
    w("  tribal row carries a knowledge_state: %s (arity %d)"
      % (k3["tribal_has_knowledge_state"], k3["tribal_row_arity"]))
    w("  authority bound with / without tribal: %d / %d  invariant: %s"
      % (k3["bound_with_tribal"], k3["bound_without_tribal"],
         k3["bound_invariant_to_tribal"]))
    w("  verdict (asymmetry):  %s" % k3["verdict_asymmetry"])
    w("  verdict (do not drop): %s" % k3["verdict_do_not_drop"])
    for ln in _wrap("correction: " + k3["proposed_correction"]):
        w("    " + ln)
    w("")

    w("THE KILL LIST IS ITSELF UNDER AUDIT")
    for ln in _wrap(
            "All three hold; none is overturned. KILL 2 arrived with an "
            "OPEN ('which is correct is not Claude's to call') that the "
            "sender then closed by physics; this audit upholds that "
            "closure rather than re-opening it. Each verdict is bounded "
            "to what a text-only environment can check: the arithmetic "
            "and the module structure, not any hydraulic magnitude."):
        w("  " + ln)
    w("")

    c17 = ccc017_delivered_instance()
    w("FINDING -- CCC_017 refuted on its delivered instance")
    w("  module_f report clean on the screen: %s"
      % c17["delivered_ccc017_holds"])
    if c17["token"]:
        w("  the token that fires: '%s'" % c17["token"])
        for ln in _wrap("on the line: " + (c17["line"] or "")):
            w("    " + ln)
    for ln in _wrap(
            "The delivered CCC_017 asserts the module_f report carries "
            "no flagged language; the repo's own screen disagrees. The "
            "delivered claim's falsifier fires on the delivered "
            "artifact. Recorded, not corrected -- module_f.py is "
            "delivered."):
        w("  " + ln)
    w("")

    vt = v2_selftest_targets()
    w("FINDING -- the delivered v2 selftest exercises the v1 modules")
    w("  imports bare v1 eap_coverage/audit: %s"
      % vt["v2_selftest_imports_bare_v1"])
    w("  unpacks NODES as a 4-tuple:          %s"
      % vt["v2_selftest_unpacks_4tuple"])
    w("  reads the v1 truncation key:         %s"
      % vt["v2_selftest_reads_v1_truncation_key"])
    w("  eap_coverage_v2 NODES arity:         %d (a 4-unpack raises)"
      % vt["eap_v2_nodes_arity"])
    w("  audit_v2 renamed the key:            %s"
      % vt["audit_v2_renamed_the_key"])
    for ln in _wrap(
            "So the delivered selftest tests v1 eap_coverage + v1 audit "
            "+ the new module_f. The revised eap_coverage_v2.py (the "
            "tribal list, a 5-tuple NODES) and audit_v2.py (the renamed "
            "key) are delivered and unexercised -- and the tribal list "
            "is exactly where KILL 3 lives, so the asymmetric row ships "
            "untested."):
        w("  " + ln)
    w("")

    pc = pre_closure_scan()
    w("FINDING -- one pre-closure in the gap file (access-tier "
      "discipline)")
    w("  bare 'if published' pre-closures: %d" % pc["count"])
    for line_no, text in pc["pre_closures"]:
        for ln in _wrap("line %d: %s" % (line_no, text)):
            w("    " + ln)
    for ln in _wrap(
            "The cover note's discipline: state the barrier, name known "
            "routes, stop there. A bare 'if published' pre-closes a "
            "route by parenthesis. The sender's replacement shape (TIER "
            "GATED + ROUTES + IF REFUSED, where a documented refusal is "
            "itself a finding on the Gap 3 coverage question) applies "
            "here as it does to the Gap 14 data line the cover note "
            "flagged. Recorded; the delivered file is not edited."):
        w("  " + ln)
    w("")

    cs = cold_start()
    w("THE COLD-START TEST -- five questions over fifteen gaps")
    w("  Q1 public  Q2 falsifier  Q3 interface  Q4 one-semester  "
      "Q5 provenance")
    w("  %-30s Q1 Q2 Q3 Q4 Q5" % "gap")
    for r in cs["rows"]:
        marks = " ".join(" y" if q else " .' "[:2] for q in r["q"])
        # render False as a dot so the flagged questions are legible
        marks = " ".join((" y" if q else " -") for q in r["q"])
        w("  %-30s %s" % (r["gap"], marks))
    w("")
    w("  startable on public data alone: %d of %d"
      % (cs["public_startable"], cs["n"]))
    w("  clean on all five questions:    %d of %d"
      % (cs["clean_on_all_five"], cs["n"]))
    for ln in _wrap(
            "Every gap names a falsifier a stranger can evaluate (Q2 "
            "clean throughout) and a deliverable interface (Q3 clean "
            "throughout) -- the two the agenda most has to get right. "
            "The flags cluster on Q1 (the hydraulic gaps that want "
            "HEC-RAS or gated dam data) and on Q4 (three gaps -- tribal "
            "EAP, breach params, Vanport -- that read as more than one "
            "semester). Q5 flags once, the Gap 6 pre-closure above. "
            "The per-gap basis is the COLD_START table in this module, "
            "declared so a reader can disagree row by row."):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("AUDIT_NOTES.md as CCA_001..CCA_009. Nothing here is a hydraulic")
    w("result: the spec's actual subject stays untested (CCC_008).")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "kill_audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_kill.py.\n"
            "    python3 columbia-chain-cascade/selftest_kill.py\n")
        sys.exit(2)
    print(render())
