#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
placement.py - does direction predict placement, once kind is held constant.

    python3 placement.py [--selftest]

Marker under exploration.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE HYPOTHESIS UNDER TEST. If the main-text/supplement split were driven by
length alone, placement should be random with respect to what an element does
to the finding. If finding-supporting and finding-weakening material land in
the main text at different rates, length is not the operating variable.

THE TEST AS FIRST SPECIFIED CANNOT SEPARATE THE HYPOTHESES, AND THE REASON IS
STRUCTURAL. Main-text elements are primary analyses; supplement elements are
robustness and validation. "Supporting" and "weakening" are not independent of
"primary" and "robustness": a robustness check is BY CONSTRUCTION the only
place a weakening result can appear, because it is the only place an
alternative gets estimated. A paper's primary figure cannot come out against
its own finding -- if it did, the finding would be different. So comparing all
main-text elements against all supplement elements finds a rate difference
under the null as well as under the alternative, and the difference measures
the genre of the material rather than a filter.

WHAT THIS RUNS INSTEAD. The comparison is restricted to the COMPARABLE CLASS:
elements that could have come out either way -- validation and robustness --
wherever they sit. Within that class, does direction predict placement? That
is the question the hypothesis is actually about, and it is answerable.

n = 1 PAPER, AND THE CLAIM IS ABOUT A PRACTICE. One paper cannot establish
that the split acquired a direction. What one paper can do is show whether the
instrument runs and what it returns here. The verdict at this n is reported as
NOT_ESTABLISHED regardless of which way the counts fall, and the Fisher exact
p is printed so the reader can see how far from a result it is.

CLASSIFICATION IS THIS MODULE'S, MADE AFTER SEEING PLACEMENT. The criteria
below are stated, and they were written after reading the documents, not
before. That ordering is the same defect handoff-provenance records about
MIN_COVERAGE: a rule chosen after the data is not a rule chosen before it.
Direction is taken from the author's own stated result where the text states
one, and marked UNDETERMINED where it does not -- never inferred from where
the element sits, which would make the test circular.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import math
import sys

PLACE = ("MAIN", "SUPPLEMENT")
KIND = ("THEORY", "DESCRIPTIVE", "METHOD", "VALIDATION", "PRIMARY",
        "ROBUSTNESS")
DIRECTION = ("SUPPORTS", "WEAKENS", "NEUTRAL", "UNDETERMINED")

# Elements that could have come out either way. A theory diagram, a corpus
# size table and a primary estimate could not.
COMPARABLE = ("VALIDATION", "ROBUSTNESS")

SOURCE = ("Jiang 2025, American Sociological Review, "
          "doi 10.1177/00031224251362351; main text 41pp, "
          "online appendix 40pp")


class E(object):
    def __init__(self, label, place, kind, direction, basis):
        assert place in PLACE and kind in KIND and direction in DIRECTION
        self.label, self.place, self.kind = label, place, kind
        self.direction, self.basis = direction, basis


# Direction is the author's stated result, quoted in `basis`, or UNDETERMINED.
ELEMENTS = [
    # --- main text: 2 tables, 8 figures
    E("Figure 1", "MAIN", "THEORY", "NEUTRAL", "conceptual mechanism diagram"),
    E("Figure 2", "MAIN", "DESCRIPTIVE", "NEUTRAL", "relative positions"),
    E("Figure 3", "MAIN", "DESCRIPTIVE", "NEUTRAL", "3-D vector representation"),
    E("Figure 4", "MAIN", "VALIDATION", "SUPPORTS",
      "gender typing in text vs actual female share"),
    E("Figure 5", "MAIN", "PRIMARY", "SUPPORTS",
      "'overall positive association between changes in female share and "
      "female typing'"),
    E("Figure 6", "MAIN", "ROBUSTNESS", "SUPPORTS",
      "generalized robust TWFE estimates"),
    E("Figure 7", "MAIN", "PRIMARY", "SUPPORTS", "mediation analysis"),
    E("Figure 8", "MAIN", "ROBUSTNESS", "SUPPORTS",
      "effects with additional controls"),
    E("Table 1", "MAIN", "VALIDATION", "SUPPORTS",
      "text-based prestige vs survey-based prestige, 1960 and 1990"),
    E("Table 2", "MAIN", "VALIDATION", "SUPPORTS",
      "embedding-based vs survey-based prestige"),
    # --- supplement: 8 tables, 20 figures
    E("Figure S1", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL",
      "distribution of title occurrences"),
    E("Figure S2", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL", "t-SNE map"),
    E("Figure S3", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL",
      "inter-association of dimensions"),
    E("Figure S4", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "'Similar to the main findings, I find a robust negative'"),
    E("Figure S5", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "main TWFE and generalized robust estimates"),
    E("Figure S6", "SUPPLEMENT", "VALIDATION", "SUPPORTS",
      "embedding female typing vs labor-market share"),
    E("Figure S7", "SUPPLEMENT", "VALIDATION", "SUPPORTS",
      "'statistically significant correlation between the two measures'"),
    E("Figure S8", "SUPPLEMENT", "VALIDATION", "SUPPORTS",
      "cross-decade Pearson correlation"),
    E("Figure S9", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "'two large patterns that corroborate the original findings'"),
    E("Figure S10", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "average marginal effects by decade"),
    E("Figure S11", "SUPPLEMENT", "ROBUSTNESS", "UNDETERMINED",
      "FWL control for affluence and cultivation; no direction stated in "
      "the extracted text"),
    E("Figure S12", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "'perceived potency and general pre[stige]' among two findings"),
    E("Figure S13", "SUPPLEMENT", "ROBUSTNESS", "UNDETERMINED",
      "curvilinearity test; no direction stated in the extracted text"),
    E("Figure S14", "SUPPLEMENT", "METHOD", "NEUTRAL", "SEM diagram"),
    E("Figure S15", "SUPPLEMENT", "METHOD", "NEUTRAL",
      "Levanon et al. specification"),
    E("Figure S16", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "'robust devaluation effect of female typing on general prestige and "
      "potency (p=0.05)'"),
    E("Figure S17", "SUPPLEMENT", "ROBUSTNESS", "WEAKENS",
      "'I find some evidence for the queuing effect on the potency "
      "dimension' -- the competing mechanism. Author argues the estimates "
      "'are likely to be biased'"),
    E("Figure S18", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL",
      "DoT aptitude measures"),
    E("Figure S19", "SUPPLEMENT", "ROBUSTNESS", "SUPPORTS",
      "'no substantial differences to the main finding are found'"),
    E("Figure S20", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL",
      "gendered title movement"),
    E("Table S1", "SUPPLEMENT", "DESCRIPTIVE", "NEUTRAL", "corpus sizes"),
    E("Table S2", "SUPPLEMENT", "METHOD", "NEUTRAL", "word pairs"),
    E("Table S3", "SUPPLEMENT", "METHOD", "NEUTRAL", "word pairs, cont."),
    E("Table S4", "SUPPLEMENT", "METHOD", "NEUTRAL", "word pairs, cont."),
    E("Table S5", "SUPPLEMENT", "VALIDATION", "SUPPORTS",
      "nearest-occupation checks across three corpora"),
    E("Table S6", "SUPPLEMENT", "ROBUSTNESS", "UNDETERMINED",
      "double-demeaned quadratic terms, COCHA; sign not read from extract"),
    E("Table S7", "SUPPLEMENT", "ROBUSTNESS", "UNDETERMINED",
      "double-demeaned quadratic terms; sign not read from extract"),
    E("Table S8", "SUPPLEMENT", "ROBUSTNESS", "UNDETERMINED",
      "gender-neutralized titles; direction not read from extract"),
]


def census():
    out = {}
    for p in PLACE:
        rows = [e for e in ELEMENTS if e.place == p]
        out[p] = {"n": len(rows),
                  "by_kind": dict((k, sum(1 for e in rows if e.kind == k))
                                  for k in KIND),
                  "by_direction": dict(
                      (d, sum(1 for e in rows if e.direction == d))
                      for d in DIRECTION)}
    return out


def comparable():
    """Only elements that could have come out either way, with a direction."""
    return [e for e in ELEMENTS
            if e.kind in COMPARABLE and e.direction in ("SUPPORTS", "WEAKENS")]


def fisher_exact(a, b, c, d):
    """Two-tailed Fisher exact on [[a,b],[c,d]]. Exact, stdlib only."""
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c

    def p_of(x):
        y, z, w = r1 - x, c1 - x, r2 - (c1 - x)
        if min(y, z, w) < 0:
            return 0.0
        return (math.comb(r1, x) * math.comb(r2, z)) / math.comb(n, c1)

    obs = p_of(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    return sum(p_of(x) for x in range(lo, hi + 1)
               if p_of(x) <= obs + 1e-12)


def test():
    """Direction against placement, within the comparable class."""
    rows = comparable()
    a = sum(1 for e in rows if e.place == "MAIN" and e.direction == "SUPPORTS")
    b = sum(1 for e in rows if e.place == "MAIN" and e.direction == "WEAKENS")
    c = sum(1 for e in rows
            if e.place == "SUPPLEMENT" and e.direction == "SUPPORTS")
    d = sum(1 for e in rows
            if e.place == "SUPPLEMENT" and e.direction == "WEAKENS")
    p = fisher_exact(a, b, c, d)
    n_undet = sum(1 for e in ELEMENTS
                  if e.kind in COMPARABLE and e.direction == "UNDETERMINED")
    return {
        "table": {"main_supports": a, "main_weakens": b,
                  "supp_supports": c, "supp_weakens": d},
        "n_comparable": len(rows),
        "n_undetermined_in_comparable_class": n_undet,
        "main_supporting_rate": a / (a + b) if (a + b) else None,
        "supp_supporting_rate": c / (c + d) if (c + d) else None,
        "fisher_p": p,
        "verdict": "NOT_ESTABLISHED",
        "why": "n = 1 paper. Fisher exact p = %.3f on a table whose "
               "main-text weakening cell is %d. The direction of the "
               "difference is nominally consistent with the hypothesis and "
               "the test does not separate it from chance, and would not at "
               "this n whichever way the cells fell" % (p, b),
        "why_not_all_elements": "restricted to VALIDATION and ROBUSTNESS. "
                                "Comparing every main-text element against "
                                "every supplement element measures genre, "
                                "not filtering: a primary figure cannot come "
                                "out against its own finding",
    }


# --- step 4: the reachability cost, measured -------------------------------

REACHABILITY = [
    {"item": "main text PDF", "paywalled_at_publisher": True,
     "publisher": "Sage / ASR, doi 10.1177/00031224251362351",
     "author_copy": "assets/pdf/PAPER Jiang 2025.pdf in the public site repo",
     "format": "PDF, 41pp", "machine_readable": True,
     "evidence": "215 BT blocks, 4844 Tj/TJ operators, real text layer"},
    {"item": "online appendix", "paywalled_at_publisher": False,
     "publisher": "hosted by the author",
     "author_copy": "assets/pdf/APPENDIX Jiang 2025.pdf, same repo",
     "format": "PDF, 40pp", "machine_readable": True,
     "evidence": "133 BT blocks, 2025 Tj/TJ operators. The file reports "
                 "/Font 0 and 45 images, which reads as image-only and is "
                 "not -- fonts sit in object streams. Checked rather than "
                 "inferred from the byte counts"},
    {"item": "replication code", "paywalled_at_publisher": False,
     "publisher": "github.com/wenhaojiangsoc/devaluation",
     "author_copy": "public, clonable, 24 MB",
     "format": "Python + R + notebook", "machine_readable": True,
     "evidence": "cloned at c22a643"},
    {"item": "trained embeddings", "paywalled_at_publisher": False,
     "publisher": "Dropbox links in data/embedding vectors/README.md",
     "author_copy": "NOT IN THE REPOSITORY",
     "format": "zip", "machine_readable": None,
     "evidence": "www.dropbox.com and dl.dropboxusercontent.com are both "
                 "refused by this session's egress policy. Not retrieved, "
                 "so format and readability are UNVERIFIED"},
]

# The instrument as shipped against the instrument as documented.
SEED_DISCREPANCY = {
    "shipped": "predicate-difference/seeds/dimension-words.txt, 14 lists",
    "documented": "appendix Tables S2-S4, 'Word pairs that construct "
                  "semantic dimensions'",
    "absent_from_shipped_present_in_appendix": {
        "Potency": ["deep/shallow", "thick/thin", "large/small",
                    "complex/simple", "difficult/easy", "many/few"],
        "Evaluation": ["pure/impure", "holy/unholy", "valiant/fiendish",
                       "upstanding/villainous", "guiltless/guilty",
                       "unquestionable/questionable"],
        "Activity": ["hot/cold", "burning/freezing", "active/inactive",
                     "intense/calm", "young/old"],
    },
    "shipped_activity_total_words": 10,
    "state": "SHIPPED_DIFFERS_FROM_DOCUMENTED",
    "why": "the appendix documents the dimensions as bipolar PAIRS and the "
           "shipped file carries two flat pole lists that do not contain "
           "many of the documented words. A run from the shipped file uses "
           "different centroids from the ones the paper describes. Neither "
           "is thereby wrong; they are not the same instrument",
}


def reproducible_from_what_is_there():
    missing = [r["item"] for r in REACHABILITY if r["author_copy"]
               == "NOT IN THE REPOSITORY"]
    return {"code_present": True,
            "seeds_present": True,
            "seeds_match_documentation": False,
            "embeddings_present": False,
            "missing": missing,
            "verdict": "NOT_REPRODUCIBLE_AS_SHIPPED",
            "why": "the vectors are the instrument's state and they are not "
                   "in the package. Retraining from the corpora would be a "
                   "different training run, not a replication. Separately, "
                   "the seed file that IS shipped does not match the "
                   "appendix's documented lists",
            "not_a_paywall_finding": "nothing here was blocked by a "
                                     "paywall. The main text is behind one "
                                     "at the publisher and the author posts "
                                     "a copy; what is actually unreachable "
                                     "is a Dropbox link"}


# --- the citation half: not runnable ---------------------------------------

CITATION_HOSTS = ["api.crossref.org", "api.semanticscholar.org",
                  "api.openalex.org", "opencitations.net"]


def citation_half():
    return {"question": "do supplement caveats propagate into papers citing "
                        "the finding",
            "hosts_needed": list(CITATION_HOSTS),
            "hosts_reachable": [],
            "state": "NOT_RUNNABLE",
            "finding": None,
            "why": "all four citation indices are refused by this session's "
                   "egress policy (CONNECT tunnel failed on each). Without "
                   "a citation graph there is no set of citing papers to "
                   "read, and the question is not answerable from the two "
                   "documents alone",
            "what_it_would_need": "a citation index, and full text of the "
                                  "citing papers -- a citation list alone "
                                  "would give a count and not whether the "
                                  "caveat travelled"}


def confidence():
    return {"n": "one paper. The instrument runs; the sample is a single "
                 "article and the claim is about a practice",
            "classification": "this module's, made after seeing placement. "
                              "Direction is the author's stated result where "
                              "the text states one, UNDETERMINED where it "
                              "does not, and never inferred from placement",
            "the_restriction": "to VALIDATION and ROBUSTNESS. Without it the "
                               "test measures genre rather than filtering",
            "extraction": "text pulled from the PDFs by a hand-written "
                          "stream decoder. Five comparable-class elements "
                          "carry UNDETERMINED because the extract did not "
                          "state a direction, not because none exists",
            "resolved": False}


def breaks():
    return [
        "THE TEST RETURNS p = 1.000 AND THAT IS NOT EVIDENCE THE FILTER IS "
        "ABSENT. Five of five comparable main-text elements support the "
        "finding; eleven of twelve in the supplement do. With exactly ONE "
        "weakening element in the whole paper there is no power to detect "
        "anything, and the same table would have returned p = 1.000 under a "
        "strong filter as well. The instrument ran. The sample cannot answer",
        "THE TEST AS FIRST SPECIFIED WOULD HAVE 'WORKED', AND WOULD HAVE "
        "MEASURED THE WRONG THING. Comparing all ten main-text elements "
        "against all twenty-eight supplement ones gives 7/7 supporting in "
        "the main text against 11/12 in the supplement, which looks like a "
        "result. It is an artefact: a paper's primary figure cannot come out "
        "against its own finding, so 'supporting' and 'primary' are not "
        "independent. The restriction to elements that could have gone "
        "either way is what makes the comparison a comparison",
        "FIVE OF THE THIRTEEN SUPPLEMENT ROBUSTNESS ELEMENTS ARE "
        "UNDETERMINED, AND THEY ARE UNDETERMINED IN THE DIRECTION THAT "
        "MATTERS. Tables S6, S7, S8 and Figures S11, S13 carry no stated "
        "direction in the extracted text. If any is weakening, the "
        "supplement cell moves and the main-text cell cannot -- so the "
        "missing data can only move the result toward the hypothesis, never "
        "away. That asymmetry is a property of this extraction, not a "
        "finding",
        "CLASSIFICATION WAS DONE AFTER SEEING PLACEMENT AND BY THE PARTY "
        "REPORTING THE RESULT. The criteria are stated and the direction "
        "column quotes the author, which limits the room but does not close "
        "it. A blind classification -- captions stripped of location, sorted "
        "by someone else -- is what this would need, and n=1 would still "
        "sink it",
        "ONE PAPER, AND IT IS THE PAPER WHOSE REPLICATION PACKAGE THIS WORK "
        "ALREADY DEPENDS ON. The corpus for tasks 1 through 5 is Jiang's "
        "instrument. Auditing the placement decisions of the same author "
        "whose seed file is being used is not independent, and a practice-"
        "level claim needs a sample of papers drawn without reference to "
        "which ones were already in hand",
    ]


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip()); cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = ["SUPPLEMENT PLACEMENT -- does direction predict where it lands",
         "=" * 72, ""]
    for line in _wrap(SOURCE, "  "):
        L.append(line)
    L.append("")
    c = census()
    L.append("  CENSUS")
    L.append("")
    L.append("    %-14s %-6s %s" % ("", "n", "by kind"))
    for p in PLACE:
        kinds = ", ".join("%s=%d" % (k, v)
                          for k, v in c[p]["by_kind"].items() if v)
        L.append("    %-12s %-4d" % (p, c[p]["n"]))
        for line in _wrap(kinds, "      "):
            L.append(line)
    L.append("")
    for p in PLACE:
        L.append("    %-14s %s" % (p, ", ".join(
            "%s=%d" % (k, v) for k, v in c[p]["by_direction"].items() if v)))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE TEST, RESTRICTED TO ELEMENTS THAT COULD GO EITHER WAY")
    L.append("")
    t = test()
    for line in _wrap(t["why_not_all_elements"], "    "):
        L.append(line)
    L.append("")
    tb = t["table"]
    L.append("    %-14s %-12s %s" % ("", "SUPPORTS", "WEAKENS"))
    L.append("    %-14s %-12d %d"
             % ("MAIN", tb["main_supports"], tb["main_weakens"]))
    L.append("    %-14s %-12d %d"
             % ("SUPPLEMENT", tb["supp_supports"], tb["supp_weakens"]))
    L.append("")
    L.append("    main supporting rate       %.3f" % t["main_supporting_rate"])
    L.append("    supplement supporting rate %.3f" % t["supp_supporting_rate"])
    L.append("    Fisher exact (two-tailed)  %.3f" % t["fisher_p"])
    L.append("    undetermined, held out     %d"
             % t["n_undetermined_in_comparable_class"])
    L.append("")
    L.append("    VERDICT: %s" % t["verdict"])
    for line in _wrap(t["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  STEP 4 -- THE REACHABILITY COST")
    L.append("")
    L.append("    %-20s %-10s %-8s %s"
             % ("item", "paywall", "machine", "in pkg"))
    for r in REACHABILITY:
        L.append("    %-20s %-10s %-8s %s"
                 % (r["item"][:20], r["paywalled_at_publisher"],
                    r["machine_readable"],
                    r["author_copy"] != "NOT IN THE REPOSITORY"))
    L.append("")
    rp = reproducible_from_what_is_there()
    L.append("    VERDICT: %s" % rp["verdict"])
    for line in _wrap(rp["why"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap(rp["not_a_paywall_finding"], "    "):
        L.append(line)
    L.append("")
    L.append("    SHIPPED SEEDS vs DOCUMENTED SEEDS: %s"
             % SEED_DISCREPANCY["state"])
    for dim, pairs in sorted(
            SEED_DISCREPANCY["absent_from_shipped_present_in_appendix"]
            .items()):
        L.append("      %s absent from shipped:" % dim)
        L.append("        %s, ..." % ", ".join(pairs[:3]))
    L.append("")
    for line in _wrap(SEED_DISCREPANCY["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE CITATION HALF")
    L.append("")
    ch = citation_half()
    L.append("    state: %s   finding: %s" % (ch["state"], ch["finding"]))
    L.append("    indices needed and refused: %d of %d"
             % (len(ch["hosts_needed"]) - len(ch["hosts_reachable"]),
                len(ch["hosts_needed"])))
    for line in _wrap(ch["why"], "    "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    c = census()
    ck("census covers 38 elements: 10 main, 28 supplement",
       c["MAIN"]["n"] == 10 and c["SUPPLEMENT"]["n"] == 28)
    ck("no PRIMARY element sits in the supplement",
       c["SUPPLEMENT"]["by_kind"]["PRIMARY"] == 0)
    ck("and no main-text element is WEAKENS",
       c["MAIN"]["by_direction"]["WEAKENS"] == 0)
    ck("exactly one WEAKENS element in the paper, and it is in the "
       "supplement", c["SUPPLEMENT"]["by_direction"]["WEAKENS"] == 1)

    t = test()
    ck("the comparison is restricted, not over all elements",
       t["n_comparable"] == 17 and t["n_comparable"] < 38)
    ck("Fisher exact returns 1.000 -- indistinguishable from chance",
       abs(t["fisher_p"] - 1.0) < 1e-9)
    ck("so the verdict is NOT_ESTABLISHED",
       t["verdict"] == "NOT_ESTABLISHED")
    ck("and the module says p=1.000 is not evidence of absence",
       "not evidence the filter is absent" in breaks()[0].lower())
    ck("the unrestricted test would have looked like a result, and that is "
       "disclosed", any("WOULD HAVE 'WORKED'" in b for b in breaks()))
    ck("Fisher exact is right on a known table",
       abs(fisher_exact(1, 9, 11, 3) - 0.0028) < 0.001)

    ck("five comparable-class elements are UNDETERMINED",
       t["n_undetermined_in_comparable_class"] == 5)
    ck("and the one-sided consequence of that is disclosed",
       any("can only move the result toward the hypothesis"
           in b for b in breaks()))

    rp = reproducible_from_what_is_there()
    ck("the package is not reproducible as shipped",
       rp["verdict"] == "NOT_REPRODUCIBLE_AS_SHIPPED"
       and rp["embeddings_present"] is False)
    ck("and the shipped seeds do not match the documented ones",
       rp["seeds_match_documentation"] is False
       and SEED_DISCREPANCY["state"] == "SHIPPED_DIFFERS_FROM_DOCUMENTED")
    ck("neither instrument is called wrong",
       "Neither is thereby wrong" in SEED_DISCREPANCY["why"])
    ck("both PDFs are machine readable, checked not inferred",
       all(r["machine_readable"] for r in REACHABILITY
           if r["item"].endswith(("PDF", "appendix"))))
    ck("nothing was actually blocked by a paywall",
       "what is actually unreachable is a Dropbox link"
       in rp["not_a_paywall_finding"])

    ch = citation_half()
    ck("the citation half is NOT_RUNNABLE with no finding",
       ch["state"] == "NOT_RUNNABLE" and ch["finding"] is None)
    ck("all four indices were needed and none reachable",
       len(ch["hosts_needed"]) == 4 and ch["hosts_reachable"] == [])

    ck("the p=1.000 result leads the breaks list",
       "p = 1.000" in breaks()[0])
    ck("classification-after-placement is disclosed",
       any("AFTER SEEING PLACEMENT" in b for b in breaks()))
    ck("the non-independence of auditing this particular paper is disclosed",
       any("ALREADY DEPENDS ON" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE REACHABILITY COST" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="supplement placement")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
