#!/usr/bin/env python3
"""cuts_c5_probe.py -- tests two proposed additions to 023's cut set.

Added, not delivered. `selection_cuts.py` implements T1 exactly as 023
specifies it and is NOT modified here. This script imports it and asks whether
two proposed cuts do work the delivered four do not.

    python3 cuts_c5_probe.py

THE PROPOSALS (maintainer, in session, 2026-08-18):

  C5 ENVIRONMENT MULTIPLICITY
     "the selection is based upon the structure not on the environment, and
      tested in only one exclusive environment with all other environments
      withheld as non options... selection or evolution cannot apply
      realistically if other environments, alternatives, interactions have
      been actively excluded as structure."
     Offered case: "it would be like saying that gasoline engines are
      evolution or have been environmentally selected."

  C2' ARBITRATION  (a re-scoring of the delivered C2, not a new condition)
     023's C2 asks who AUTHORED the environment. Its own stated consequence
     asks something else: "The criterion does not return a reading. It returns
     a decision someone made." UNI_148 found C2 inert as authorship. This tests
     whether it separates as arbitration.

Both are scored here for the first time. The scores are AUTHORED by this audit
and are the input, not a result.

stdlib only, deterministic. CC0.
"""

import itertools
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selection_cuts as SC                                     # noqa: E402

BAR = "=" * 72

C5_VALUES = ["PLURAL_UNCONTROLLED", "MIXED", "SINGLE_ALTERNATIVES_EXCLUDED"]
ARB_VALUES = ["WORLD_RETURNS_READING", "MIXED", "PARTY_RETURNS_DECISION"]

# proposed scores. AUTHORED by this audit.
PROPOSED = {
    "population_genetics":      ("PLURAL_UNCONTROLLED", "WORLD_RETURNS_READING"),
    "antibiotic_resistance":    ("MIXED", "WORLD_RETURNS_READING"),
    "directed_evolution":       ("SINGLE_ALTERNATIVES_EXCLUDED",
                                 "WORLD_RETURNS_READING"),
    "evolutionary_algorithms":  ("SINGLE_ALTERNATIVES_EXCLUDED",
                                 "WORLD_RETURNS_READING"),
    "lysenkoism":               ("SINGLE_ALTERNATIVES_EXCLUDED",
                                 "PARTY_RETURNS_DECISION"),
    "eugenics":                 ("SINGLE_ALTERNATIVES_EXCLUDED",
                                 "PARTY_RETURNS_DECISION"),
    "spencer_social_darwinism": ("MIXED", "PARTY_RETURNS_DECISION"),
    "alchian_firm_selection":   ("MIXED", "MIXED"),
    "memetics":                 ("PLURAL_UNCONTROLLED", "MIXED"),
}
SUBJ = ("SINGLE_ALTERNATIVES_EXCLUDED", "PARTY_RETURNS_DECISION")

# the maintainer's own offered case, added as a new calibration point.
GASOLINE = {
    "expects": "BORROWED",
    "note": "maintainer's offered case. Nobody says gasoline engines were "
            "environmentally selected, though the refinement is real and "
            "iterated. Infrastructure, fuel supply and regulation excluded "
            "alternatives structurally.",
    "C1_exclusivity": "NON_EXCLUSIVE",
    "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
    "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
    "C4_application_grain": "PER_ROUND_UNIFORM",
}
GASOLINE_PROPOSED = ("SINGLE_ALTERNATIVES_EXCLUDED", "PARTY_RETURNS_DECISION")


def head(n, title):
    print()
    print(BAR)
    print("%d  %s" % (n, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def build(extra_case=None, include=("C5", "ARB")):
    """Assemble a case table with the proposed cuts appended."""
    cases = OrderedDict()
    for name, c in SC.CALIBRATION.items():
        d = dict(c)
        if "C5" in include:
            d["C5_environment_multiplicity"] = PROPOSED[name][0]
        if "ARB" in include:
            d["C2prime_arbitration"] = PROPOSED[name][1]
        cases[name] = d
    if extra_case:
        cases["gasoline_engine"] = extra_case
    return cases


def cuts_for(include):
    c = list(SC.CUTS)
    if "C5" in include:
        c.append("C5_environment_multiplicity")
    if "ARB" in include:
        c.append("C2prime_arbitration")
    return c


def separates(cases, subset):
    vec = {}
    for c in cases.values():
        vec.setdefault(tuple(c[x] for x in subset), set()).add(c["expects"])
    return all(len(v) == 1 for v in vec.values())


def per_cut(cases, cuts):
    out = OrderedDict()
    for cut in cuts:
        lit = set(c[cut] for c in cases.values() if c["expects"] == "LITERAL")
        bor = set(c[cut] for c in cases.values() if c["expects"] == "BORROWED")
        out[cut] = sorted(lit & bor)
    return out


print("cuts_c5_probe -- two proposed additions to 023's cut set")
print("selection_cuts.py is imported and not modified")

# ---------------------------------------------------------------- 1
head(1, "does C5 separate on its own?")

cases = build()
cuts = cuts_for(("C5", "ARB"))
ov = per_cut(cases, cuts)
print("    %-34s %-10s %s" % ("cut", "separates", "overlapping values"))
for cut in cuts:
    print("    %-34s %-10s %s"
          % (cut, "yes" if not ov[cut] else "NO", ", ".join(ov[cut]) or "-"))

block("""
C5 as the maintainer states it does NOT separate the calibration set, and it
fails on the same case C2 failed on.

`directed_evolution` and `evolutionary_algorithms` are single authored
environments with alternatives excluded by construction -- a binding assay
admits one condition and no other -- and 023's NOT CLAIMED HERE names both as
domains where the vocabulary is CORRECT. So "one exclusive environment,
alternatives withheld" is a property shared by the clearest literal cases and
the subject.

That is `UNI_148` again with a different label, which is worth knowing before
anything is built on C5.
""")

# ---------------------------------------------------------------- 2
head(2, "does the ARBITRATION re-scoring separate where authorship did not?")

print("    C2  as authorship  -- overlapping values: %s"
      % (", ".join(ov["C2_authorship"]) or "none: SEPARATES"))
print("    C2' as arbitration -- overlapping values: %s"
      % (", ".join(ov["C2prime_arbitration"]) or "none: SEPARATES"))
print()
print("    %-26s %-32s %s" % ("case", "arbitration", "class"))
for n, c in cases.items():
    print("    %-26s %-32s %s"
          % (n, c["C2prime_arbitration"], c["expects"]))

block("""
It separates. Every LITERAL case has the world returning the reading; every
BORROWED case has a party returning a decision, or is mixed on the borrowed
side only.

This is the substantive result of the probe. 023's C2 asks who AUTHORED the
environment and comes back inert. Its own next sentence asks the discriminating
question -- "The criterion does not return a reading. It returns a decision
someone made" -- and that separates cleanly.

So the maintainer's objection lands, one step over from where it was aimed. The
problem is not that the environment is singular or authored; directed evolution
is both and the word holds there. The problem is that in a directed-evolution
assay the molecule either binds or it does not, and nobody decides that. The
authoring stops at the environment and the arbitration is physical.

Restated as a condition: **selection requires that the criterion be settled by
the world rather than by a party.** That is what C2 was reaching for and is not
what C2 measures.
""")

# ---------------------------------------------------------------- 3
head(3, "the gasoline engine, added as a calibration case")

g = dict(GASOLINE)
g["C5_environment_multiplicity"] = GASOLINE_PROPOSED[0]
g["C2prime_arbitration"] = GASOLINE_PROPOSED[1]
cases_g = build(extra_case=g)
ovg = per_cut(cases_g, cuts)
print("    with gasoline_engine added (%d cases):" % len(cases_g))
for cut in cuts:
    print("      %-34s %s"
          % (cut, "separates" if not ovg[cut] else "overlap: %s"
             % ", ".join(ovg[cut])))
print()
print("    delivered four, as a vector, still separate: %s"
      % separates(cases_g, list(SC.CUTS)))
print("    arbitration alone still separates:           %s"
      % separates(cases_g, ["C2prime_arbitration"]))
print()
sv = tuple(SUBJ)
gv = (g["C5_environment_multiplicity"], g["C2prime_arbitration"])
print("    gasoline_engine vs the subject on the two proposed cuts:")
print("      gasoline: %s" % (gv,))
print("      subject:  %s" % (sv,))
print("      identical: %s" % (gv == sv))

block("""
The offered case behaves as offered. It is BORROWED -- nobody says gasoline
engines were environmentally selected -- and it scores identically to the
subject on both proposed cuts, which is the comparison the maintainer drew.

It also survives the delivered four without breaking them, so adding it costs
the existing instrument nothing.

Worth noting what it does to C4. The gasoline engine scores PER_ROUND_UNIFORM:
engines competed against reasonably uniform criteria within an era. So a case
can be clearly borrowed while satisfying C4, which is a second reason -- after
`UNI_149` -- not to read C4 as the cut that ends the analogy.
""")

# ---------------------------------------------------------------- 4
head(4, "minimal separating subsets, delivered four vs delivered + arbitration")

for label, sub in (("delivered four", list(SC.CUTS)),
                   ("delivered + C5 + arbitration", cuts)):
    minimal = []
    for r in range(1, len(sub) + 1):
        for combo in itertools.combinations(sub, r):
            if separates(cases_g, combo) and not any(
                    set(f) < set(combo) for f in minimal):
                minimal.append(combo)
    print("    %-30s %s" % (label,
                            "; ".join(" + ".join(x.split("_")[0] for x in m)
                                      for m in minimal) or "none separate"))

block("""
On the ten-case set including the gasoline engine, arbitration separates alone
and so does C3. C5 appears in no minimal subset.

Read together with `UNI_147`, the honest shape of the instrument is two
conditions rather than four or six:

  - C3, the criterion holds still long enough for anything to accumulate
  - ARBITRATION, the criterion is settled by the world rather than by a party

Each separates the calibration set alone. C1, C2-as-authorship, C4 and C5 all
take values that appear in both classes, on ten cases coded from 023's own
descriptions plus the maintainer's offered one.

Not a claim that the others are wrong about the AI case. A claim about which
of them are carrying the discrimination, which is what a calibration set is
for.
""")

print()
print(BAR)
print("end of probe -- recorded in AUDIT_NOTES.md as UNI_154..UNI_156")
print(BAR)
