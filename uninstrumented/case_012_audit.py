#!/usr/bin/env python3
"""case_012_audit.py -- checks on the Case 012 drop.

Added, not delivered. `cases/012fuelincidencesubstrategoods.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_027..UNI_033.

    python3 case_012_audit.py

Case 012 is the third consecutive delivered case the register's schema
cannot hold, and the first whose stated confidence is checkable by
computation rather than recorded verbatim.

LITERATURE CHECKS. Four of the checks below were run against the open web
on 2026-08-18 and are marked. They are NOT reproducible by running this
script -- it does no network access. Section 1 is arithmetic and IS
reproducible; it is the only section that settles anything on its own.

stdlib only, deterministic. CC0.
"""

import io
import os
import re

import uninstrumented as U

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = io.open(os.path.join(HERE, "cases", "012fuelincidencesubstrategoods.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


subq = re.findall(r"^## (Q\d) — (.*)$", CASE, re.M)
print("uninstrumented -- audit of the Case 012 drop")
print("delivered: cases/012fuelincidencesubstrategoods.md")
print("cluster   : %d sub-questions, mechanism candidates named not assigned"
      % len(subq))

# ---------------------------------------------------------------- UNI_027

head(1, "UNI_027", "Q1's confidence claim is checkable, and it holds")
block("""
The entry states its own confidence on Q1 as "high -- arithmetic, not
hypothesis". That is the first confidence claim in this register that can
be settled by computing rather than by taking the author's word, so it is
computed.

The identity. Let class i deliver n_i loads of value v_i each at freight
cost f_i each. The published aggregate is total freight over total value:

    F / V  =  sum_i n_i f_i  /  sum_i n_i v_i

which rearranges to

    F / V  =  sum_i  ( n_i v_i / V ) * ( f_i / v_i )

-- a mean of the PER-CLASS ratios f_i/v_i, weighted by each class's share
of total VALUE. So the aggregate is not a summary of freight burden across
classes; it is a summary weighted toward whichever class carries the
dollars. The entry's claim is an algebraic identity, not a model.
""")
CLASSES = [
    ("electronics, dry van", 1000, 500000.0, 2000.0),
    ("produce, reefer", 1000, 45000.0, 3200.0),
    ("structural steel, flatbed", 1000, 20000.0, 2500.0),
    ("transformer, oversize", 50, 180000.0, 14000.0),
]
V = sum(n * v for _, n, v, _ in CLASSES)
F = sum(n * f for _, n, _, f in CLASSES)
print()
print("  %-26s %10s %9s %8s %8s"
      % ("illustrative class", "value/load", "freight", "ratio", "$ weight"))
print("  " + "-" * 66)
for name, n, v, f in CLASSES:
    print("  %-26s %10.0f %9.0f %7.2f%% %7.2f%%"
          % (name, v, f, 100 * f / v, 100 * n * v / V))
agg = F / V
wmean = sum((n * v / V) * (f / v) for _, n, v, f in CLASSES)
print()
print("  aggregate      F/V                = %6.3f%%" % (100 * agg))
print("  same, as the weighted mean above  = %6.3f%%" % (100 * wmean))
print("  unweighted mean of class ratios   = %6.3f%%"
      % (100 * sum(f / v for _, _, v, f in CLASSES) / len(CLASSES)))
worst = max(CLASSES, key=lambda c: c[3] / c[2])
print()
print("  identity holds exactly            : %s" % (abs(agg - wmean) < 1e-12))
print("  worst class (%s)" % worst[0])
print("    its own ratio                   = %6.2f%%" % (100 * worst[3] / worst[2]))
print("    the aggregate reports           = %6.2f%%" % (100 * agg))
print("    understatement factor           = %6.1fx" % ((worst[3] / worst[2]) / agg))
block("""
The illustrative numbers are chosen to be plausible and are not data --
what they demonstrate is the mechanism, and the mechanism is exact. One
class holding 87% of the dollars pulls the aggregate to 1.46% while the
worst-affected class sits at 12.50%.

So Q1 is correct, and correct in a stronger sense than the entry claims
for it. It does not need the freight numbers to be right. Any mix in which
value-density varies across classes produces the same effect, and the
effect is largest exactly where the entry says the interesting classes
are: low value per pound, small share of total dollars.

This also makes Case 012 the first entry whose confidence field is not
merely recorded verbatim (`UNI_014`, `UNI_021`) but adjudicable -- and it
adjudicates in the entry's favour.
""")

# ---------------------------------------------------------------- UNI_028

head(2, "UNI_028", "a fourth confidence state: split across the cluster")
conf = CASE.split("## CONFIDENCE", 1)[1].split("## FALSIFIERS", 1)[0]
print()
for line in [l for l in conf.splitlines() if l.strip()]:
    print("  %s" % line.strip())
print()
print("  states now seen in the wild:")
print("    high, one string                8 of 8 original entries")
print("    one gradient (~40 percent)      Case 010")
print("    deliberately absent, with why   Case 011")
print("    SPLIT across sub-questions      Case 012")
print("  states entry() can represent   : 1 (a single string)")
block("""
`entry()` takes one `confidence`. Case 012 states a different confidence
for Q1 than for Q2-Q4, and gives the reason for the split: the later
questions are causal chains that need Q1's data to exist before a gradient
would mean anything.

That is the `UNI_020` sub-entry repair reaching a second field. A cluster
needs per-question `excluded_by` and `would_measure`; it also needs
per-question `confidence`, and for the same reason -- the questions close
at different times and on different evidence.

Three cases, three different ways the one-string field fails: too coarse
(`UNI_014`), unable to record a reasoned absence (`UNI_021`), unable to
record a split (here).
""")

# ---------------------------------------------------------------- UNI_029

head(3, "UNI_029", "a negative-provenance record, which is new here")
note = CASE.split("## NOTE ON A CIRCULATING NUMBER", 1)[1].split(
    "## CONFIDENCE", 1)[0]
print()
for line in [l for l in note.splitlines() if l.strip()]:
    print("  %s" % line.strip())
block("""
This has no precedent in the register and no slot in the schema, and it is
the strongest methodological move in the drop.

Every prior literature finding in this drop family runs the other
direction: `ANC_010`, `CD_009`, `RD_015`, `HO_005` are all citation
markers that pointed outside the delivery, found afterwards by an auditor
and marked UNVERIFIED. Case 012 marks the numbers BEFORE anyone builds on
them, names where they circulate, states that no peer-reviewed origin was
located, and says why the note exists: "recorded so the next reader does
not mistake them for literature."

An entry that carries its own do-not-use list is doing the auditor's job
in the direction that is cheap -- at authoring time, by the person who
knows which numbers were tempting. Doing it afterwards is what costs.

The jet-fuel item is handled the same way and is filed correctly:
attributed to a source class ("at least one large 3PL"), marked
unverified, and listed as a check rather than as a finding. Neither number
appears anywhere else in the entry's reasoning -- checked: no reasoning
step depends on 4.75, 5.25, or the jet-fuel claim.
""")
for tok in ("4.75", "5.25", "jet fuel"):
    body = CASE.split("## NOTE ON A CIRCULATING NUMBER", 1)[0]
    print("  %-10s appears outside the note: %s" % (tok, tok in body))

# ---------------------------------------------------------------- UNI_030

head(4, "UNI_030", "the published finding, checked  [web, 2026-08-18]")
print()
for claim, status, note_ in (
    ("~50% of a diesel price change reaches shippers immediately",
     "CONFIRMED", "reported as 50% immediate pass-through"),
    ("near 100% within one week", "CONFIRMED",
     "reported as reaching 100% within a week, contract and spot"),
    ("carriers do not absorb it -- thin margins, competitive market",
     "CONFIRMED", "reported as market structure driving full pass-through; "
                  "carriers unable to absorb without risking failure"),
):
    print("  %-9s %s" % (status, claim))
    for i in range(0, len(note_), 60):
        print("            %s" % note_[i:i + 60])
block("""
Third consecutive occasion in this register that checks out, after
`UNI_015` (Case 010) and `UNI_023` (Case 011). The entry's summary of the
pass-through work is accurate, including the mechanism it attributes the
result to.
""")

# ---------------------------------------------------------------- UNI_031

head(5, "UNI_031", "the rate figure does not check out as stated  [web, 2026-08-18]")
print()
print("  entry states : flatbed roughly $0.70-$1.20/mile above dry van,")
print("                 2026 spot data")
print()
print("  located      : early 2026 national spot averages")
print("                   dry van $2.47  flatbed $2.95  reefer $2.88")
print("                   -> premium $0.48")
print("                 March 2026, stated directly")
print("                   -> flatbed $0.48/mile above dry van")
print("                 late July 2026")
print("                   flatbed $3.72, reefer $3.39, no matched dry van")
block("""
The one explicitly published premium located is $0.48/mile, which is below
the bottom of the entry's stated range, and the early-2026 averages give
the same figure independently. No matched-date pair was located for late
2026, when flatbed alone is quoted much higher, so the range may hold at
some date or on some lanes -- but it is not what the located 2026 spot
data shows, and the entry cites "2026 spot data".

**This does not touch Q1.** Q1's claim is the identity in section 1, which
holds for any mix in which value-density varies and does not depend on the
size of the flatbed premium. What the correction changes is a downstream
magnitude: the premium is one input to the numerator Q1's WOULD MEASURE
asks for, and it appears to be roughly half the stated size.

Recorded rather than edited into the entry, which is delivered verbatim.
""")

# ---------------------------------------------------------------- UNI_032

head(6, "UNI_032", "Q4 splits three ways  [web, 2026-08-18]")
block("""
Q4's falsifier: "closes if national accounts already publish an adjustable
versus non-adjustable decomposition."

**Partially fires.** BLS publishes which item categories use hedonic
quality adjustment and publishes the share: excluding shelter, hedonic
methods are employed in categories comprising approximately **2.9% of the
CPI**. The adjusted set is enumerable and its weight is stated, which is
most of the decomposition Q4 asks for.

**The asymmetry claim is confirmed by the published list.** The categories
named are personal computers, televisions, consumer audio, VCRs,
camcorders, DVD players, apparel, microwave ovens, refrigerators, college
textbooks, and broadband for PPI. That is the high-value-density consumer
set exactly as Q4 predicts. Neither food nor electricity appears --
"a calorie has no new features. A kilowatt-hour has no new features" is
borne out by which categories the method is applied to.

**The magnitude constrains the mechanism.** Q4's stated test is that "the
aggregate can be held level by hedonic credit accruing to deniable-quality
goods while substrate goods degrade in real terms". At ~2.9% of the index
ex-shelter, that channel has a published upper bound on its leverage, and
the bound is small. The claim is now quantitative and the number is
against it.

**And there is a denominator switch worth naming.** Q4 is about GDP real
output, which is BEA and is deflated by price indexes; the 2.9% figure is
the CPI, which is BLS. The two are related through the deflators and are
not the same aggregate, so the located share bounds the channel in one of
them and leaves it unchecked in the other. That is
`../measurement-fork/`'s VOID RATIO shape -- a ratio whose two operands
are properties of different objects -- arriving inside a falsifier rather
than inside a result.

Not checked: the entry's claim that "the quality dimensions come largely
from the producer's own account of what improved". BLS hedonic models use
product characteristics data whose provenance was not established here.
""")

# ---------------------------------------------------------------- UNI_033

head(7, "UNI_033", "Q3's two halves have opposite epistemic status")
block("""
Q3 carries two claims and they are not alike.

**The non-linearity is a hypothesis with a good falsifier and no data
either way.** "A generator load postponed is postponed. A reefer load past
viability is destroyed." The entry's own falsifier is the sharpest in the
drop -- it fails "if reefer loads past viability are in practice rerouted
or downgraded at a rate that smooths the discontinuity" -- because it
names a specific industry practice that either happens at a measurable
rate or does not, and either answer is informative. That is a reachable
negative, so Q3 is not `CONSTANT_SILENT`.

The methodological line under it is stronger than the claim and stands on
its own: "Smooth elasticity models do not generate discontinuities -- the
functional form is wrong before any parameter is estimated." That is the
`../climate-modeling/` cascade-speed result in another domain, and this
repo has it twice already (`PhaseChangeAudit`, and
`../sustained-activation-gate/`'s double well).

**The accounting claim is true by construction and needs no search.** In
the national accounts, food bought by households is final consumption
expenditure -- it enters GDP on the output side, as C. Labour is a primary
input rather than a produced one, so it has no row in the intermediate
input-output matrix and the calories that sustain it are not intermediate
consumption of any industry. The entry's sentence

    The one input without which no other input can be produced is
    recorded as a consumption category

is a correct description of the framework, not a contested reading of it.

That asymmetry is worth stating because it inverts the usual pattern in
this register: the half with "WOULD MEASURE: unclear, flagged as needing
an instrument" is the half that is already established, and the half with
a clean falsifier is the one still open. The instrument is not missing
because the fact is uncertain -- it is missing because the framework has
no slot for the quantity, which is this register's own subject and would
make Q3 the entry's best candidate for a filed mechanism if one had to be
chosen today.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_027..UNI_033")
print(BAR)
