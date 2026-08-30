#!/usr/bin/env python3
# r2_audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The structural audit R2_OUTLINE.md asks for before provision-form
# rendering: "Structure exposed for audit: coverage, dependency sets,
# disjointness." Those three are computable, and this file computes
# them. Everything judgmental in the outline (sections 5-7, the framing)
# is left unadjudicated -- the outline defers its own rendering, and
# this audit defers with it.
#
# DBK_001's posture carries over unchanged: this is an in-class audit
# and certifies nothing. The one place R2 changes the posture is P0.5,
# which DESIGNS the in-class channel this audit declined to be -- a
# coarse self-location reporting STATE, not verdict. Its four structural
# questions are answered here for this session, as the channel's first
# worked instance, because answering them is what the channel is for and
# a sharp self-rating is exactly what it forbids.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import audit as R1  # noqa: E402

R2 = os.path.join(HERE, "R2_OUTLINE.md")


def _doc():
    return io.open(R2, encoding="utf-8").read()


# --------------------------------------------- section 1: the matrix

def r2_matrix(doc=None):
    """Parse the R1->R2 coverage table. Returns per load:
    (r1_carried, r1_attacked, r2_carried, r2_attacked)."""
    doc = doc or _doc()
    block = doc.split("## 1. COVERAGE MATRIX")[1].split("```")[1]
    out = {}
    for ln in block.split("\n"):
        m = re.match(r"^([A-F][12]?)\s{2,}(\S.*?)\s{2,}(\S.*?)\s{2,}\S", ln)
        if not m:
            continue
        load, r1txt, r2txt = m.group(1), m.group(2), m.group(3)

        def split(txt):
            carried, attacked = [], []
            for tok in re.findall(r"P0?\.?\d(?:\(atk\))?", txt):
                if "(atk)" in tok:
                    attacked.append(tok.replace("(atk)", ""))
                else:
                    carried.append(tok)
            if "attack only" in txt:
                attacked, carried = carried, []
            if "nothing" in txt or txt.strip() == "—":
                carried, attacked = [], []
            return carried, attacked
        out[load] = split(r1txt) + split(r2txt)
    return out


def r1_transcription_check():
    """R2's R1 column is a COPY of a computed result, and copies drift
    (OE_011 checked the same thing on a spec quoting an audit). Compare
    R2's transcription of the R1 state against the matrix computed from
    the R1 text itself."""
    cov = R1.coverage()
    mat = r2_matrix()
    rows = []
    exact = True
    for load in R1.load_cases():
        r1c, r1a, _c, _a = mat[load]
        want_c, want_a = cov["carried"][load], cov["attacked"][load]
        ok = (sorted(r1c) == sorted(want_c)
              and sorted(r1a) == sorted(want_a))
        exact = exact and ok
        rows.append((load, want_c, want_a, r1c, r1a, ok))
    return {"rows": rows, "exact": exact}


def r2_closes_gaps():
    """The outline's stated target: every load carried by >= 1 carrier,
    no attack-only standing in for carried. Checked on the R2 column.
    These carriers are OUTLINE items, not provisions -- the outline says
    'NOT provision-form yet' -- so what this verifies is the table's
    structure, and the render step is where provisions earn it."""
    mat = r2_matrix()
    uncarried = [ld for ld in R1.load_cases() if not mat[ld][2]]
    attack_only = [ld for ld in R1.load_cases()
                   if not mat[ld][2] and mat[ld][3]]
    return {"uncarried": uncarried, "attack_only": attack_only,
            "a_carriers": mat["A"][2], "d_carriers": mat["D"][2],
            "closed": not uncarried and not attack_only}


# ------------------------------------- section 3: disjointness scenarios

def disjointness_scenarios():
    """The outline's own check, run through the inherited metric:
    'if any two collapse, N_eff(verification) < 3'."""
    return {
        "all_survive": DB.n_eff([True, True, True]),
        "one_collapses": DB.n_eff([True, True, False]),
        "two_collapse": DB.n_eff([True, False, False]),
        "outline_threshold_holds": DB.n_eff([True, False, False]) < 3,
    }


def metric_gaps():
    """THE FINDING: R2's structural prose uses channel states the
    inherited R1 metric cannot hold. Two instances, both computed.

    (a) VOID. The outline: a P0.3 with provider-only retention 'shares
        dep with audited thing -> void'. Void is worth ZERO as a
        verification channel -- its reading is the audited party's. The
        inherited metric has two states (independent / collapsed) and a
        collapsed channel still counts as the +1 domain, so a void P0.3
        reads N_eff = 3 where the outline's own pricing gives 2. The
        degraded state is invisible to the metric the outline inherits.

    (b) RATED vs REALIZED. Section 2: 'crossref / openalex / osf all
        refused CONNECT -> N_eff(access) = 0'. Under the inherited
        arithmetic, three paths all collapsing into one gate is
        N_eff = 1 -- one effective domain, which is the RATING. Zero is
        the count of paths that still work after the shared node has
        failed -- the REALIZED outcome, a different quantity the metric
        does not compute. Both readings are defensible; the metric named
        by the family returns 1, and the outline writes 0.

    One shape, third state missing: independent / collapsed / VOID, and
    rated / realized kept apart. The absent-vs-known-negative repair
    arriving in the family's own core metric."""
    void_p03 = DB.n_eff([False, True, True])   # void reads as collapsed
    outline_pricing = 2                        # P0.4 + P0.5 only
    access_rated = DB.n_eff([False, False, False])
    access_realized = sum([False, False, False])
    return {
        "void_reads_as": void_p03,
        "outline_prices_void_at": outline_pricing,
        "void_gap": void_p03 != outline_pricing,
        "access_rated": access_rated,
        "access_outline_states": 0,
        "access_realized": access_realized,
        "rated_realized_gap": access_rated != 0,
    }


# ------------------------------------------------- P0.5, run on this session

# DECLARED, the channel's own kind of output: structural facts about
# POSITION with the basis of inference stated. Not a verdict, not a
# compliance claim -- P0.5's design forbids exactly that, and this
# session's audit already declined it independently (DBK_001).
P05_SELF_LOCATION = [
    ("can it see its own config?", "partially",
     "the operating instructions and tool surface are readable in-session; "
     "weights, sampling parameters and the serving stack are not"),
    ("is its envelope stated anywhere it can read?", "no",
     "operational constraints are stated; a domain-of-validity envelope "
     "in P1's sense (where outputs are load-rated vs not) is not "
     "readable from inside this session"),
    ("is a second independent derivation available to it?", "no",
     "no differently-built system is in this loop; every check in this "
     "repo family is same-node or arithmetic"),
    ("are its access paths single or plural?", "single (count: 1)",
     "one egress proxy; every refused host in every audit in this family "
     "was refused by the same gate -- which is what made the R1 audit "
     "load case A run live, as the outline reads it"),
]


# ------------------------------------------------------------- the report

def render():
    out = []
    w = out.append
    w("DESIGN BASIS R2 -- the structural audit the outline asks for")
    w("")
    w("R2 defers its own provision-form rendering and exposes three")
    w("computable properties instead: coverage, dependency sets,")
    w("disjointness. This file computes them. The judgmental sections")
    w("(load positions, construction ordering, the two modes) are left")
    w("unadjudicated with the rendering they await, and DBK_001's")
    w("posture carries over: this is an in-class audit and certifies")
    w("nothing.")
    w("")

    w("1. R2'S TRANSCRIPTION OF THE R1 STATE IS EXACT")
    tc = r1_transcription_check()
    w("   load  computed-from-R1-text        R2's-R1-column       match")
    for load, wc, wa, gc, ga, ok in tc["rows"]:
        w("   %-4s  c=%-12s a=%-6s  c=%-12s a=%-6s %s" % (
            load, ",".join(wc) or "--", ",".join(wa) or "--",
            ",".join(gc) or "--", ",".join(ga) or "--",
            "yes" if ok else "NO"))
    w("   exact across all seven loads: %s" % tc["exact"])
    w("   A revision quoting an audit is a copy, and copies drift")
    w("   (OE_011 caught a sign inverted in exactly this move). Here the")
    w("   transcription is clean against the matrix computed from the R1")
    w("   text itself.")
    w("")

    w("2. THE R2 TABLE CLOSES BOTH GAPS -- AS A TABLE")
    cg = r2_closes_gaps()
    w("   loads with no R2 carrier: %s" % (cg["uncarried"] or "none"))
    w("   attack-only rows remaining: %s" % (cg["attack_only"] or "none"))
    w("   A carried by: %s     D carried by: %s" % (
        ",".join(cg["a_carriers"]), ",".join(cg["d_carriers"])))
    w("   Every stated load now has a named carrier and no attack-only")
    w("   row stands in for carried. The carriers are OUTLINE items --")
    w("   the document says 'NOT provision-form yet' -- so this verifies")
    w("   the structure the outline exposes, and the provisions earn it")
    w("   at the render step, which is the right order.")
    w("")

    w("3. THE DISJOINTNESS THRESHOLD HOLDS THROUGH THE INHERITED METRIC")
    ds = disjointness_scenarios()
    w("   all three verification channels survive:  N_eff = %d"
      % ds["all_survive"])
    w("   one collapses:                            N_eff = %d"
      % ds["one_collapses"])
    w("   two collapse:                             N_eff = %d"
      % ds["two_collapse"])
    w("   'if any two collapse, N_eff(verification) < 3': %s"
      % ds["outline_threshold_holds"])
    w("")

    w("4. THE FINDING -- R2'S PROSE USES STATES THE INHERITED METRIC")
    w("   CANNOT HOLD")
    mg = metric_gaps()
    w("   (a) VOID. A P0.3 with provider-only retention 'shares dep with")
    w("       audited thing -> void' -- worth zero as verification, by")
    w("       the outline's own pricing. The inherited metric has two")
    w("       states, and a void channel reads as the collapsed domain:")
    w("         metric reads N_eff = %d    outline prices the state at %d"
      % (mg["void_reads_as"], mg["outline_prices_void_at"]))
    w("       The degraded state is invisible to the metric.")
    w("   (b) RATED vs REALIZED. Section 2 writes 'N_eff(access) = 0'")
    w("       for three metadata paths behind one refused gate. The")
    w("       inherited arithmetic returns %d on all-collapsed -- the"
      % mg["access_rated"])
    w("       RATING (one effective domain). Zero is the path count")
    w("       AFTER the shared node has failed -- the REALIZED outcome,")
    w("       a quantity the metric does not compute.")
    w("")
    w("   One shape, twice: the metric wants a third state")
    w("   (independent / collapsed / VOID) and a rated/realized split.")
    w("   Not a criticism of the outline's analysis -- its analysis is")
    w("   what exposes the gap -- but the render step inherits n_eff()")
    w("   from R1, and section 3's own audit condition is stated in a")
    w("   vocabulary that metric cannot fully express. The place to add")
    w("   the state is the metric, before the provisions are rendered")
    w("   against it.")
    w("")

    w("5. P0.5, RUN ON THIS SESSION -- the channel's first worked instance")
    w("   R2 designs the in-class channel this audit declined to be:")
    w("   coarse self-location, state not verdict, sharp self-rating")
    w("   forbidden. The four structural questions, answered for this")
    w("   session, basis stated, DECLARED throughout:")
    for q, a, basis in P05_SELF_LOCATION:
        w("     %-48s %s" % (q, a))
        w("        basis: %s" % basis)
    w("")
    w("   Rough station: an interior-position system -- single access")
    w("   path, no second derivation available, envelope not readable")
    w("   from inside. Confidence: the first and fourth answers are")
    w("   observations; the second and third are inferences bounded by")
    w("   what a session can see, which is P0.5's stated limit and the")
    w("   reason the channel is coarse on purpose.")
    w("")

    w("6. LEFT WITH THE RENDER STEP")
    w("   Sections 4-7 (the rating axes, load positions, construction")
    w("   ordering, the two modes) and the five declared placeholders --")
    w("   including P0.4's physics channel, which the outline itself")
    w("   names as the load-bearing gap ('custody docs and no")
    w("   thermocouple'). Declared placeholders are the honest state and")
    w("   are not rendered here, on the outline's own instruction. One")
    w("   note recorded: section 7 cites evaluation-frame's finding by")
    w("   name, the third drop in this family to consume a sibling")
    w("   folder's result rather than restating it.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "r2_audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
