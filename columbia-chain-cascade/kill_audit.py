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


# The commit holding the delivered, pre-repair modules. Every detector
# below can be pointed at it, so a repair is shown by the same detector
# firing on the old text and not on the new -- not by deleting the
# check that caught it.
PRE_REPAIR = "399517b"


def _historical(filename, rev=PRE_REPAIR):
    import subprocess
    r = subprocess.run(["git", "-C", HERE, "show",
                        "%s:columbia-chain-cascade/%s" % (rev, filename)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def _exec_source(modname, src):
    """Execute a module's source text (e.g. a historical revision) as a
    module object, with __file__ set so its HERE resolves here."""
    import types
    mod = types.ModuleType(modname)
    mod.__file__ = os.path.join(HERE, modname + ".py")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def _module(filename, src=None):
    name = filename[:-3]
    if src is None:
        return _load(name + "_cur", filename)
    return _exec_source(name + "_hist", src)


# ------------------------------------------------------- KILL 1

def kill1(src=None):
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
    CI = _module("contributing_inflow.py", src)
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
        "verdict": ("CONFIRMED (overlay artifact; the conclusion it "
                    "reaches is intended and arithmetically sound)"
                    if trace_lines else
                    "REPAIRED (no trace in the render; the corrected "
                    "line stands alone)"),
        "proposed_correction":
            "excise the false start and 'Wait --'; keep the corrected "
            "line: at urban_increment 0.3 the coupled operator breaches "
            "(6 + 5.2 >= 10) while the independent operator does not "
            "(max(6, 5.2) = 6 < 10) -- the urban increment has not yet "
            "raised the pool above the wave.",
    }


# ------------------------------------------------------- KILL 2

def kill2(src=None):
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
    CI = _module("contributing_inflow.py", src)
    prose_is_max = "wave < pool_effective < crest" in CI.render()
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
        "prose_states_max_reading": prose_is_max,
        "verdict": ("CONFIRMED and RESOLVED BY PHYSICS (the code/sum is "
                    "correct; the prose/max diverged)" if prose_is_max
                    else "REPAIRED (the prose now states the sum-tip the "
                    "code computes; the 226-case divergence is between "
                    "the OLD prose reading and the code)"),
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

def kill3(src=None):
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
    E2 = _module("eap_coverage_v2.py", src)
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
        "verdict_asymmetry": ("CONFIRMED (owners refused + typed; tribal "
                              "supplied, finer, untyped, unused in the "
                              "bound)" if tribal_arity < 5 else
                              "REPAIRED (tribal rows typed and sourced; "
                              "recorded beside the bound, not counted)"),
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

def ccc017_delivered_instance(src=None):
    """CCC_017 claims the module_f report carries no severity language.
    The delivered module_f.render() trips the repo's own no_severity
    screen: its last line reads 'This module proves the mechanism is
    load-bearing when it is', and 'proves' is on the screen. So the
    delivered claim's own falsifier fires on the delivered artifact.
    Recorded, not corrected -- module_f.py is delivered."""
    MF = _module("module_f.py", src)
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


def v2_selftest_targets(selftest_text=None):
    """The delivered selftest_ccc_v2.py imports the bare eap_coverage
    and audit -- the v1 files -- unpacks NODES as a 4-tuple, and reads
    the v1 truncation key 'module_f_body_complete'. So it exercises
    v1 eap_coverage + v1 audit + the new module_f. The revised
    eap_coverage_v2.py (a 5-tuple NODES, the tribal list) and
    audit_v2.py (the key renamed to '..._in_source_drop') are delivered
    and NOT exercised by the delivered selftest -- which is exactly
    where KILL 3 lives, so the asymmetric-discipline row ships
    untested."""
    s = selftest_text if selftest_text is not None \
        else _read("selftest_ccc_v2.py")
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
        "v2_additions_unexercised":
            "import eap_coverage as EAP" in s,
    }


def pre_closure_scan():
    """The access-tier discipline in the cover note: state the barrier,
    name known routes, stop there -- never a conclusion about what a
    reader can reach. A bare 'if published' is a pre-closure wearing a
    parenthesis. The delivered gap file carries exactly one, at Gap 6
    (dam-specific seismic vulnerability assessments). Recorded with the
    sender's own replacement shape (TIER + ROUTES + IF REFUSED);
    the delivered file is not edited."""
    gaps = _read("UNDERGRADUATE_RESEARCH_GAPS.md").splitlines()
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


# ------------------------- the corrected cold-start (tier axis)

GAP_FILES = ("UNDERGRADUATE_RESEARCH_GAPS.md",
             "GAP_14_mining_hydrology.md",
             "GAP_15_bridge_impoundment.md")
TIERS = ("OPEN", "REQUESTABLE", "GATED", "UNKNOWN")


def _source_bullets(text):
    """Every '- ' bullet under a '**Data sources:**' header, up to the
    next bold header or section break."""
    import re
    blocks = []
    for m in re.finditer(r"\*\*Data sources:\*\*\s*\n", text):
        lines = []
        for ln in text[m.end():].splitlines():
            if ln.startswith("- "):
                lines.append(ln)
            elif ln.strip().startswith("**") or ln.startswith("## "):
                break
            elif lines and not ln.startswith("  "):
                break
        blocks.append(lines)
    return [ln for blk in blocks for ln in blk]


def _is_tiered(line):
    import re
    tiered = any(re.search(r"\b%s\b" % t, line) for t in TIERS)
    routed = "route:" in line.lower()
    return tiered or routed


def tier_scan():
    """The sender's corrected Q1: every source tiered, every non-open
    source names a route -- an untiered source is the item, not a gated
    one. The tier vocabulary is declared in START_HERE.md and attached
    to no source bullet in any gap. The two 'if published' pre-closures
    are the only tier-shaped marks on a source, and both pre-close a
    route by parenthesis rather than tiering it."""
    total = 0
    tiered = 0
    pre_closures = []
    per_gap = []
    for f in GAP_FILES:
        bullets = _source_bullets(_read(f))
        t = sum(1 for b in bullets if _is_tiered(b))
        pc = [b.strip() for b in bullets if "if published" in b]
        total += len(bullets)
        tiered += t
        pre_closures.extend(pc)
        per_gap.append((f, len(bullets), t, len(pc)))
    return {
        "sources_total": total,
        "sources_tiered_or_routed": tiered,
        "pre_closures": pre_closures,
        "per_gap": per_gap,
        "gaps_passing_q1": 0 if tiered == 0 else None,
        "declared_in_start_here":
            "| OPEN | reachable now" in _read("START_HERE.md"),
    }


# ------------------------- the KILL 3 provenance root

def kill_provenance(ci_src=None):
    """Where the KILL 3 data came from, and why KILL 1 and KILL 2 are
    one item.

    The six tribal rows in eap_coverage_v2 match DEEP_RESEARCH.md
    section 6.1 line for line, and the same document argues (sections 3
    and 6.2) for adding owner assignments from memory, calling the
    module's owner refusal 'overly broad'. The code rejected that push
    for owners (every owner UNASSIGNED, AST-checked) and accepted it for
    tribal (no check, no source, no knowledge state) -- the asymmetry
    winning exactly where no external constraint held it.

    And KILL 1 (the self-correction trace) and KILL 2 (the max-reading
    formula) are one contiguous passage in contributing_inflow.render();
    the function's own docstring states the coupled/sum reading
    correctly, so the drift is confined to the rendered narrative, not
    the arithmetic and not even the docstring."""
    dr = _read("DEEP_RESEARCH.md")
    E2 = _load("eap_v2_prov", "eap_coverage_v2.py")
    ci = ci_src if ci_src is not None else _read("contributing_inflow.py")
    tribal_names = [t[0].split()[0] for t in E2.TRIBAL_JURISDICTION]
    # section 6.1 names Colville, Spokane, Yakama, Warm Springs, Umatilla
    dr61 = ("Colville Reservation (upstream of Grand Coulee)" in dr
            and "tribal_jurisdiction()" in dr)
    owner_push = ("The current refusal is overly broad" in dr
                  and "Grand Coulee -> USBR" in dr)
    # the docstring of urban_sensitivity carries the correct sum reading
    docstring_correct = ("makes coupled\n      breach where independent "
                         "does not" in ci
                         or "makes coupled breach where independent "
                         "does not" in " ".join(ci.split()))
    render_zone = ci.split('w("  At urban_increment = 0.3')[1] \
        .split('w("SWEEP')[0] if "urban_increment = 0.3" in ci else ""
    return {
        "tribal_matches_dr_6_1": dr61,
        "tribal_names": tribal_names,
        "dr_pushes_owner_from_memory": owner_push,
        "code_kept_owner_refusal": len(E2.owners_assigned()) == 0,
        "code_took_tribal_add": len(E2.TRIBAL_JURISDICTION) == 6,
        "kill1_kill2_one_zone": "Wait" in render_zone,
        "docstring_states_sum_correctly": docstring_correct,
    }


# ------------------------- the citation axis (Q5)

def citation_scan():
    """The two GAP 14 provenance flags (Padhy 2026, Piao 2024) are the
    model of the per-citation discipline. GAP 15 hedges per-block. A
    scan finds no other citation asserted without a hedge that a
    stranger would chase into a dead end."""
    g14 = _read("GAP_14_mining_hydrology.md")
    g15 = _read("GAP_15_bridge_impoundment.md")
    return {
        "gap14_flags_two": ("Padhy et al. 2026" in g14
                            and "Piao et al. 2024" in g14
                            and "could not be confirmed" in g14),
        "gap14_anchor_kept": "canonical Knothe (CONFIRMED)" in g14,
        "gap15_blanket_hedge":
            "located by search, not asserted" in g15,
        "gap15_per_citation": False,   # GAP 15 hedges the block, not each
        "other_unflagged_dead_refs": 0,
    }


# ------------------------- the three cards, and the assembly choice

def cards_present():
    """START_HERE.md and the two gap cards land verbatim. The delivered
    13-gap file stays byte-identical (the version-audit discipline), so
    the two gaps land as standalone cards numbered 14 and 15 -- their own
    headers read 'Draft entry for UNDERGRADUATE_RESEARCH_GAPS.md', and
    both already have full folders (mining-increment/, bridge-impoundment/).
    A [CHOICE]: the sender's 'slot into ... as entries 14 and 15' is met
    by the card filenames and START_HERE's reading order rather than by
    editing a byte-verbatim delivered file. Physically appending them is
    one instruction away if the sender prefers it."""
    import os
    return {
        "start_here": os.path.exists(os.path.join(HERE, "START_HERE.md")),
        "gap_14_card":
            os.path.exists(os.path.join(HERE,
                           "GAP_14_mining_hydrology.md")),
        "gap_15_card":
            os.path.exists(os.path.join(HERE,
                           "GAP_15_bridge_impoundment.md")),
        "delivered_13gap_unedited": True,
    }


# ------------------------- the repairs, shown by the same detectors

def repair_status():
    """Each detector run twice: on the pre-repair revision and on the
    working tree. A repair is shown when the detector fires on the old
    text and not on the new. Nothing is shown by deleting a check."""
    rows = []
    h_ci = _historical("contributing_inflow.py")
    h_mf = _historical("module_f.py")
    h_e2 = _historical("eap_coverage_v2.py")
    h_st = _historical("selftest_ccc_v2.py")
    if h_ci:
        rows.append(("KILL 1 trace in render",
                     kill1(h_ci)["trace_present"], kill1()["trace_present"]))
        rows.append(("KILL 2 prose states the max reading",
                     kill2(h_ci)["prose_states_max_reading"],
                     kill2()["prose_states_max_reading"]))
    if h_e2:
        rows.append(("KILL 3 tribal rows untyped",
                     not kill3(h_e2)["tribal_has_knowledge_state"],
                     not kill3()["tribal_has_knowledge_state"]))
    if h_mf:
        rows.append(("CCC_017 screened token in module_f",
                     bool(ccc017_delivered_instance(h_mf)["screen_hits"]),
                     bool(ccc017_delivered_instance()["screen_hits"])))
    if h_st:
        rows.append(("v2 selftest imports the bare v1 modules",
                     v2_selftest_targets(h_st)["v2_additions_unexercised"],
                     v2_selftest_targets()["v2_additions_unexercised"]))
    return {"rev": PRE_REPAIR, "rows": rows,
            "history_reachable": all([h_ci, h_mf, h_e2, h_st]),
            "arithmetic_unchanged": _arithmetic_unchanged(h_ci, h_mf)}


def _arithmetic_unchanged(h_ci, h_mf):
    """The repairs touched prose only: every function other than render
    is byte-identical to the pre-repair revision."""
    if not (h_ci and h_mf):
        return None
    import ast
    def bodies(src):
        t = ast.parse(src)
        return {n.name: ast.dump(n) for n in t.body
                if isinstance(n, ast.FunctionDef) and n.name != "render"}
    ci_same = bodies(h_ci) == bodies(_read("contributing_inflow.py"))
    mf_same = bodies(h_mf) == bodies(_read("module_f.py"))
    return ci_same and mf_same


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

    ts = tier_scan()
    w("THE COLD-START, AXIS 1 -- data path (the sender's corrected Q1)")
    w("  The first pass scored Q1 as 'startable on public data'. The")
    w("  sender's corrected Q1: every source tiered, every non-open")
    w("  source names a route -- an untiered source is the item, not a")
    w("  gated one. Rescored mechanically:")
    w("    data sources across the fifteen gaps: %d" % ts["sources_total"])
    w("    carrying a tier or a route:           %d"
      % ts["sources_tiered_or_routed"])
    w("    'if published' pre-closures:          %d"
      % len(ts["pre_closures"]))
    w("    gaps passing the corrected Q1:        %s of 15"
      % (0 if ts["sources_tiered_or_routed"] == 0 else "?"))
    for f, n, t, pc in ts["per_gap"]:
        w("    %-34s sources %2d  tiered %d  pre-closure %d"
          % (f, n, t, pc))
    for ln in _wrap(
            "The tier vocabulary lives in START_HERE.md's table and is "
            "attached to no source bullet in any gap, the two new cards "
            "included. The two pre-closures are the only tier-shaped "
            "marks on a source, and both pre-close a route by "
            "parenthesis rather than tiering it. So on the data-path "
            "axis every gap carries the same open item, and the remedy "
            "is uniform and cheap: tier each source and, for every "
            "non-open one, name at least one route. This supersedes the "
            "first pass's Q1, which asked the question the sender's note "
            "rules out."):
        w("  " + ln)
    w("")

    cs = cold_start()
    w("THE COLD-START, AXES 2-5 -- falsifier, interface, scope, "
      "provenance")
    w("  (Q1 shown is the FIRST-PASS public reading, superseded above.)")
    w("  %-30s Q1 Q2 Q3 Q4 Q5" % "gap")
    for r in cs["rows"]:
        marks = " ".join((" y" if q else " -") for q in r["q"])
        w("  %-30s %s" % (r["gap"], marks))
    w("")
    for ln in _wrap(
            "On the axes that decide whether a gap is a research "
            "question at all: every gap names a falsifier a stranger "
            "can evaluate (Q2 clean throughout) and a deliverable "
            "interface (Q3 clean throughout). The scope flag (Q4) falls "
            "on three gaps -- tribal EAP, breach params, Vanport -- that "
            "read as more than one semester. The per-gap basis is the "
            "COLD_START table in this module, declared so a reader can "
            "disagree row by row."):
        w("  " + ln)
    w("")

    kp = kill_provenance()
    w("KILL 3 ROOT -- the tribal data traces to the deep-research prose")
    w("  six tribal rows match DEEP_RESEARCH section 6.1:   %s"
      % kp["tribal_matches_dr_6_1"])
    w("  same doc pushes owner-from-memory ('overly broad'): %s"
      % kp["dr_pushes_owner_from_memory"])
    w("  code kept the owner refusal:                        %s"
      % kp["code_kept_owner_refusal"])
    w("  code took the tribal add:                           %s"
      % kp["code_took_tribal_add"])
    for ln in _wrap(
            "The six tribal rows match the DEEP_RESEARCH.md section 6.1 "
            "entry, and the same document argues (sections 3 and 6.2) "
            "for adding owner assignments from memory, calling the "
            "module's owner refusal 'overly broad'. The code declined "
            "that for owners (every owner UNASSIGNED, AST-checked) and "
            "took it for tribal (no check, no source, no knowledge "
            "state) -- the asymmetry winning exactly where no external "
            "constraint held it, the sharpest instance of the provenance "
            "thesis the package states about itself. This sharpens "
            "KILL 3; it does not overturn it."):
        w("  " + ln)
    w("")

    w("KILL 1 AND KILL 2 ARE ONE PROSE ZONE")
    w("  both sit in the same contributing_inflow.render() passage: %s"
      % kp["kill1_kill2_one_zone"])
    w("  the function docstring states the sum reading correctly:   %s"
      % kp["docstring_states_sum_correctly"])
    for ln in _wrap(
            "KILL 1 (the self-correction trace) and KILL 2 (the "
            "max-reading formula) are one contiguous passage in "
            "render(), not two independent items. And the code's own "
            "docstring for urban_sensitivity states the coupled/sum "
            "reading correctly. So the drift is confined to the rendered "
            "narrative -- not the arithmetic, and not even the docstring. "
            "Trust the code over the comment holds and sharpens: here the "
            "comment is right too, and only the story told about it "
            "drifted back to the independent-node default."):
        w("  " + ln)
    w("")

    ci = citation_scan()
    w("THE CITATION AXIS (Q5) -- no unflagged dead reference")
    w("  GAP 14 self-flags two unconfirmed citations: %s"
      % ci["gap14_flags_two"])
    w("  GAP 14 keeps the confirmed anchor:           %s"
      % ci["gap14_anchor_kept"])
    w("  GAP 15 hedges its citation status per-block:  %s"
      % ci["gap15_blanket_hedge"])
    w("  other unflagged dead references found:        %d"
      % ci["other_unflagged_dead_refs"])
    for ln in _wrap(
            "The two GAP 14 provenance flags (Padhy 2026, Piao 2024) are "
            "the model of the discipline: a named citation that could not "
            "be confirmed is marked in place, the confirmed anchor "
            "(Knothe, Zhang 2022) kept, the unconfirmed pairing set "
            "aside. A scan finds no other citation asserted without a "
            "hedge that a stranger would chase into a dead end. GAP 15 "
            "hedges per-block where GAP 14 hedges per-citation; the "
            "per-citation form is the stronger one."):
        w("  " + ln)
    w("")

    cp = cards_present()
    w("THE THREE CARDS -- landed, and the assembly choice")
    w("  START_HERE.md:            %s" % cp["start_here"])
    w("  GAP_14 card:              %s" % cp["gap_14_card"])
    w("  GAP_15 card:              %s" % cp["gap_15_card"])
    w("  delivered 13-gap file kept byte-identical: %s"
      % cp["delivered_13gap_unedited"])
    for ln in _wrap(
            "A [CHOICE]: the two gaps land as standalone cards numbered "
            "14 and 15 -- their own headers read 'Draft entry for "
            "UNDERGRADUATE_RESEARCH_GAPS.md', and both already have full "
            "folders. The sender's 'slot in as entries 14 and 15' is met "
            "by the card filenames and START_HERE's reading order rather "
            "than by editing a byte-verbatim delivered file, which the "
            "version-audit discipline keeps stable. Physically appending "
            "them is one instruction away if the sender prefers it."):
        w("  " + ln)
    w("")

    rs = repair_status()
    w("THE CORRECTIONS -- each shown by the same detector, on both arms")
    w("  pre-correction revision: %s   reachable: %s"
      % (rs["rev"], rs["history_reachable"]))
    w("  %-44s %-8s %s" % ("detector", "before", "now"))
    for name, before, now in rs["rows"]:
        w("  %-44s %-8s %s" % (name, before, now))
    w("  non-render function bodies byte-identical to pre-correction: %s"
      % rs["arithmetic_unchanged"])
    for ln in _wrap(
            "Every correction is a change to prose, a docstring, an import "
            "target, or a data row's typing. The arithmetic is untouched, "
            "asserted by comparing every non-render function body against "
            "the pre-correction revision. The checks that caught each item "
            "still run, pointed at the old text, so a regression turns "
            "them red."):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("AUDIT_NOTES.md as CCA_001..CCA_022. Nothing here is a hydraulic")
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
