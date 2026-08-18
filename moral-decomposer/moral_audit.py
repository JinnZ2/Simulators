#!/usr/bin/env python3
"""moral_audit.py -- checks on the moral-decomposer drop.

Added, not delivered. README.md, CLAIM_TABLE.md and both files under
cases/ are the drop as received and are not modified. Findings are
recorded in AUDIT_NOTES.md as MD_001..MD_008.

    python3 moral_audit.py

decompose.py is named five times in the README and did not arrive. It is
NOT reconstructed: category-weld CW_004 is the cost of the one time a
reconstruction filled a gap of this kind, and the README fixes far less
of the arithmetic than that one did. Everything below is read off the
delivered case JSON.

stdlib only, deterministic. CC0.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


CASES = []
for f in sorted(os.listdir(os.path.join(HERE, "cases"))):
    if f.endswith(".json"):
        with open(os.path.join(HERE, "cases", f), encoding="utf-8") as fh:
            CASES.append(json.load(fh))

print("moral-decomposer -- audit of the delivered drop")
print("delivered: README.md, CLAIM_TABLE.md (M1-M5), %d case file(s)" % len(CASES))
print("NOT delivered: decompose.py, named five times in the README")

# ------------------------------------------------------------------ MD_001
head(1, "MD_001", "M5 rests entirely on the file that did not arrive")
print("""
M5: "Zero live residue across cases is an absence, not a proof."

    Status: stated in the tool output and enforced by the schema: the
    selftest includes a fixture with a live residue item, so a non-empty
    residue is representable and the instrument is not rigged toward M1.

That status has two halves and both are in decompose.py: the tool output
and the selftest fixture. Neither is in the drop.

M5 is the guard against the folder's central risk -- that a decomposer
built to show disagreements reduce will show them reducing. It is the one
claim whose whole content is "the detector can fire", and it is the one
claim that cannot be checked from the folder.
""".strip())
print()
tot = sum(len(c.get("residue_candidates", [])) for c in CASES)
live = [(c["case"], r) for c in CASES for r in c.get("residue_candidates", [])
        if not r.get("resolved")]
print("  residue candidates in the delivered corpus : %d" % tot)
print("  marked resolved                            : %d" % (tot - len(live)))
print("  live                                       : %d" % len(live))
print()
print("""
0 of %d. On the delivered data alone the instrument has never returned a
non-empty residue -- which is exactly what M5 says not to read as proof,
and exactly why the missing fixture is the load-bearing artifact.
null-harness grades a detector that has not been shown to fire
CONSTANT_SILENT; here the demonstration exists and was not shipped.

Fifth consecutive drop whose status sentence names an absent artifact
(CW_001 code, arrived; PB_001 data, arrived exact; GC_009 data,
outstanding; PB_015 tests, outstanding). The prior pattern is real and
late.
""".strip() % tot)

# ------------------------------------------------------------------ MD_002
head(2, "MD_002", "reduces_to: null carries two opposite meanings")
print("""
README, stage description:

    RESIDUE   candidates that reduce to stage 1 or 2 are accounted for.
              Candidates that reduce to neither are the case the
              instrument exists to find.

So `reduces_to: null` is the finding. In the delivered corpus:
""".strip())
print()
print("  %-16s %-52s %-9s %s" % ("case", "claim", "reduces_to", "resolved"))
print("  " + "-" * 92)
for c in CASES:
    for r in c.get("residue_candidates", []):
        print("  %-16s %-52s %-9s %s" % (
            c["case"], r["claim"][:52], r.get("reduces_to"), r.get("resolved")))
print()
print("""
The last row is `reduces_to: null` AND `resolved: true`. Its note says it
is not residue between the sides but agreement between them, routed to
presented-binary.

That reading is right, and it is the most interesting cell in the drop --
agreement across both sides is where a shared unmeasured assumption sits,
and the case says so. What it costs is the meaning of the field. A null
`reduces_to` now means either "irreducible, this is the finding" or "not
applicable, handled elsewhere", and only `resolved` separates them --
a boolean set by the case author with nothing checking it.

A third value would do it: reduces_to `option` / `frame` / `routed` /
null, with null reserved for the finding. Same shape as PB_012 and GC_004
one folder over -- a single value standing for a measurement and for its
own absence.
""".strip())

# ------------------------------------------------------------------ MD_003
head(3, "MD_003", "M3's asymmetry is exactly as stated")
print("""
M3's status: "asymmetry appears in both cases (3 undocumented cuts vs 0,
both times, in opposite file positions)."
""".strip())
print()
print("  %-16s %-10s %-24s %6s %6s" % (
    "case", "side", "boundary criterion", "cuts", "undoc"))
print("  " + "-" * 70)
for c in CASES:
    for s in c["sides"]:
        cuts = s["frame"].get("cuts_required", [])
        undoc = sum(1 for k in cuts if not k.get("documented"))
        print("  %-16s %-10s %-24s %6d %6d" % (
            c["case"], s["id"], s["frame"]["boundary_criterion"][:24],
            len(cuts), undoc))
print()
print("""
Confirmed to the digit, including the position claim: the 3-cut side is
second in animal-standing and first in means-to-save.

The status sentence also states its own limit -- "cut lists are enumerated
by hand, so the count reflects the enumerator, not a survey. Not a
measurement." That is the right reading and it is stronger than it looks:
a frame with no listed cuts scores as terminating, so the readout is
`CONSTANT_SILENT` on any frame nobody enumerated. `terminates` is a
separate asserted field that could disagree with the cut list and nothing
checks the two against each other.
""".strip())
for c in CASES:
    for s in c["sides"]:
        f = s["frame"]
        cuts = f.get("cuts_required", [])
        consistent = (f.get("terminates") is True) == (len(cuts) <= 1)
        print("  %-16s %-10s terminates=%-5s cuts=%d  consistent: %s" % (
            c["case"], s["id"], f.get("terminates"), len(cuts), consistent))

# ------------------------------------------------------------------ MD_004
head(4, "MD_004", "the run order is stated and the corpus does not follow it")
print("""
README, RUN ORDER:

    Welded terms first. If a term in the dispute fuses independent
    quantities, stage 1 will read divergence that is an artifact of the
    word. List them in `welded_terms` and decompose in `category-weld`
    before trusting the output.

The drop's own DISCLOSED WEAKNESSES agrees: "Nothing checks that the
decomposition happened first, and both cases carry unresolved welds."
Measured against the sibling folder:
""".strip())
weldsdir = os.path.join(ROOT, "category-weld", "welds")
have = set()
if os.path.isdir(weldsdir):
    have = {f[:-5] for f in os.listdir(weldsdir) if f.endswith(".json")}
print()
print("  %-16s %-16s %s" % ("case", "welded term", "in category-weld/welds/"))
print("  " + "-" * 56)
n_terms = n_have = 0
for c in CASES:
    for t in c.get("welded_terms", []):
        n_terms += 1
        key = t.replace(" ", "_")
        present = key in have or t in have
        n_have += present
        print("  %-16s %-16s %s" % (c["case"], t, present))
print()
print("  %d welded terms named, %d decomposed. category-weld holds: %s" % (
    n_terms, n_have, ", ".join(sorted(have)) or "none"))
print()
print("""
`the few` is `presented-binary` B5's "a few" under a different article --
the same term, now named from a second folder, and still with no
welds/a_few.json (PB_009). Two folders point at one missing file, and the
run order says the output of both is not trustworthy until it exists.

Not a defect in the cases. It is a stated precondition with nothing
enforcing it, and the shape recurs: measurement-fork MF_017, category-weld
CW_015, generation-capacity GC_003 -- a rule the prose states and the
schema has no slot to check.
""".strip())

# ------------------------------------------------------------------ MD_005
head(5, "MD_005", "the no-moral-labels rule holds against the delivered schema")
print("""
README: "Field names carry no moral terms. An instrument for reading
smuggled frames that smuggles one cannot do the job."

Checkable. Every field name that appears anywhere in the two case files:
""".strip())
MORAL = ("good", "bad", "right", "wrong", "ought", "should", "harm",
         "evil", "virtue", "vice", "moral", "ethic", "just", "unjust",
         "fair", "unfair", "deserve", "worthy", "innocent", "guilty")


def keys(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k)
            keys(v, acc)
    elif isinstance(o, list):
        for v in o:
            keys(v, acc)
    return acc


allkeys = sorted(keys(CASES, set()))
print()
for i in range(0, len(allkeys), 4):
    print("  " + "  ".join("%-22s" % k for k in allkeys[i:i + 4]))
hits = [k for k in allkeys if any(m in k.lower() for m in MORAL)]
print()
print("  %d distinct field names; moral terms among them: %s" % (
    len(allkeys), ", ".join(hits) if hits else "none"))
print()
print("""
The rule holds. `in_tally`, `held_fixed`, `optionality`,
`decision_authority`, `boundary_criterion`, `cuts_required` are positional
and directional, and none of them scores a side.

Worth recording because it is cheap to state and expensive to keep, and
because the one place a moral term could enter without tripping this check
is a VALUE rather than a key -- `position` and `claim` are free text and
carry the dispute's own language. Those are quotations of the parties, not
the instrument's vocabulary, which is the right place for them.
""".strip())

# ------------------------------------------------------------------ MD_006
head(6, "MD_006", "the weakest part is named by the drop, and it is the right one")
print("""
DISCLOSED WEAKNESSES, first item:

    Both cases are model-constructed. Neither is a documented dispute
    between real parties. A case where each side's stage-1 entries are
    filled in by that side, rather than by one party modelling both,
    would test M1 very differently -- the reductions here were produced by
    the same process that predicts them.

That is the finding an auditor would lead with, stated by the author, with
the mechanism named: the process producing the reductions is the process
predicting them.

Both case `source` fields say the same thing unprompted:
""".strip())
print()
for c in CASES:
    print("  %s:" % c["case"])
    for line in [c["source"][i:i + 62] for i in range(0, len(c["source"]), 62)]:
        print("      " + line)
print("""
`animal-standing` goes further -- "Offered, then found to reduce; recorded
with the reduction rather than discarded." A candidate counterexample that
failed, kept with its failure, which is the refutation protocol applied to
the folder's own generated evidence.

What this audit adds is only the arithmetic: n=2, both self-produced, 0
live residue, and the fixture that would show a non-empty residue is
representable is the file that did not arrive (MD_001). The claim table
says n=2 self-produced is "the weakest evidence in the repo" and does not
overstate.
""".strip())

# ------------------------------------------------------------------ MD_007
head(7, "MD_007", "the first case not built by the model, and what it reaches")
print("""
DISCLOSED WEAKNESSES, first item: "Both cases are model-constructed."
MD_006 recorded it as the finding an auditor would lead with. Drop 2
answers it.
""".strip())
print()
for c in CASES:
    origin = ("EXTERNAL" if "not constructed by the model" in c.get("source", "")
              else "model-constructed")
    print("  %-18s %s" % (c["case"], origin))
print()
print("""
mortuary-practice is from a classroom exchange, and its source field says
what makes it different: "the smuggled content sits in the question's
setup rather than in either side's position."

It also reaches something none of the others do. M1's falsifier:

    a case where both sides' stage-1 readings match on every party AND
    every held-fixed variable, and a disagreement remains
""".strip())
print()
print("  %-18s %-16s %-18s %s" % ("case", "parties match", "held_fixed match", "live residue"))
print("  " + "-" * 66)


def _sig(side):
    return sorted((o["party"], o["in_tally"], o["optionality"],
                   o["decision_authority"]) for o in side["option_claims"])


for c in CASES:
    a, b = c["sides"]
    pm = _sig(a) == _sig(b)
    hm = sorted(a.get("held_fixed", [])) == sorted(b.get("held_fixed", []))
    live = sum(1 for r in c["residue_candidates"] if not r.get("resolved"))
    print("  %-18s %-16s %-18s %d" % (c["case"], pm, hm, live))
print()
mp = next(c for c in CASES if c["case"] == "mortuary-practice")
a, b = mp["sides"]
extra = [x for x in a["held_fixed"] if x not in b["held_fixed"]]
print("  mortuary-practice held_fixed differs by exactly %d item:" % len(extra))
for x in extra:
    print("      %s: %s" % (a["id"], x))
print()
print("""
So the case gets closer to M1's falsifier than anything else in the
corpus -- first case where stage 1 matches on EVERY party -- and does not
meet it, because the falsifier also requires the held_fixed lists to
match, and they differ by one item: "which practices are available to
score against".

That one item is the disagreement. The case's own note says as much:
"the divergence is entirely at stage 2 -- what the practice is scored
against." M1 survives, and the margin is now visible and small: one
held_fixed entry between the corpus and the claim's stated falsifier.

Whether the falsifier is well-drawn is a separate question this audit
does not settle. Requiring held_fixed to match makes a stage-2 divergence
insufficient to refute a claim about stage 1 -- which is either the right
boundary or a boundary that puts the falsifier out of reach, and the two
readings are not distinguishable from three cases.
""".strip())

# ------------------------------------------------------------------ MD_008
head(8, "MD_008", "M3's three fields never vary independently")
print()
print("  %-18s %-11s %6s %-12s %s" % (
    "case", "side", "cuts", "crit_doc", "terminates"))
print("  " + "-" * 60)
_triples = []
for c in CASES:
    for side in c["sides"]:
        f = side["frame"]
        n = len(f.get("cuts_required", []))
        _triples.append((n, f.get("criterion_documented"), f.get("terminates")))
        print("  %-18s %-11s %6d %-12s %s" % (
            c["case"], side["id"], n, f.get("criterion_documented"),
            f.get("terminates")))
print()
print("  distinct (cuts, criterion_documented, terminates) triples: %d"
      % len(set(_triples)))
for t in sorted(set(_triples)):
    print("      %s" % (t,))
print("""
Across six sides in three cases the three fields are perfectly collinear:
cuts=3 always with criterion_documented=False and terminates=False,
cuts=1 always with True and True. Two triples, no independent variation.

M3's status reads the cut asymmetry as evidence. On this corpus the cut
count, the documentation flag and the termination flag are one variable
reported three ways -- so M3 has n=3 on a single distinction, not three
converging measurements.

This is `category-weld`'s own mechanism applied to the sibling folder's
schema: three quantities that could diverge, never observed diverging,
all set by the same hand in the same file. The weld test asks whether a
divergence case can be named; here the divergence is not merely unnamed,
it is unrepresented across the whole corpus.

What would separate them, and it is cheap: a side whose criterion IS
documented and which still requires many cuts (a well-specified ordering
that keeps ordering), or a side with one cut and an undocumented
criterion (a terminating frame nobody wrote down). Either breaks the
collinearity and turns M3 from one reading into two.
""".strip())


print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as MD_001..MD_008")
print(BAR)
