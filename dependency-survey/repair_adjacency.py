#!/usr/bin/env python3
"""repair_adjacency.py -- the repair-adjacency RESULT
(RESULT_repair_adjacency.md) made checkable at the level the document
fixes.

A third system, DeepSeek, sorted the same 19 records by REPAIR (its R3
adjacency graph, 9 connected components), where Kimi had sorted by repair
CLASS (4 kinds + a straggler) and Perplexity by SUBJECT MATTER (11
groups). The RESULT's headline (§2) is that the three do not conflict --
they NEST, in one order:

    Kimi (4-5)  >  DeepSeek (9)  >  Perplexity (11)

every DeepSeek component contained in one Kimi kind, every Perplexity
group contained in one DeepSeek component, zero cross-cutting. Grain was
never a disagreement; it is a cut height on a tree all three
independently found.

That is a REFINEMENT-CHAIN claim over the transcribed memberships, and it
is checkable here without the corpus. §1 gives the DeepSeek partition at
record level in full; §2 gives the two places Perplexity splits a
component; §3 gives the Kimi coarsening (which components each kind
contains). This module transcribes those (nothing invented; where §3's
reading is contested the edge is flagged, not dropped) and verifies each
link of the chain is a refinement. It is a transcription-consistency
check, NOT a reproduction of any sort -- the 19-cell corpus is external
model output not held in this repo.

    python3 repair_adjacency.py       # the hierarchy readout
Refuses --selftest (checks live in selftest_repadj.py). Stdlib only,
parses under Python 3.9.
"""

import sys

# ---- §1, verbatim: DeepSeek's 9 connected components, record-level ------
DEEPSEEK = {
    "C1": ["T01", "T07", "T13"],               # pass the matching reference
    "C2": ["T02", "T09", "T10", "T12", "T17"], # measure wall clock, drop proxy
    "C3": ["T03", "T18"],                      # normalize by own magnitude
    "C4": ["T04"],                             # apply the 1/2 factor
    "C5": ["T05", "T16"],                      # p = 1 - exp(-rate*dt)
    "C6": ["T06"],                             # compare component-wise
    "C7": ["T08", "T14"],                      # supply scale as a parameter
    "C8": ["T11"],                             # adjust for covariates
    "C9": ["T15", "T19"],                      # compare against a baseline
}

# ---- §2, verbatim: the two components Perplexity splits, into these pieces
PERPLEXITY_SPLITS = {
    "C1": [["T01", "T07"], ["T13"]],   # Perplexity separated the straggler
    "C9": [["T15"], ["T19"]],          # null-baseline vs adaptive-baseline
}

# ---- §3, verbatim: the live Kimi kinds and the components each contains --
KIMI = {
    "K1": ["C1", "C3", "C4", "C5"],   # conversion exists (splits into four)
    "K3": ["C2", "C7"],               # no conversion (speedup core + NLS-3)
    "K2": ["C6"],                     # boundary difference (one, consistent)
    "K5": ["C8", "C9"],               # re-baseline (T11 covariate + T15/T19)
}
# §3 contested edges: still present under Kimi, but flagged, not settled.
CORRECTION_CANDIDATE = {"C7": "K3"}   # NLS-3: both external systems pulled it
CONTESTABLE = {"C8": "K5"}            # T11 covariate: arguably a re-baseline too

# §3: K4 is DEAD as a repair class -- its three Run-1 blind members land in
# three different components, so it is not a component and does not nest.
K4_SCATTER = ["C1", "C6", "C7"]

# §4: the straggler, unassignable to Kimi and unnamed to Perplexity, placed
# by DeepSeek in C1 -- the one cross-cutting event, NOT closed on one system.
STRAGGLER = "T13"
STRAGGLER_COMPONENT = "C1"


def deepseek_records():
    out = []
    for c in DEEPSEEK.values():
        out.extend(c)
    return out


def perplexity_groups():
    """The 11 Perplexity groups: the 7 components it left whole, plus the
    pieces of the 2 it split."""
    groups = []
    for comp, recs in DEEPSEEK.items():
        if comp in PERPLEXITY_SPLITS:
            groups.extend([list(p) for p in PERPLEXITY_SPLITS[comp]])
        else:
            groups.append(list(recs))
    return groups


def refines(fine_blocks, coarse_blocks):
    """(ok, offenders): every fine block is a subset of exactly one coarse
    block. An offender is a fine block that spans two coarse blocks (a
    cross-cut) or lands in none."""
    offenders = []
    for fb in fine_blocks:
        fbs = set(fb)
        covering = [ci for ci, cb in enumerate(coarse_blocks) if fbs <= set(cb)]
        if len(covering) != 1:
            offenders.append((sorted(fbs), len(covering)))
    return (len(offenders) == 0, offenders)


def component_to_kind():
    """Inverse of KIMI: component -> [kinds]. Refinement of DeepSeek by
    Kimi means each component under exactly one kind."""
    inv = {}
    for kind, comps in KIMI.items():
        for c in comps:
            inv.setdefault(c, []).append(kind)
    return inv


def deepseek_refines_kimi():
    """Each DeepSeek component sits inside exactly one live Kimi kind."""
    inv = component_to_kind()
    crosscut = sorted(c for c, ks in inv.items() if len(ks) > 1)
    uncovered = sorted(c for c in DEEPSEEK if c not in inv)
    return (not crosscut and not uncovered, crosscut, uncovered)


def perplexity_refines_deepseek():
    """Each Perplexity group sits inside exactly one DeepSeek component."""
    return refines(perplexity_groups(), list(DEEPSEEK.values()))


def k4_dead():
    """K4's blind members scatter across >= 2 components, so it is not a
    repair operation -- dead as a class."""
    n = len(set(K4_SCATTER))
    return {"scatter": sorted(set(K4_SCATTER)), "distinct_components": n, "dead": n >= 2}


def cut_heights():
    """§6: the count is a cut height on the shared tree, now known. Report
    the levels, never a single number as THE answer."""
    return {
        "class (is a conversion available at all)": "4-5  (Kimi)",
        "operation (which move)": "9  (DeepSeek)",
        "operation + referent (which move, on which referent)": "11  (Perplexity)",
    }


def kind_count():
    """§6, extending the crossmodel refusal: a single number is a cut, and
    a cut with no stated height is the thing the instrument exists to
    catch. Never returns a bare integer."""
    return "A CUT HEIGHT, not a number (4-5 class / 9 operation / 11 operation+referent); state the height"


def standing_answer():
    return {
        "one_or_several": "SEVERAL (four sorts, none returned one)",
        "how_many": kind_count(),
        "which_to_report": "both endpoints, with the nesting stated",
        "fixed": "MEMBERSHIP at every level; nothing cross-cuts",
    }


def report():
    pk, poff = perplexity_refines_deepseek()
    dk, dcc, dunc = deepseek_refines_kimi()
    k4 = k4_dead()
    L = ["repair-adjacency hierarchy (RESULT_repair_adjacency.md §2)",
         "transcription-consistency check of the refinement chain; not a reproduction",
         "(the 19-cell corpus is external model output: Kimi, Perplexity, DeepSeek)",
         "",
         "DeepSeek partition: %d components, %d records" % (len(DEEPSEEK), len(deepseek_records())),
         "chain:  Kimi (4-5)  >  DeepSeek (9)  >  Perplexity (11)",
         "",
         "Perplexity REFINES DeepSeek: %s%s"
         % ("yes, zero cross-cutting" if pk else "NO", "" if pk else " -- offenders: %r" % poff),
         "  11 groups from 9 components: 7 whole + 2 split (C1 -> T01,T07 | T13; C9 -> T15 | T19)",
         "DeepSeek REFINES Kimi: %s%s%s"
         % ("yes, zero cross-cutting" if dk else "NO",
            "" if not dcc else " -- cross-cut: %s" % ", ".join(dcc),
            "" if not dunc else " -- uncovered: %s" % ", ".join(dunc)),
         "  contested (present, flagged, not settled): C7->K3 correction candidate (NLS-3);"
         " C8->K5 contestable (T11 covariate)",
         "",
         "K4: %s across components %s -- DEAD as a repair class"
         % ("scattered" if k4["dead"] else "not scattered", ", ".join(k4["scatter"])),
         "straggler %s: placed by DeepSeek in %s (the one cross-cutting event); "
         "close-test NOT decided on one system" % (STRAGGLER, STRAGGLER_COMPONENT),
         "",
         "CUT HEIGHTS (§6):"]
    for level, h in cut_heights().items():
        L.append("  %-52s %s" % (level, h))
    sa = standing_answer()
    L.append("")
    L.append("STANDING ANSWER (§6):")
    L.append("  one or several? %s" % sa["one_or_several"])
    L.append("  how many?       %s" % sa["how_many"])
    L.append("  which to report? %s" % sa["which_to_report"])
    L.append("  what is fixed?  %s" % sa["fixed"])
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("repair_adjacency has no selftest; run selftest_repadj.py", file=sys.stderr)
        sys.exit(2)
    print(report())
