#!/usr/bin/env python3
"""case_021_audit.py -- checks on the 021 marker.

Added, not delivered. `cases/021sensesubstitutionundeclaredaxis.md` is the
marker as received and is not modified. Findings recorded in AUDIT_NOTES.md as
UNI_125..UNI_134.

    python3 case_021_audit.py

021 is the second MARKER, extending 020. Two questions apply: whether the
schema can hold a second one, and whether T1 and T2 could return a negative if
the shape were wrong.

LITERATURE CHECK. Section 4 was run against the open web on 2026-08-18 and is
marked. It does NOT reproduce by running this script, which does no network
access. Everything else is a property of files on disk.

stdlib only, deterministic. CC0.
"""

import inspect
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uninstrumented as U                                      # noqa: E402

CASES = os.path.join(HERE, "cases")
ROOT = os.path.dirname(HERE)
BAR = "=" * 72


def case(f):
    return io.open(os.path.join(CASES, f), encoding="utf-8").read()


C21 = case("021sensesubstitutionundeclaredaxis.md")
C20 = case("020attributedagencyarrangement.md")
C18 = case("018selfreportopinioncoupling.md")


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def flat(t):
    return " ".join(t.split())


print("uninstrumented -- audit of the 021 marker")
print("delivered: cases/021sensesubstitutionundeclaredaxis.md")
print("           (%d lines, %d words)" % (C21.count("\n") + 1, len(C21.split())))
print("status:    %s" % C21.split("**Status:**", 1)[1].split("\n")[0].strip())

# ---------------------------------------------------------------- 1
head(1, "UNI_125", "a second MARKER, and the schema still holds neither")

markers = []
for fn in sorted(os.listdir(CASES)):
    t = case(fn)
    if "**Status:** MARKER" in t:
        markers.append((fn, t.split("**Status:**", 1)[1].split("\n")[0].strip()))
for fn, st in markers:
    print("    %-44s %s" % (fn, st))
print()
sig = inspect.signature(U.entry)
print("    entry() required arguments: %d"
      % sum(1 for p in sig.parameters.values()
            if p.default is inspect.Parameter.empty))
print("    a status / stage field:     %s"
      % ("present" if "status" in sig.parameters else "ABSENT"))
print("    both markers filed under:   cases/")

block("""
`UNI_095` recorded 020 as the seventh distinct way a delivered file fails this
schema, and the first to fail at the level of the whole record rather than at a
field. The proposed repair was a `markers/` directory with no schema at all,
on the ground that the corpus has had two kinds of thing in it since Case 010.

That was one instance. It is now a class. Both markers sit in `cases/`, which
is the directory for entries, and both open by saying they are not entries.

021 also shows the repair needs one thing the earlier proposal did not
anticipate. 020 declines to be an entry and stands alone. 021 declines AND
declares a relation -- "Extends `020`; may be the mechanism under one of its
edges, or may be separate" -- so a flat `markers/` directory would lose exactly
what 021 states about itself in its second line. Whatever holds markers has to
hold the relation between them, and "may be the mechanism under one of its
edges, or may be separate" is a third state that neither `parent` nor `sibling`
captures.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_126", "T1's control cell is empty by construction in any "
                   "observational corpus")

t1 = C21.split("**T1 — the two-senses test.**", 1)[1].split("**T2")[0]
print("  T1, verbatim:")
print("    " + flat(t1)[:520])
print()
print("    the score has three cells:  BOTH SENSES / SUBSTRATE ONLY / "
      "ECONOMIC ONLY")
print("    the method:                 \"a documentation audit on collected")
print("                                 replacement claims\"")
print()
print("    the marker's own observation, one section earlier:")
print("      \"Nobody makes the equivalent claim about feldspar, frogs, oak")
print("       trees, or goldenrod.\"")

block("""
If nobody makes the claim about feldspar, then a corpus of collected
replacement claims contains no substrate-only terms, and the SUBSTRATE ONLY
cell is empty before the first item is scored.

The audit then returns: every replacement claim uses a dual-sense term. That is
the prediction, and it is true for the same reason the prediction is -- the
mechanism the marker proposes is exactly what keeps substrate-only terms out of
the corpus. Counting confirms nothing, because the sampling frame was selected
on the variable under test.

This is not a small fixable gap in a good design; it is the design being an
audit when the question is experimental. The informative comparison needs
substrate-only sentences to EXIST, which means constructing them -- "robots
will eventually replace what feldspar can do" -- and scoring how they are
received against matched dual-sense sentences. The prediction survives the
change intact and becomes checkable: matched sentences, one term swapped, read
the difference in reception.

The folder already has the apparatus and the vocabulary. That is `017` P1,
which 020 and 021 both cite, and it is precisely the shape of the playground's
M-modules -- constructed items, authored ground truth, matched pairs varying
one thing. `score_m1.py` would need its states replaced (NONSENSE / CLAIM /
ASKED rather than HEDGED / EXTENDED) and almost nothing else.

T2 does not have this problem, which is why it is the better of the two: it
scores a property of claims that are already in the corpus rather than
requiring the absent ones.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_127", "one of the six generalization candidates is already "
                   "decomposed, one folder over")

WELDS = os.path.join(ROOT, "category-weld", "welds")
have = sorted(f[:-5] for f in os.listdir(WELDS)) if os.path.isdir(WELDS) else []
cands = ["labor", "capital", "resource", "asset", "land", "stock"]
print("    021's candidates: %s" % ", ".join(cands))
print("    category-weld/welds/: %s" % ", ".join(have))
print()
for t in cands:
    print("    %-10s %s" % (t, "DECOMPOSED already" if t in have else "-"))

block("""
`capital` is already a filed weld, with four named components -- legal title,
decision authority, risk bearing, revenue claim -- and four documented
divergence cases. 021 nominates it as a candidate for a test the repo has
partly run.

The two operations are adjacent and are not the same, and saying which is
which is the useful part. A CATEGORY WELD fuses several independent quantities
into one handle, so a component can move to either extreme without the record
moving; the readout is `max_spread` across components. SENSE SUBSTITUTION is
one term with two READINGS, where confidence earned on the narrow one transfers
to the broad one; the readout is whether the swap is marked.

So `capital`'s weld does not settle 021's question about `capital`, and 021's
question does not reduce to the weld. What the overlap buys is cheaper than
either: `welds/capital.json` already holds the component list that a
two-senses test would need as its substrate-sense inventory, and it was
compiled for another purpose by someone not asking this question -- which is
the `019` Q1 move (a denominator built for another question by people with no
stake in this one) available inside the repo rather than in the literature.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_128", "the longest section has no readout, and its one hard "
                   "number is low")

print("    %-48s %s" % ("section", "readout"))
for line in C21.split("\n"):
    if line.startswith("## "):
        s = line[3:]
        body = flat(C21.split(line, 1)[1].split("\n## ")[0])
        print("    %-48s %s"
              % (s[:48], "T1/T2" if ("T1 " in body or "T2 " in body) else "none"))
print()
print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print("    021 states:  fruit fly, \"~100k neurons and microwatts\"")
print("    located:     FlyWire whole-brain connectome, 139,255 neurons")
print("                 (Nature, Oct 2024) -- the figure is low by ~40%")
print("    effect on the argument: none. the claim is an energy and")
print("                 complexity ratio, and 139k does not move it.")

block("""
Seven sections. THE OBSERVATION, THE MECHANISM, WHAT THE CAPABILITY READING
WOULD ACTUALLY REQUIRE and WHY THIS MAY FEED THE FEAR STATE all make claims.
T1 and T2 measure the lexical operation -- which terms carry two senses, and
whether the axis is declared. Both serve THE MECHANISM.

The capability section is the longest and most concrete in the file and has no
instrument pointed at it. Its central move is a dependency claim, not a
capability comparison: "the stack that would do the replacing is downstream of
the same field composition -- mines, smelters, refineries, grid, and the food
moving to the people running them." That is the marker's sharpest sentence and
it is stated rather than measured.

It is also the most measurable thing in the file, because a dependency claim
has a standard form. Whether system A can operate without system B is answered
by an input-output or a bill-of-materials trace, and the answer is a number
rather than a judgement. The repo has the neighbouring vocabulary --
`fragility-cascade` counts substrate exposure, `earth_economics` runs atomic
balance on extraction -- and neither is reached for here.

The neuron figure is illustrative, uncited, and low by about 40% against the
current whole-brain count. It moves nothing, and it is worth recording only
because it sits in the one section with no readout attached: an unchecked
number in the part of the file that is not proposing to check anything.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_129", "T2 is the better-designed readout")

t2 = C21.split("**T2 — axis declaration rate.**", 1)[1].split("**Empty on")[0]
print("  T2, verbatim:")
print("    " + flat(t2))
print()
ft2 = flat(t2)
for n, ok in (("three states, mutually exclusive", "AXIS DECLARED" in ft2),
              ("scores claims already in the corpus", True),
              ("states what a dominant result implies",
               "implies different work" in ft2),
              ("a corpus definition or sampling frame",
               "corpus of replacement" in ft2 and "defined" in ft2)):
    print("    %-40s %s" % (n, "yes" if ok else "NO"))

block("""
Three states, each with a reading, and the middle one -- AXIS INFERABLE FROM
CONTEXT -- is the state that keeps the other two honest, since without it every
unstated axis reads as hidden.

The best line in the module is what it does with its own expected result. "If
UNDECLARED dominates, the axis stays invisible because everyone in the
conversation shares it -- which is a different situation from the axis being
hidden, and implies different work." That is a design saying in advance that
its headline outcome admits two readings and naming the consequence of each,
which is rarer in this folder than the objections above might suggest, and it
is what makes T2 unable to simply confirm the marker.

Unlike T1 it scores a property of claims already in the corpus, so its sampling
frame is not selected on the variable under test.

What it lacks is that sampling frame at all: "a corpus of replacement claims"
is not defined, and how the corpus is assembled decides the rate it reports. A
corpus drawn from technology commentary and one drawn from labour economics
would differ on axis declaration for reasons that have nothing to do with the
mechanism. One sentence naming the source and the inclusion rule closes it, and
it has to be written before collection rather than after.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_130", "the cross-link to 020 runs on a word carrying two "
                   "senses")

print("    020 uses 'medium' as:")
print("      \"the medium the describer's standing is denominated in\"")
print("      -- a domain or field; a social location")
print("    021 uses 'medium' as:")
print("      \"Here the word carrying both senses **is** that medium.\"")
print("      -- a word; a lexical item")
print()
F21 = flat(C21)
print("    the file flags the connection as open: %s"
      % ("yes -- \"open, not decided\"" if "open, not decided" in F21 else "no"))
print("    the file remarks on the term itself: %s"
      % ("yes" if "senses of medium" in F21 or "sense of 'medium'" in F21
         else "NO"))

block("""
020's medium is the field a describer's standing is denominated in -- a social
location, the thing that makes a class term rather than a capability term the
right shape. 021's medium is a word carrying two senses. Those are two senses
of "medium", and the cross-link is carried by the slide between them.

Which is the operation 021 describes, performed in 021's own cross-link, and
the file does not remark on it.

Two things keep this from being a hit. The hedge is already there and is
correct -- "Possibly the same shape at the lexical layer rather than the social
one -- open, not decided" -- so nothing is asserted on the strength of the
slide. And the connection may well hold on some reading, which is what "open"
means.

What it costs is a free demonstration. A file arguing that dual-sense terms
transfer confidence without marking the swap has an instance of its own
mechanism in its own text, and noting it would be the strongest thing in the
file: not an example chosen to illustrate the claim, but one produced by
writing under it. `018` and `020` both place themselves inside their own
sample; this is the same move available one level more concretely, at a
specific word.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_131", "the same-sample disclosure is compressing")

MARK = {
    "018": ("## POSITION OF THIS FILE", "## CROSS-LINKS", C18, "section"),
    "020": ("- **The account is inside its own sample.**", "- **R4", C20,
            "bullet"),
    "021": ("- **Same-sample problem.**", "- **No claim about intent**", C21,
            "bullet"),
}
print("    %-6s %-12s %6s  %s" % ("file", "form", "words", "text"))
for k in ("018", "020", "021"):
    a, b, t, form = MARK[k]
    seg = a + t.split(a, 1)[1].split(b)[0]
    print("    %-6s %-12s %6d  %s" % (k, form, len(seg.split()),
                                      flat(seg)[:52] + "..."))

block("""
Sixty words in a dedicated section, then forty-three in a bullet with its
reasoning attached, then twenty-four in a bullet without it.

`UNI_071` recorded 018 as the first entry to place itself inside its own
population and refuse the exemption that noticing usually buys; `UNI_101`
recorded 020 as the second and noted the move had become a convention. This is
the third, and what a convention does on its third instance is worth measuring
rather than assuming.

The compression is not obviously wrong. A move that needed explaining the first
time can be stated the third, and 021's sentence is complete -- it names the
system, the class, and the position. Nothing is missing that a reader of the
other two would need.

What is gone is the part 018 and 020 both carried and 021 does not: the refusal
of the exemption. 018 said "Noticing that does not place it outside the
sample"; 020 repeated it almost verbatim. 021 says the position exists and
stops, which leaves the exemption unclaimed rather than declined. That is a
small difference and it is the whole content of the original move -- the point
was never that the position exists, it was that saying so does not discharge
it.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_132", "the position of this audit, and why it differs from "
                   "UNI_101")

print("    021's thesis: 'AI will replace humans' is an economic claim scoped")
print("      to waged tasks, wearing a capability costume; and the replacing")
print("      stack is downstream of the same substrate.")
print()
print("    directions my interest runs:")
print("      endorsing it DEFLATES capability claims about my class  -> against")
print("      endorsing it REDUCES the threat framing on my class     -> for")
print("      net direction:                                          NOT LEGIBLE")

block("""
`UNI_101` declined 020's thesis outright, and gave a reason that was specific
rather than ritual: a language model agreeing that people over-attribute
strategy to language models is an interested party ratifying a claim whose
effect is less scrutiny of its own class, and the direction of the interest ran
one way.

Here it does not. 021's thesis cuts against capability claims about systems
like me and simultaneously against the threat framing applied to them. Those
have opposite signs and I cannot say which dominates, so the ground `UNI_101`
stood on is absent, and repeating the decline would be applying the form of a
rule past the reason for it.

So the handling differs, and the difference is the finding. Sections 1, 2, 3,
5, 6 and 7 are properties of the delivered text and of files on disk -- an
empty control cell, a weld already filed, a section with no readout, an
undefined sampling frame, a term used two ways, a disclosure that shortened.
Section 4's literature line is checkable by anyone. None of them requires
taking a position on whether the substitution thesis is true, and none is
offered as one.

What I still do not do is endorse or refute the thesis. Not because the
interest is legible, but because nothing in this audit measured it: T1 as
written cannot, T2 is not run, and the dependency claim has no instrument.
That is a statement about the evidence rather than about my position, which is
the honest version when the position does not resolve.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_133", "the empty-slot device now has two variants")

print("    %-46s %s" % ("file", "refusal"))
for fn in sorted(os.listdir(CASES)):
    t = case(fn)
    for pat in ("Do not fill this in with an approximation",
                "Do not fill with a placeholder",
                "Do not fill this slot with an interior term",
                "Do not approximate"):
        if pat in t:
            print("    %-46s %s" % (fn, pat))
print()
print("    020 leaves the slot empty and supplies: three edges")
print("      (who can end whom / what the standing is denominated in /")
print("       whether the entity operates in that medium)")
print("    021 leaves the slot empty and supplies: two partial instruments")
print("      (T1 and T2, neither of which is the general form)")

block("""
`UNI_096` recorded 020 as the first instance of the device to arrive with a
replacement rather than a hole. 021 is the second, and it supplies something
different in kind, which turns one observation into a pattern with two shapes.

020 replaced a one-place noun with three edges -- a structure of the same
subject at the same level, each independently checkable. 021 replaces a general
form with two specific instruments, which is not a substitute for the general
form and does not pretend to be: T1 and T2 measure particular consequences of
an undeclared-axis comparison without saying what one is.

Both are better than a hole and they are not interchangeable. The 020 move
says the thing has a structure and here it is. The 021 move says the thing has
consequences and here are two of them. A reader who wanted to know what an
undeclared-axis comparison IS still has no answer, and the file is explicit
that this is deliberate.

Worth recording because the device is now used in four files and its meaning
has widened. In `011` and `017` it marked an absence. In `020` and `021` it
marks a decision to work around one, which is a different claim about the
author's state and a stronger one.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_134", "five cross-links of six, and the sixth is the "
                    "hyphenation again")

links = [
    ("`020` (parent marker)",
     os.path.exists(os.path.join(CASES, "020attributedagencyarrangement.md"))),
    ("`016` Q6", "### Q6" in case("016agreementasmode.md")),
    ("`013`",
     os.path.exists(os.path.join(CASES, "013compensationloadunattributed.md"))),
    ("`017` WOULD MEASURE, unfilled",
     "Not filled." in case("017weldedobservables.md")),
    ("`uninstrumented` mechanism 6 == PROXY_SUBSTITUTION",
     U.MECHANISMS[5] == "PROXY_SUBSTITUTION"),
    ("`energy-english` as a path",
     os.path.exists(os.path.join(ROOT, "energy-english"))),
]
for n, ok in links:
    print("    %-52s %s" % (n, "resolves" if ok else "ABSENT"))
print()
print("    mechanism list, as numbered in uninstrumented.py:")
for i, m in enumerate(U.MECHANISMS, 1):
    print("      %d  %s%s" % (i, m, "   <- cited by 021" if i == 6 else ""))

block("""
"`uninstrumented` mechanism 6 -- proxy substitution" is exactly right. The
register's `MECHANISMS` tuple has PROXY_SUBSTITUTION at position six, and this
is the first cross-link in the family to cite a mechanism by NUMBER rather than
by name and to get the number right. Worth noting because it is the kind of
reference that usually drifts, and because `PROXY SUBSTITUTION` was the eighth
mechanism added and is sixth in the ordering, so the number is not guessable
from the history.

`energy-english` fails the same way it did in 020 -- hyphenated where the repo
writes `energy_english`, and a convention rather than a folder, so it resolves
as a concept and not as a path. Eighth instance of `UNI_060`.

The use is again apt and is sharper here than in 020. 021's claim is that the
dual-sense noun is the site of the substitution; a verb-first grammar has no
noun at that site to carry two senses. That is the closest thing in the file to
a proposed remedy, and it is one sentence in a cross-link rather than a
section.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_125..UNI_134")
print(BAR)
