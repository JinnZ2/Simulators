#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
additivity_inheritance -- WO-9, the additivity assumption traced forward
from the Fisher synthesis, built to the order and run on CONSTRUCTED
data. These are OPEN QUESTIONS instrumented, not a critique of statistics;
the tools are not in dispute, their inherited assumptions are the object.

Nothing here reads a primary source or a real paper. R1 codes a
constructed corpus, R2 codes a constructed re-entry set, R3 is NOT_RUN
(prior art unsearched, egress-blocked), and R4 is a citation-graph
simulation whose known answer is the eugenics/Mendel case the order names.
The one arithmetic result -- an additive decomposition losing a real
interaction to the residual -- is exact on a balanced design.

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live
in test_additivity.py.
"""

from __future__ import annotations

import sys

STATUS = ("OBSERVED", "DERIVED", "PROPOSED", "CONSTRUCTED", "CARRIED")

# R1's four codes, the order's
R1_CODES = ("A_STATED", "B_STATED_TESTED", "C_PRESENT_UNSTATED",
            "D_RELAXED")

CHOICES = {
    1: "R1 codes a constructed corpus by the order's four codes; the "
       "prediction is that C (present and unstated) rises with distance "
       "from the source discipline, and the corpus is built to carry that "
       "shape so R1 is a known-answer run on the coder, not evidence",
    2: "R2 codes a re-entry as HAD_TO_FIGHT iff the constructed record "
       "carries rejection or nuisance-framing; the field-distance axis is "
       "declared, not measured from a real literature",
    3: "R4's citation trace is a BFS over CITATION edges only; the "
       "structural trace adds INHERITANCE edges; a precondition reachable "
       "only through an inheritance edge is a citation-trace false negative",
    4: "the additive decomposition is main-effects-only on a balanced 2x2; "
       "the full model adds the interaction; the interaction SS the "
       "additive model assigns to residual is the quantity",
}


class Refused(ValueError):
    """Raised at intake. A refused record never reaches a readout."""


def absent(v):
    return v is None or v == "" or v == "UNDECLARED"


# ===================================================== R1 stated-vs-invisible

def r1_code(paper):
    """Code one paper record. `additivity` in the four codes; a record
    with none is refused -- an uncoded paper is not a data point."""
    c = paper.get("additivity")
    if c not in R1_CODES:
        raise Refused("r1_code: %r is not one of the four codes" % (c,))
    return c


def r1_distribution(papers):
    """Distribution of the four codes by field and by decade, and the
    C-share against field distance from the source discipline."""
    by_field = {}
    by_decade = {}
    for p in papers:
        c = r1_code(p)
        by_field.setdefault(p["field"], {k: 0 for k in R1_CODES})[c] += 1
        by_decade.setdefault(p["decade"], {k: 0 for k in R1_CODES})[c] += 1
    # C-share vs declared field distance
    dist_share = []
    for f, counts in by_field.items():
        n = sum(counts.values())
        dist_share.append((FIELD_DISTANCE[f], counts["C_PRESENT_UNSTATED"] / n))
    dist_share.sort()
    rises = all(dist_share[i][1] <= dist_share[i + 1][1] + 1e-9
                for i in range(len(dist_share) - 1))
    return {"by_field": by_field, "by_decade": by_decade,
            "c_share_by_distance": dist_share,
            "prediction": ("C rises with distance from the source discipline"
                           if rises else
                           "C does not rise monotonically -- the finding")}


# declared distance of each field from the source discipline (population
# genetics); [CHOICE 1], not measured
FIELD_DISTANCE = {"behaviour genetics": 1, "agriculture": 2,
                  "medicine": 3, "education": 4}


# ===================================================== R2 re-entry audit

def r2_reentry(records):                                    # [CHOICE 2]
    """records: {phenomenon, had_to_fight (bool), framing}. Counts how
    many non-additive phenomena had to fight the frame to re-enter."""
    fought = [r for r in records if r["had_to_fight"]]
    return {"n": len(records), "had_to_fight": len(fought),
            "phenomena": [r["phenomenon"] for r in fought],
            "share": None if not records else len(fought) / len(records)}


# ===================================================== R3 prior art

R3 = {"status": "NOT_RUN", "reason": "prior art unsearched; the history-of-"
      "statistics and philosophy-of-biology hosts are egress-blocked",
      "note": "if the what-was-dropped question has been asked at the merge "
              "specifically, WO-9 becomes a pointer, a good outcome"}


# ===================================================== R4 citation trace

def citation_trace(nodes, edges, start, precondition):      # [CHOICE 3]
    """BFS over CITATION edges only, from start. Returns whether the
    precondition node is reachable. edges: list of (src, dst, kind) with
    kind in {'citation', 'inheritance'}."""
    adj = {}
    for s, d, kind in edges:
        if kind == "citation":
            adj.setdefault(s, []).append(d)
    seen, stack = set(), [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, []))
    return precondition in seen


def structural_trace(nodes, edges, start, precondition):
    """BFS over CITATION and INHERITANCE edges. Reaches a precondition
    carried by a shared structural inheritance that citation misses."""
    adj = {}
    for s, d, kind in edges:
        adj.setdefault(s, []).append(d)
    seen, stack = set(), [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, []))
    return precondition in seen


def r4_known_answer():
    """The eugenics/Mendel case as a citation graph. Eugenics (the
    precondition) predates Mendel's rediscovery; Galton had to be TOLD of
    Mendel in 1900. The precondition reaches both camps only through the
    shared FORK they inherited, an inheritance edge, not a citation.
    Citation tracing returns a false negative; the structural trace does
    not. CONSTRUCTED to the order's own description."""
    nodes = ["fork", "eugenics_precondition", "mendelian_camp",
             "biometrician_camp", "fisher_synthesis"]
    edges = [
        # the fork is inherited by both camps (structural, not cited)
        ("mendelian_camp", "fork", "inheritance"),
        ("biometrician_camp", "fork", "inheritance"),
        ("fork", "eugenics_precondition", "inheritance"),
        # the camps cite each other and Fisher cites them
        ("fisher_synthesis", "mendelian_camp", "citation"),
        ("fisher_synthesis", "biometrician_camp", "citation"),
        ("mendelian_camp", "biometrician_camp", "citation"),
    ]
    cite = citation_trace(nodes, edges, "fisher_synthesis", "eugenics_precondition")
    struct = structural_trace(nodes, edges, "fisher_synthesis", "eugenics_precondition")
    return {"citation_reaches_precondition": cite,
            "structural_reaches_precondition": struct,
            "false_negative": (struct and not cite),
            "reads": ("citation tracing misses a precondition carried by "
                      "shared structural inheritance; the structural trace "
                      "reaches it" if (struct and not cite) else
                      "the known-answer case did not reproduce")}


# ============================ the arithmetic: additive decomposition demo

def variance_components(cells):                             # [CHOICE 4]
    """A balanced 2x2 design. cells: {(g, e): value} with one value per
    cell (means). Returns the total, main-effect, interaction and (for the
    additive model) residual sums of squares. On a balanced 2x2 with one
    observation per cell the decomposition is exact.

    grand = mean; SS_G, SS_E from marginal means; SS_int = the remainder.
    An additive (main-effects-only) model has SS_int as its RESIDUAL,
    which is exactly the interaction it cannot represent.
    """
    gs = sorted(set(g for g, _ in cells))
    es = sorted(set(e for _, e in cells))
    if len(gs) != 2 or len(es) != 2 or len(cells) != 4:
        raise Refused("variance_components: a balanced 2x2 with 4 cells")
    vals = list(cells.values())
    grand = sum(vals) / 4.0
    gmean = {g: sum(cells[(g, e)] for e in es) / 2.0 for g in gs}
    emean = {e: sum(cells[(g, e)] for g in gs) / 2.0 for e in es}
    ss_g = 2.0 * sum((gmean[g] - grand) ** 2 for g in gs)
    ss_e = 2.0 * sum((emean[e] - grand) ** 2 for e in es)
    ss_total = sum((v - grand) ** 2 for v in vals)
    ss_int = ss_total - ss_g - ss_e
    return {"grand": grand, "ss_g": ss_g, "ss_e": ss_e,
            "ss_interaction": ss_int, "ss_total": ss_total,
            "additive_residual": ss_int,
            "reads": "the additive model's residual IS the interaction SS; a "
                     "real interaction is assigned to noise"}


def interaction_ss(a, b, c, d):
    """The interaction SS of a balanced 2x2 with cell means
    [[a, b], [c, d]] (rows genotype, cols environment). Registered in
    tools/known_answer.py. On a 2x2 it is (a - b - c + d)^2 / 4."""
    return variance_components({(0, 0): a, (0, 1): b, (1, 0): c, (1, 1): d})["ss_interaction"]


# =============================================== constructed corpora

def r1_corpus():
    """CONSTRUCTED papers built so C rises with field distance -- the
    order's prediction as a declared shape."""
    plan = {"behaviour genetics": ("C_PRESENT_UNSTATED", 2, 8),
            "agriculture": ("C_PRESENT_UNSTATED", 4, 6),
            "medicine": ("C_PRESENT_UNSTATED", 6, 4),
            "education": ("C_PRESENT_UNSTATED", 8, 2)}
    papers = []
    decade = 2000
    for field, (_, c_n, other_n) in plan.items():
        for i in range(c_n):
            papers.append({"field": field, "decade": decade,
                           "additivity": "C_PRESENT_UNSTATED"})
        codes = ["A_STATED", "B_STATED_TESTED", "D_RELAXED"]
        for i in range(other_n):
            papers.append({"field": field, "decade": decade,
                           "additivity": codes[i % 3]})
    return papers


def r2_records():
    """CONSTRUCTED re-entry records for the phenomena the order names."""
    return [
        {"phenomenon": "epigenetics", "had_to_fight": True,
         "framing": "framed as nuisance in early papers"},
        {"phenomenon": "gene-environment interaction", "had_to_fight": True,
         "framing": "re-expressed as a variance component to publish"},
        {"phenomenon": "plasticity", "had_to_fight": True,
         "framing": "rejection language in early reception"},
        {"phenomenon": "norm of reaction", "had_to_fight": False,
         "framing": "entered as its own object"},
    ]


LINEAGE_CLAIM = {
    "claim": "variance partitioning descends from the Fisher merge and "
             "heritability estimates inherit the additivity assumption",
    "status": "CARRIED, verifiable or breakable with sources; if false "
              "WO-9 collapses cheaply and that is the test to run first",
    "verified_here": False}


# ------------------------------------------------------------------ render

def refuse_selftest(name):
    sys.stderr.write("%s carries no selftest; run python3 test_additivity.py\n"
                     % name)
    return 2


def render():
    out = ["WO-9  ADDITIVITY TRACED FORWARD   (corpora CONSTRUCTED, "
           "PROPOSED; no primary source read)", "-" * 72]
    r1 = r1_distribution(r1_corpus())
    out.append("R1  C-share by field distance   [CHOICE 1]")
    for dist, share in r1["c_share_by_distance"]:
        out.append("    distance %d  C-share %.3f" % (dist, share))
    out.append("    -> %s" % r1["prediction"])
    out.append("")
    r2 = r2_reentry(r2_records())
    out.append("R2  re-entry audit   [CHOICE 2]")
    out.append("    %d of %d phenomena had to fight the frame: %s"
               % (r2["had_to_fight"], r2["n"], ", ".join(r2["phenomena"])))
    out.append("")
    out.append("R3  prior art: %s -- %s" % (R3["status"], R3["reason"]))
    out.append("")
    r4 = r4_known_answer()
    out.append("R4  citation-trace false negative (eugenics/Mendel)   [CHOICE 3]")
    out.append("    citation trace reaches the precondition: %s" % r4["citation_reaches_precondition"])
    out.append("    structural trace reaches it:             %s" % r4["structural_reaches_precondition"])
    out.append("    -> false negative: %s" % r4["false_negative"])
    out.append("")
    vc = variance_components({(0, 0): 10.0, (0, 1): 12.0,
                              (1, 0): 12.0, (1, 1): 20.0})
    out.append("additive decomposition, balanced 2x2   [CHOICE 4]")
    out.append("    SS_G %.2f  SS_E %.2f  SS_interaction %.2f  (= additive "
               "residual)" % (vc["ss_g"], vc["ss_e"], vc["ss_interaction"]))
    out.append("    %s" % vc["reads"])
    out.append("")
    out.append("lineage claim (CARRIED, test first): %s" % LINEAGE_CLAIM["claim"])
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("additivity_inheritance.py")
    if "--choices" in argv:
        for k in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
