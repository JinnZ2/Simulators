# SPDX-License-Identifier: CC0-1.0
"""
T1 -- DETECTION, NOT KEYWORD.

Work order: extract the subject of the main causal claim per abstract and
classify it as individuated-persistent or not. Valence off. Field-agnostic.

WHAT THIS DOES AND DOES NOT DO, stated before the code so it is not a
footnote. Three steps, and they are not equally sound:

  step 1  CLAIM SELECTION      predicate-structural. Ordered rule from
                               BOUNDARY.md D0. Not lexical: it selects a
                               sentence by the verb class it carries, not
                               by topic words.
  step 2  SUBJECT EXTRACTION   syntactic, heuristic, stdlib only. Takes the
                               span before the first finite verb and its
                               head noun. No parser. Fails on inversion,
                               heavy pre-modification, and any subject that
                               is a clause.
  step 3  CLASSIFICATION       PARTLY LEXICAL, and this is the finding.
                               Claim-level nouns (BOUNDARY.md D2 `market`,
                               D3 `system` / `network`) are decided by the
                               predicate. Everything else falls back to the
                               D3 unit table, which is a word list.

The work order's own premise is that lexical search fails here because the
identity assumption is PREMISE, not vocabulary. Step 3 reproduces that
failure for every noun not on the claim-level list. The detector therefore
reports HOW each classification was reached -- `PREDICATE`, `TABLE`, or
`UNDECIDABLE` -- and the TABLE share is the size of the unfixed problem, not
a footnote about it.

Decisions are imported from BOUNDARY.md by transcription into the tables
below. The transcription is checked by `--selftest`, which fails if a unit
in the table is missing from BOUNDARY.md's D3 table or carries a different
call.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUNDARY = os.path.join(HERE, "BOUNDARY.md")

IDENTITY = "IDENTITY_BEARING"
NONIDENTITY = "NON_IDENTITY"
UNDECIDABLE = "UNDECIDABLE"

BY_PREDICATE = "PREDICATE"
BY_TABLE = "TABLE"
BY_NEITHER = "UNDECIDABLE"

# --------------------------------------------------------------------------
# D3, transcribed. `--selftest` checks this against BOUNDARY.md.
# --------------------------------------------------------------------------

UNIT_TABLE = {
    "firm": IDENTITY, "firms": IDENTITY,
    "organization": IDENTITY, "organizations": IDENTITY,
    "institution": IDENTITY, "institutions": IDENTITY,
    "species": IDENTITY, "lineage": IDENTITY, "lineages": IDENTITY,
    "gene": IDENTITY, "genes": IDENTITY, "replicator": IDENTITY,
    "population": IDENTITY, "populations": IDENTITY,
    "cohort": IDENTITY, "cohorts": IDENTITY, "generation": IDENTITY,
    "individual": IDENTITY, "individuals": IDENTITY,
    "agent": IDENTITY, "agents": IDENTITY,
    "household": IDENTITY, "households": IDENTITY,
    "state": IDENTITY, "states": IDENTITY, "nation": IDENTITY,
    "jurisdiction": IDENTITY, "jurisdictions": IDENTITY,
    "norm": IDENTITY, "norms": IDENTITY,
    "niche": NONIDENTITY, "niches": NONIDENTITY,
    "role": NONIDENTITY, "roles": NONIDENTITY,
    "office": NONIDENTITY, "position": NONIDENTITY,
    "process": NONIDENTITY, "processes": NONIDENTITY,
    "practice": NONIDENTITY, "practices": NONIDENTITY,
    "procedure": NONIDENTITY,
    "flow": NONIDENTITY, "flows": NONIDENTITY,
    "flux": NONIDENTITY, "throughput": NONIDENTITY,
    "field": NONIDENTITY,
    "equilibrium": NONIDENTITY, "equilibria": NONIDENTITY,
    "loop": NONIDENTITY, "loops": NONIDENTITY,
    "feedback": NONIDENTITY, "coupling": NONIDENTITY,
    "rate": NONIDENTITY, "rates": NONIDENTITY,
    "gradient": NONIDENTITY, "gradients": NONIDENTITY,
    "elasticity": NONIDENTITY,
    "convention": IDENTITY, "conventions": IDENTITY,
    "information": NONIDENTITY, "signal": NONIDENTITY,
    "allocation": NONIDENTITY, "selection": NONIDENTITY,
    "transmission": NONIDENTITY, "diffusion": NONIDENTITY,
}

# Two-token units, checked BEFORE the unigram table.
#
# `state` is why this exists. BOUNDARY.md D3 files `state, nation,
# jurisdiction` as identity-bearing and `equilibrium, steady state` as
# non-identity, so the bare head noun `state` carries two opposite calls
# under two senses. `--selftest` found the collision; it was not noticed
# while the table was being written. This is case 021's sense-substitution
# operating inside this detector's own vocabulary, and the repair is a
# modifier check, not a better word list.
BIGRAM_TABLE = {
    ("steady", "state"): NONIDENTITY,
    ("stationary", "state"): NONIDENTITY,
    ("ground", "state"): NONIDENTITY,
    ("feedback", "loop"): NONIDENTITY,
    ("nation", "state"): IDENTITY,
    ("member", "state"): IDENTITY,
}

# Head nouns known to carry more than one D3 call depending on a modifier.
# A bare occurrence is reported, not guessed.
AMBIGUOUS_HEAD = {"state", "states"}

# BOUNDARY.md D2 and D3: decided at the claim, not at the noun.
CLAIM_LEVEL = {"market", "markets", "system", "systems",
               "network", "networks"}

# Predicate classes for the claim-level decision.
# A property or state-change attached TO the subject -> the subject is the
# carrier. An operation the subject performs ON something else -> the
# subject is the mechanism.
CARRIER_VERBS = re.compile(
    r"^(is|are|was|were|has|have|had|becomes?|became|remains?|remained|"
    r"tightened?|loosened?|declines?|declined|grew|grows|shrank|shrinks|"
    r"collapsed?|persists?|persisted|survives?|survived|fails?|failed|"
    r"expands?|expanded|contracts?|contracted|recovers?|recovered)$")

MECHANISM_VERBS = re.compile(
    r"^(allocates?|allocated|clears?|cleared|distributes?|distributed|"
    r"transmits?|transmitted|propagates?|propagated|mediates?|mediated|"
    r"regulates?|regulated|coordinates?|coordinated|routes?|routed|"
    r"converts?|converted|dissipates?|dissipated)$")

RESULT_FIRST_PERSON = re.compile(
    r"\b(we find|we show|we demonstrate|we argue|we report|"
    r"results show|results indicate|findings show|here we)\b", re.I)

CAUSAL = re.compile(
    r"\b(causes?|caused|drives?|drove|driven|increases?|increased|"
    r"reduces?|reduced|decreases?|decreased|predicts?|predicted|"
    r"leads? to|led to|produces?|produced|determines?|determined|"
    r"explains?|explained)\b", re.I)

# Step 2 is partly lexical too, and this is where. A stdlib heuristic with
# no parser cannot find a base-form or irregular finite verb by shape, so
# both are supplied as closed lists. The `[a-z]+(?:s|ed)` branch is barred
# at position 0 because it matches plural nouns -- `firms`, `populations`,
# `households` were all read as verbs before that guard, which is what took
# the first null-test run to 6 of 12. Recorded in FINDINGS T1-2.
AUX = ("is|are|was|were|has|have|had|does|do|did|can|could|will|would|"
       "may|might|must|should|becomes?|became|remains?|remained")

IRREGULAR = ("fell|rose|grew|shrank|took|made|led|drove|held|went|ran|"
             "gave|found|saw|said|arose|began|broke|chose|kept|lost|"
             "spread|struck|withstood")

BASE_FORM = ("smooth|reduce|increase|persist|decline|allocate|respond|"
             "vary|depend|predict|explain|produce|determine|drive|cause|"
             "lead|remain|occur|emerge|exhibit|show|find|shape|track|"
             "scale|couple|dissipate|propagate|mediate|constrain")

FINITE_ANY = re.compile(r"^(%s|%s|%s)$" % (AUX, IRREGULAR, BASE_FORM), re.I)
FINITE_GREEDY = re.compile(r"^[a-z]+(?:s|ed)$", re.I)

SUBORDINATOR = re.compile(
    r"^(although|though|while|whereas|because|since|if|when|after|before|"
    r"here|thus|therefore|however|moreover|in|by|for|with|under|across|"
    r"using|through|despite|given|based)\b", re.I)

DETERMINER = {"the", "a", "an", "this", "that", "these", "those", "our",
              "their", "its", "his", "her", "such", "each", "every",
              "some", "any", "no", "both", "all", "most", "many", "few"}

PRONOUN = {"it", "they", "we", "this", "that", "these", "those", "there",
           "one", "which", "who"}

STOP_MOD = {"of", "in", "on", "for", "with", "and", "or", "to", "from",
            "as", "at", "by"}


def sentences(text):
    """Split on sentence-final punctuation. Crude and stated as crude."""
    parts = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    return [p.strip() for p in parts if p.strip()]


def main_claim(abstract):
    """BOUNDARY.md D0. Returns (sentence, rule_number)."""
    sents = sentences(abstract)
    if not sents:
        return None, 0
    for s in reversed(sents):
        if RESULT_FIRST_PERSON.search(s):
            return s, 1
    for s in reversed(sents):
        if CAUSAL.search(s):
            return s, 2
    return sents[-1], 3


def _strip_lead(sentence):
    """Drop a leading subordinate clause or adverbial, if any."""
    s = sentence.strip()
    if SUBORDINATOR.match(s):
        m = re.search(r",\s*", s)
        if m:
            return s[m.end():]
    m = re.match(r"^(we find|we show|we demonstrate|we argue|we report|"
                 r"results show|results indicate|findings show|here we)"
                 r"\s*(that)?\s*", s, re.I)
    if m:
        return s[m.end():]
    return s


def subject_span(sentence):
    """Text before the first finite verb. Heuristic, no parser."""
    s = _strip_lead(sentence)
    toks = s.split()
    for i, t in enumerate(toks):
        bare = re.sub(r"[^A-Za-z-]", "", t).lower()
        if not bare:
            continue
        if i == 0 and bare in DETERMINER:
            continue
        if bare in DETERMINER or bare in STOP_MOD:
            continue
        if FINITE_ANY.match(bare):
            return " ".join(toks[:i]), " ".join(toks[i:])
        if i >= 1 and FINITE_GREEDY.match(bare):
            return " ".join(toks[:i]), " ".join(toks[i:])
    return s, ""


PREP = {"of", "through", "in", "with", "on", "for", "across", "from",
        "by", "at", "under", "over", "between", "among", "during",
        "within", "without", "into", "onto", "about"}


def _core(span):
    """Span up to its first preposition. `the rate of transmission` -> `the
    rate`; `energy flux through the boundary layer` -> `energy flux`. Without
    this the head noun is taken from the prepositional phrase, which is a
    different unit from the one the claim is about."""
    toks = [re.sub(r"[^A-Za-z-]", "", t).lower() for t in span.split()]
    toks = [t for t in toks if t]
    for i, t in enumerate(toks):
        if t in PREP and i > 0:
            return toks[:i]
    return toks


def head_bigram(span):
    """Last two content tokens, for BIGRAM_TABLE. None if fewer than two."""
    toks = _core(span)
    while toks and toks[-1] in STOP_MOD:
        toks.pop()
    if len(toks) < 2:
        return None
    return (toks[-2], toks[-1])


def head_noun(span):
    """Last content token of the subject span, minus trailing modifiers."""
    toks = _core(span)
    while toks and toks[-1] in STOP_MOD:
        toks.pop()
    if not toks:
        return None
    for t in reversed(toks):
        if t in DETERMINER or t in STOP_MOD:
            continue
        return t
    return None


def first_verb(rest):
    toks = rest.split()
    if not toks:
        return None
    return re.sub(r"[^A-Za-z-]", "", toks[0]).lower()


def classify(abstract):
    """
    Returns a dict. `decided_by` says which of the three steps produced the
    label, so the lexical share of the answer is countable.
    """
    claim, rule = main_claim(abstract)
    out = {"claim": claim, "claim_rule": rule, "subject": None,
           "head": None, "verb": None, "label": UNDECIDABLE,
           "decided_by": BY_NEITHER, "why": ""}
    if claim is None:
        out["why"] = "no sentence"
        return out
    span, rest = subject_span(claim)
    head = head_noun(span)
    verb = first_verb(rest)
    bigram = head_bigram(span)
    out["subject"], out["head"], out["verb"] = span, head, verb
    out["bigram"] = bigram
    if bigram in BIGRAM_TABLE:
        out["label"], out["decided_by"] = BIGRAM_TABLE[bigram], BY_TABLE
        out["why"] = "D3 two-token unit %r" % (" ".join(bigram),)
        return out
    if head is None:
        out["why"] = "no extractable subject"
        return out
    if head in PRONOUN:
        out["why"] = "subject is a pronoun with no in-abstract antecedent"
        return out
    if head in CLAIM_LEVEL:
        if verb and CARRIER_VERBS.match(verb):
            out["label"], out["decided_by"] = IDENTITY, BY_PREDICATE
            out["why"] = "claim-level noun, carrier predicate"
        elif verb and MECHANISM_VERBS.match(verb):
            out["label"], out["decided_by"] = NONIDENTITY, BY_PREDICATE
            out["why"] = "claim-level noun, mechanism predicate"
        else:
            out["why"] = ("claim-level noun, predicate not in either class "
                          "-- D2 says this is undecidable at the noun")
        return out
    if head in AMBIGUOUS_HEAD:
        out["why"] = ("head noun %r carries two opposite D3 calls under two "
                      "senses and no modifier resolved it" % head)
        return out
    if head in UNIT_TABLE:
        out["label"], out["decided_by"] = UNIT_TABLE[head], BY_TABLE
        out["why"] = "D3 unit table"
        return out
    out["why"] = "head noun not in D3 table and not claim-level"
    return out


# --------------------------------------------------------------------------
# Null test. null-harness discipline: a detector that always fires and a
# detector that never fires both pass an assertion that it CAN fire.
#
# LIMIT, stated before the numbers: the ground truth below was authored by
# the same party that wrote the classifier. This measures internal
# consistency, not validity. It is triad-playground TP_003's shared-bias
# result applied to this harness, and it is not repaired by adding cases.
# --------------------------------------------------------------------------

KNOWN_SIGNAL = [
    ("We find that firms with concentrated ownership reduce investment "
     "following the reform.", IDENTITY),
    ("We show that populations declined across all sampled sites.",
     IDENTITY),
    ("Results indicate that households smooth consumption across shocks.",
     IDENTITY),
    ("We argue that the norm eroded once enforcement lapsed.", IDENTITY),
    ("We demonstrate that institutions persist long after the conditions "
     "that produced them.", IDENTITY),
    ("We find that energy flux through the boundary layer increases with "
     "surface roughness.", NONIDENTITY),
    ("We show that the feedback loop stabilizes at moderate gain.",
     NONIDENTITY),
    ("Results show that allocation proceeds without any central "
     "coordinator.", NONIDENTITY),
    ("We report that the niche remained unoccupied for three seasons.",
     NONIDENTITY),
    ("We find that the rate of transmission fell after the intervention.",
     NONIDENTITY),
    ("The labour market tightened over the following two quarters.",
     IDENTITY),
    ("The market allocates scarce goods without a designer.", NONIDENTITY),
]

KNOWN_NULL = [
    "It increased sharply thereafter.",
    "They were observed under both conditions.",
    "This remains an open question.",
    "There is considerable variation across settings.",
    "Further work is needed.",
]


def _fail_class(tp, fp, n_sig, n_null):
    if tp == 0 and fp == 0:
        return "CONSTANT_SILENT"
    if tp == n_sig and fp == n_null:
        return "CONSTANT_FIRES"
    if n_null and fp / float(n_null) > 0.10:
        return "TOO_MANY_FALSE_ALARMS"
    if n_sig and tp / float(n_sig) <= (fp / float(n_null) if n_null else 0):
        return "NO_DISCRIMINATION"
    return "OK"


def null_test(verbose=True):
    tp = 0
    wrong = []
    for text, truth in KNOWN_SIGNAL:
        got = classify(text)
        if got["label"] == truth:
            tp += 1
        else:
            wrong.append((text, truth, got["label"], got["why"]))
    fp = 0
    fired = []
    for text in KNOWN_NULL:
        got = classify(text)
        if got["label"] != UNDECIDABLE:
            fp += 1
            fired.append((text, got["label"], got["why"]))
    cls = _fail_class(tp, fp, len(KNOWN_SIGNAL), len(KNOWN_NULL))
    if verbose:
        print("NULL TEST")
        print("  known-signal recovered : %d/%d"
              % (tp, len(KNOWN_SIGNAL)))
        print("  known-null fired       : %d/%d"
              % (fp, len(KNOWN_NULL)))
        print("  fail class             : %s" % cls)
        print("  ground truth authored by the same party as the classifier;")
        print("  this is internal consistency, not validity (TP_003).")
        for t, truth, got, why in wrong:
            print("  MISS  want=%s got=%s :: %s" % (truth, got, why))
            print("        %s" % t)
        for t, got, why in fired:
            print("  FIRED ON NULL got=%s :: %s" % (got, why))
            print("        %s" % t)
    return {"tp": tp, "fp": fp, "n_signal": len(KNOWN_SIGNAL),
            "n_null": len(KNOWN_NULL), "fail_class": cls,
            "misses": wrong, "fired_on_null": fired}


def _boundary_table():
    """Parse BOUNDARY.md D3 so the transcription can be checked."""
    calls = {}
    if not os.path.exists(BOUNDARY):
        return calls
    with open(BOUNDARY) as fh:
        text = fh.read()
    for line in text.split("\n"):
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) < 2:
            continue
        units, call = cells[0], cells[1]
        if "identity-bearing" in call and "non-identity" not in call:
            v = IDENTITY
        elif "non-identity" in call:
            v = NONIDENTITY
        else:
            continue
        for u in units.replace("**", "").split(","):
            u = u.strip().split("(")[0].strip().lower()
            if u:
                calls[u] = v
    return calls


def selftest():
    fails = []
    calls = _boundary_table()
    if not calls:
        fails.append("BOUNDARY.md D3 table not parsed -- cannot check "
                     "transcription")
    for unit, want in calls.items():
        singular = unit.rstrip("s") if unit.endswith("s") else unit
        if unit in CLAIM_LEVEL or singular in CLAIM_LEVEL:
            continue
        parts = tuple(unit.split())
        if len(parts) == 2 and parts in BIGRAM_TABLE:
            if BIGRAM_TABLE[parts] != want:
                fails.append("D3 unit %r: BOUNDARY says %s, BIGRAM_TABLE "
                             "says %s" % (unit, want, BIGRAM_TABLE[parts]))
            continue
        got = UNIT_TABLE.get(unit, UNIT_TABLE.get(singular))
        if got is None:
            fails.append("D3 unit %r absent from UNIT_TABLE" % unit)
        elif got != want:
            fails.append("D3 unit %r: BOUNDARY says %s, UNIT_TABLE says %s"
                         % (unit, want, got))
    for text, truth in KNOWN_SIGNAL:
        c = classify(text)
        if c["claim"] is None:
            fails.append("no claim extracted from %r" % text[:40])
    if classify("")["label"] != UNDECIDABLE:
        fails.append("empty input must be UNDECIDABLE")
    r = null_test(verbose=False)
    if r["fail_class"] == "CONSTANT_SILENT":
        fails.append("null test says CONSTANT_SILENT")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def report(abstracts):
    """Run T1 over a list of (id, field, abstract). Returns rows."""
    rows = []
    for aid, fld, text in abstracts:
        c = classify(text)
        c["id"], c["field"] = aid, fld
        rows.append(c)
    return rows


def summarize(rows):
    out = {"n": len(rows), IDENTITY: 0, NONIDENTITY: 0, UNDECIDABLE: 0,
           BY_PREDICATE: 0, BY_TABLE: 0, BY_NEITHER: 0, "rule": {1: 0, 2: 0, 3: 0}}
    for r in rows:
        out[r["label"]] += 1
        out[r["decided_by"]] += 1
        if r["claim_rule"] in out["rule"]:
            out["rule"][r["claim_rule"]] += 1
    return out


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--null" in argv:
        null_test()
        return 0
    if "--demo" in argv:
        rows = report([("KS-%02d" % i, "authored", t)
                       for i, (t, _) in enumerate(KNOWN_SIGNAL, 1)])
        s = summarize(rows)
        print("T1 over the authored known-signal set (NOT a corpus)")
        for r in rows:
            print("  %-7s %-16s %-9s head=%-14s %s"
                  % (r["id"], r["label"], r["decided_by"],
                     r["head"], r["why"]))
        print("  decided by predicate: %d  by table: %d  undecidable: %d"
              % (s[BY_PREDICATE], s[BY_TABLE], s[BY_NEITHER]))
        return 0
    print(__doc__.strip())
    print("\nusage: t1_predicate_unit.py [--selftest | --null | --demo]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
