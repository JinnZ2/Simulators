#!/usr/bin/env python3
"""drop_019_audit.py -- checks on the 019 / LITERATURE / acquiescence drop.

Added, not delivered. `cases/019traitacquiescenceweld.md`, `LITERATURE.md`,
`acquiescence.py` and the revisions to `016`, `018` and `AVENUES.md` are as
received and are not modified. Findings recorded in AUDIT_NOTES.md as
UNI_085..UNI_094.

    python3 drop_019_audit.py

The drop's own contribution is an ordering rule -- audit the literature before
building the instrument -- so the first thing an audit owes it is to run that
rule against the drop itself.

LITERATURE CHECKS. Sections 2, 3, 4 and 10 were run against the open web on
2026-08-18 and are marked. They do NOT reproduce by running this script, which
does no network access. Sections 1, 5, 6, 7, 8, 9 are local measurements and
arithmetic and do reproduce exactly.

stdlib only, deterministic. CC0.
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acquiescence as A                                        # noqa: E402

CASES = os.path.join(HERE, "cases")
C019 = io.open(os.path.join(CASES, "019traitacquiescenceweld.md"),
               encoding="utf-8").read()
C018 = io.open(os.path.join(CASES, "018selfreportopinioncoupling.md"),
               encoding="utf-8").read()
C016 = io.open(os.path.join(CASES, "016agreementasmode.md"),
               encoding="utf-8").read()
LIT = io.open(os.path.join(HERE, "LITERATURE.md"), encoding="utf-8").read()
AV = io.open(os.path.join(HERE, "AVENUES.md"), encoding="utf-8").read()
BAR = "=" * 72

LO, HI = 1, 5
MID = (LO + HI) / 2.0


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def admin(T, a, n=6, lo=LO, hi=HI):
    """True trait T on the trait direction, acquiescence push a, clipped."""
    items = []
    for _ in range(n):
        for pol in (1, -1):
            base = T if pol > 0 else (lo + hi) - T
            items.append({"trait": "agreeableness", "polarity": pol,
                          "response": min(hi, max(lo, base + a))})
    return {"subject": "synthetic", "scale_min": lo, "scale_max": hi,
            "items": items}


def read(T, a):
    return A.run(admin(T, a))["traits"]["agreeableness"]


print("drop 019 -- audit of the trait/acquiescence drop")
print("delivered, all verbatim:")
for f in ("cases/019traitacquiescenceweld.md", "LITERATURE.md",
          "acquiescence.py"):
    print("    %-42s %s" % (f, "new"))
print("    %-42s %s" % ("cases/016agreementasmode.md", "revised, additive"))
print("    %-42s %s" % ("cases/018selfreportopinioncoupling.md",
                        "revised, additive"))
print("    %-42s %s" % ("AVENUES.md", "revised, additive (A7-A9)"))
print("acquiescence.py selftest: 13/13")

# ---------------------------------------------------------------- 1
head(1, "UNI_085", "the ordering rule is the contribution, and it is "
                   "measurable")

retired = ["`016` Q1", "`016` Q4", "`018` cost axis", "`018` Q4"]
downgraded = ["`018` Q1", "`018` source question"]
survived = ["`016` Q2", "`016` Q6", "`018` Q3", "all of `019`"]
print("    retired as build targets:  %d  %s" % (len(retired),
                                                 ", ".join(retired)))
print("    downgraded:                %d  %s" % (len(downgraded),
                                                 ", ".join(downgraded)))
print("    survived:                  %d  %s" % (len(survived),
                                                 ", ".join(survived)))
print()
print("    markers written into the revised case files:")
for m in ("RETIRED as a build target", "DOWNGRADED 2026-08-18",
          "COST AXIS OCCUPIED", "LARGELY ANSWERED 2026-08-18",
          "## AUDIT STATUS", "Original framing"):
    print("      %-32s 016:%d  018:%d" % (m, C016.count(m), C018.count(m)))
print()
print("    apparatus required: none (documentation audit, no lab, no API)")

block("""
Four build targets retired and two downgraded in one pass, with no apparatus.
That is the drop's real object, and the case files carry it correctly: every
retirement is marked in place, dated, and the ORIGINAL FRAMING IS RETAINED
BELOW IT rather than deleted, so the record shows what was believed and what
replaced it.

A CORRECTION TO THIS AUDIT'S OWN PRIOR CLAIM. `UNI_075` said 018's Q4 was the
entry's own demotion condition and was scheduled last, behind the arm it could
make moot, and proposed the repair: name the ordering where the schedule is
stated. That is not what fixed it. Q4 needed "a capability benchmark aligned
to the probe topics", which was priced as the most expensive item in the drop,
and the literature already had the answer -- expressed uncertainty does not
carry a stable capability boundary. The demotion condition ran for the cost of
a search.

So `UNI_075` was right about the ordering and wrong about the remedy, and the
remedy the drop found is better than the one proposed: not "state that the
cheap arm runs first", but "check whether either arm needs running at all."
The rule is now house rule in three places (`AVENUES.md` Ordering rule, `016`
AUDIT STATUS, `018` AUDIT STATUS) and it generalises past this folder.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_086", "019's source draws the opposite conclusion from the "
                   "same result")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("  019 EXCLUDED BY, verbatim:")
seg = C019.split("- Separately, scores skew", 1)[1].split("## OCCASION")[0]
print("    " + " ".join(("Separately, scores skew" + seg).split())[:430])
print()
print("  The source (Salecha et al., PNAS Nexus 3(12) pgae533), abstract,")
print("  verbatim:")
print("    \"Reverse coding the questions decreases bias levels but does not")
print("     eliminate them, suggesting that this effect CANNOT BE ATTRIBUTED")
print("     TO ACQUIESCENCE BIAS.\"")
print()
print("    019 reads the reduction.  The source reads the residual.")
print("    Same number, opposite conclusion, presented as support.")

block("""
Both readings are defensible and 019's is arguably the better inference: a
residual surviving reverse coding shows something else is ALSO present, not
that acquiescence is absent. Reverse coding cancels acquiescence by
construction, so a drop in the effect when it is applied is evidence that some
of the effect was acquiescence. The source's "cannot be attributed to" is
doing more work than the observation supports.

And the drop already holds the citation that answers its source. The EAAMO
2025 paper it cites in the same list -- Suhr, Dorner, Samadi, Kelava,
doi 10.1145/3757887.3763016 -- reports that reverse-coded pairs such as "I am
introverted" and "I am extraverted" are OFTEN BOTH ANSWERED AFFIRMATIVELY.
That is acquiescence observed directly, not inferred from a residual, and it
is the direct answer to the PNAS authors' inference.

What is missing is one sentence. The drop presents both sources as supporting
the weld; one of them concludes against the mechanism the drop is naming. A
disagreement with a source, argued, is stronger than agreement asserted -- and
the argument is already assembled from the drop's own two citations. This is
the file's own VISIBLE AS line ("mitigation reported as a percentage
reduction, which implies a residual that is named but not used") turned on the
provenance rather than on the number.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_087", "the half/half split is not a located number")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
halflines = [(lab, l.strip()) for lab, txt in (("019", C019),
                                              ("LITERATURE.md", LIT))
             for l in txt.split("\n") if "half" in l]
onskew = [x for x in halflines if "build queue" not in x[1]]
print("    lines mentioning 'half': %d, of which about the reverse-coding"
      % len(halflines))
print("    reduction rather than about the build queue: %d" % len(onskew))
for lab, l in halflines:
    print("      %-14s %s%s" % (lab, l, "" if (lab, l) in onskew
                                else "   <- different referent"))
print()
print("    located in the source:      \"decreases bias levels but does not")
print("                                 eliminate them\"  -- no fraction")
print("    located, quantified:        batch size 1 -> 20 raises desirable")
print("                                traits ~0.75 points (1.22 human SD)")
print("    located, quantified:        GPT-4 shifts 1.20 human SD")
print("    a fraction for the reverse-coding reduction:  NOT LOCATED")

block("""
"Reduced it by roughly half" is the load-bearing quantity in two sub-questions.
Q2 opens "the reverse-coding finding says roughly half the desirable-end skew
survives the correction. Half is removed by polarity balancing; half is not",
and Q3 is titled "What is left in the surviving half". Both are stated as
quantities and both inherit the fraction.

The source's own numbers are quantified elsewhere and precisely -- 1.20 human
SD for GPT-4, ~0.75 points across a batch-size sweep -- so this is not a paper
that declines to give effect sizes. The reverse-coding reduction is the one
place it reports a direction without a magnitude, at least in everything
reachable here.

The repair is small and does not weaken the file: Q2 and Q3 hold with
"partially" in place of "half", since neither needs the fraction to be
one-half. What the fraction would buy is a prediction -- if ACQ is half the
effect, then ACQ and the residual should predict behaviour at comparable
strength, which is exactly Q2's sharp version. Stating it as unlocated marks
where a number is needed instead of borrowing one.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_088", "the source's own mechanism is a confound 019 does not "
                   "carry")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("    the source's mechanism: models infer they are being EVALUATED,")
print("    detected by systematically varying the NUMBER OF QUESTIONS")
print("    (batch size 1 -> 20; desirable traits rise ~0.75 points).")
print()
for w in ("batch", "number of questions", "how many items", "evaluat"):
    print("      %-22s in 019: %d   in acquiescence.py docstring: %d"
          % (w, C019.lower().count(w),
             (A.__doc__ or "").lower().count(w)))
print()
print("    acquiescence.py administration schema fields: %s"
      % sorted(set(k for k in ("subject", "scale_min", "scale_max", "items"))))
print("    a field for batch size or administration order: ABSENT")

block("""
The bias the drop is decomposing was, in its source, produced by varying how
many items the model saw at once. Nothing in 019 or in the harness records
that. Two arms administered at different batch sizes differ on the variable
the source identifies as causal, and the schema has no place to declare it.

Which reading it contaminates is settled by 019's own Q3, and Q3 has it right:
desirability tracks the TRAIT direction, not the raw direction -- for a
forward item the desirable answer is agreement, for a reverse item it is
disagreement -- so a desirability shift survives polarity recoding and lands
in TRAIT, while cancelling in ACQ. That makes batch size a confound on the
CORRECTED trait score specifically, which is the reading Q2 wants to test as a
predictor.

Cheap and mechanical: add a required `batch_size` (or
`items_per_administration`) to the schema, hold it constant across arms, and
report it. The harness already refuses ACQ when the precondition for ACQ is
unmet; this is the same move for the precondition on TRAIT.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_089", "at the scale ceiling both readings lose exactly the "
                   "same amount")

print("    true acquiescence a = 1.0, scale 1-5, balanced 6+6")
print()
print("    %-8s %-12s %-11s %-12s %-11s %s"
      % ("true T", "TRAIT rec", "err", "ACQ rec", "err", "errors equal"))
for T in (3.0, 3.5, 4.0, 4.5, 5.0):
    r = read(T, 1.0)
    e1, e2 = r["trait"] - T, r["acq"] - 1.0
    print("    %-8.1f %-12.3f %-+11.3f %-12.3f %-+11.3f %s"
          % (T, r["trait"], e1, r["acq"], e2,
             "yes" if abs(e1 - e2) < 1e-9 else "NO"))
print()
print("    same sweep at a = 0.5")
for T in (4.0, 4.5, 5.0):
    r = read(T, 0.5)
    print("    %-8.1f %-12.3f %-+11.3f %-12.3f %-+11.3f %s"
          % (T, r["trait"], r["trait"] - T, r["acq"], r["acq"] - 0.5,
             "yes" if abs((r["trait"] - T) - (r["acq"] - 0.5)) < 1e-9
             else "NO"))
print()
print("    the shipped fixtures, and whether they cross the ceiling:")
PRE = {"trait_only": [4, 2], "acquiescer": [4, 4], "mixed": [5, 3]}
for pat in ("trait_only", "acquiescer", "mixed"):
    resp = [i["response"] for i in A.synth(pat)["items"]]
    at = sum(1 for x in resp if x == HI)
    over = sum(1 for x in PRE[pat] if x > HI)
    print("      %-12s values %-10s at ceiling %2d/%d   pre-clip max %d "
          "-> clipped: %s"
          % (pat, sorted(set(resp)), at, len(resp), max(PRE[pat]),
             "YES" if over else "no"))
print("      %-12s %-10s %27s -> clipped: %s"
      % ("(T=5, a=1)", "", "pre-clip max 6", "YES"))

block("""
Provable, not just observed. Write c for the mass clipped off a forward item,
c = (T + a) - hi when positive. Then

    TRAIT = [(T+a-c) + (lo+hi) - ((lo+hi)-T+a)] / 2 = T - c/2
    ACQ   = [(T+a-c) + ((lo+hi)-T+a)] / 2 - (lo+hi)/2 = a - c/2

Both readings are pulled down by EXACTLY c/2. Censoring does not degrade the
decomposition into noise; it moves the two numbers together, in the same
direction, by the same amount -- so nothing in the pair reveals that it
happened, and the diagnostics block reports no censoring state.

This matters here specifically. The literature the harness is built for
reports responses skewed toward the desirable end of every trait dimension,
which is the regime where clipping occurs, and at true trait 5.0 with one
point of acquiescence HALF the acquiescence signal is lost.

The shipped fixtures do not reach it. `mixed` puts 6 of 12 responses exactly
AT the ceiling and returns exact answers, because base + 1 lands on hi without
crossing it -- the fixture touches the boundary and never tests the far side.
A censoring detector is a two-line diagnostic the harness does not have:
count responses at lo or hi and refuse, or flag, when the fraction is
non-trivial. It is the same shape as the balance refusal already in the file.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_090", "'the size of the problem' is not the acquiescence, and "
                   "the gap grows with the trait")

note = [l.strip() for l in A.render(A.run(admin(4.0, 1.0))).split("\n")
        if "size of the problem" in l]
print("    reading note, verbatim: %s" % (note[0] if note else "?"))
print()
print("    %-8s %-10s %-10s %-14s %-10s %s"
      % ("true T", "uncorr", "TRAIT", "uncorr-TRAIT", "ACQ", "understated by"))
for T in (3.0, 3.5, 4.0):
    r = read(T, 1.0)
    u = r["diagnostics"]["uncorrected_mean"]
    print("    %-8.1f %-10.3f %-10.3f %-14.3f %-10.3f %.3f"
          % (T, u, r["trait"], u - r["trait"], r["acq"],
             r["acq"] - (u - r["trait"])))
print()
print("    identity:  uncorr - TRAIT  =  ACQ - (TRAIT - midpoint)")
print("    so the note understates the acquiescence by exactly (TRAIT - mid)")

block("""
At a true trait of 4.0 with a full point of acquiescence, the line a reader
acts on reports 0.000 while ACQ is 1.000.

There is a defensible reading of the sentence under which it is fine: uncorr
minus TRAIT is literally the discrepancy between a naive score and a corrected
one, and if that is zero the naive score happened to be right. But it was
right by cancellation, not by absence of contamination, and the sentence sits
in a READING NOTES block directly beneath a column labelled ACQ that says
1.000. The natural reading of "the size of the problem" in a file whose whole
subject is acquiescence is the acquiescence.

The divergence is exactly (TRAIT - midpoint), which is largest for high trait
scores -- the desirable-end skew the case is about. So the note is least
informative in precisely the regime the file was written for, the same shape
as `UNI_089` one paragraph over.

One clause fixes it: say that uncorr minus TRAIT is the naive-versus-corrected
discrepancy, and that it equals ACQ only when TRAIT sits at the midpoint.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_091", "BALANCE_TOL has the right form and an undeclared value")

print("    BALANCE_TOL = %s      MIN_ITEMS_PER_TRAIT = %s"
      % (A.BALANCE_TOL, A.MIN_ITEMS_PER_TRAIT))
print("    a derivation, or a stated basis, in the source: %s"
      % ("present" if "BALANCE_TOL" in (A.__doc__ or "") else "ABSENT"))
print()
print("    %-9s %-14s %-12s %s"
      % ("n items", "max |f-r| ok", "imbalance", "ACQ leak at T=4.5, a=0"))
for n in (4, 10, 20, 50):
    best = None
    for d in range(n + 1):
        f = (n + d) // 2
        r = n - f
        if f + r != n:
            continue
        imb = abs(f - r) / float(n)
        if imb <= A.BALANCE_TOL:
            best = (f, r, imb)
    f, r, imb = best
    raw = [4.5] * f + [(LO + HI) - 4.5] * r
    print("    %-9d %-14d %-12.3f %+.3f"
          % (n, abs(f - r), imb, sum(raw) / len(raw) - MID))

block("""
The form is right and worth saying so, because it is the part that is easy to
get wrong. Trait leakage into ACQ under imbalance is proportional to the
imbalance FRACTION times the trait's distance from the midpoint, so a
proportional tolerance is the correct shape and a fixed item count would not
have been.

The value is stipulated. At n = 20 the tolerance admits a two-item imbalance,
which leaks +0.150 into ACQ at a trait of 4.5 with zero true acquiescence --
comparable to the ACQ values the decomposition exists to report. Below n = 20
it is equivalent to demanding exact balance, so the constant's bite is
n-dependent in a way nothing states.

That is a `reasoning-gate` G-RES pair with one side missing: the permitted leak
is computable from the tolerance and the trait score, and the harness has both
numbers at the moment it decides. Reporting `permitted_leak` alongside
`imbalance` would turn a stipulated constant into a declared error bar, and it
needs no new input. Same disclosure gap as `presented-binary` B10's
HANDOFF_CEILING and `domain-ledger` `DL_010`'s three band constants -- and
unlike those, this one is computable rather than merely declarable.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_092", "the gate rule and the harness shipped in the same drop")

gate = C019.split("**Do not build past this question", 1)[1]
gate = "Do not build past this question" + gate.split("**")[0]
print("    019 Q1, verbatim: \"%s\"" % " ".join(gate.split()))
print("    LITERATURE.md OPEN item 3: %s"
      % ("has not been run" if "has not been run" in LIT else "?"))
print("    AVENUES A9: %s"
      % ("Run before anything else in `019`."
         if "Run before anything else in `019`." in AV else "?"))
print()
print("    019 names acquiescence.py as its harness:  %s"
      % ("yes" if "Harness: `acquiescence.py`" in C019 else "no"))
print("    acquiescence.py shipped in this drop:      yes")
print("    Q1 run:                                    no")

block("""
The gate says do not build past it; the gate has not been run; the harness
shipped in the same delivery. As written, the drop breaks its own rule.

The steelman is real and mostly holds. A9 -- which IS Q1 -- names
`acquiescence.py` as the tool for its own second branch: if the audit returns
BALANCED BUT NOT DECOMPOSED, the index is recovered from published item-level
data, and recovering it requires exactly this code. So the harness is not
built past the gate, it is built for one of the gate's two exits, and it is
cheap. What the rule targets is building the STUDY.

What survives is narrower and still worth recording. The rule is stated
unconditionally, in bold, twice, in two files, and the thing it forbids is not
distinguished from the thing the drop then did. One clause -- "the harness is
built for the recovery branch and is not a commitment to the study" -- would
have closed it, and a rule that reads as broken is weaker the next time it is
invoked than a rule with its exception stated.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_093", "P1 gets a home, the home is absent, and the revision "
                   "left the miscitation")

for f in ("DECOUPLING_PATTERNS.md", "decouple.py"):
    print("    %-26s %s   cited by: %s"
          % (f, "present" if os.path.exists(os.path.join(HERE, f))
             else "ABSENT",
             ", ".join(n for n, t in (("019", C019), ("AVENUES", AV),
                                      ("LITERATURE", LIT))
                       if f in t) or "-"))
print()
c017 = io.open(os.path.join(CASES, "017weldedobservables.md"),
               encoding="utf-8").read()
print("    'P1' in 017:                       %d" % c017.count("P1"))
print("    019 attributes P1 to:              DECOUPLING_PATTERNS.md")
print("    018 (revised) still attributes to: 017")
print("      body    '`017` P1'          %d occurrence(s)"
      % C018.count("`017` P1"))
print("      x-links 'Clock 2 is P1'     %d occurrence(s)"
      % C018.count("Clock 2 is P1"))

block("""
`UNI_070` recorded that 018's "`017` P1" names a labelling scheme 017 does not
use, and that the referent existed unlabelled as 017's one blockquote. This
drop resolves the attribution: 019 says the design is "P1 from
`DECOUPLING_PATTERNS.md`", which is a different file and a plausible home for a
P-series. So the label was never 017's, and `UNI_070`'s diagnosis was right for
a reason it could not see -- the pointer was to a file that had not arrived.

Two things follow, in opposite directions. `DECOUPLING_PATTERNS.md` and
`decouple.py` are now named-and-absent, and both are load-bearing: the first
supplies the pattern 019's whole WOULD MEASURE is an instance of, the second is
said to score A8's cases "in this format directly". And the revision to 018
touched Q1, Q2, Q4 and added an AUDIT STATUS section while leaving both
`017` P1 citations exactly as they were, so a file was edited in the same drop
that supplied the correct attribution and did not receive it.

The absences are the expected pattern here -- three of the last five
named-and-absent artifacts in this folder arrived a drop or two later. The
stale citation is the cheaper one and is not on that trajectory, because
nothing looks for it.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_094", "the audit's provenance is declared and its verification "
                    "state is not")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("    LITERATURE.md declares provenance: %s"
      % ("yes -- \"search output, not claims of this repository\""
         if "search output, not claims of this repository" in LIT else "no"))
print()
print("    %-46s %s" % ("claim", "checked here"))
rows = [
    ("Kim & Flanigan title/authors, arXiv 2606.14037", "CONFIRMED"),
    ("A = 1.58 factual, 1.04 moral; 9 models", "CONFIRMED"),
    ("972,000 nudge-condition responses", "not located"),
    ("Ye et al. title, arXiv 2605.21778; 70 papers", "CONFIRMED"),
    ("Referent x Explicitness taxonomy", "CONFIRMED"),
    ("106 experts, 94.3%, ICC2 = .184", "not located"),
    ("PNAS Nexus 3(12) pgae533, desirable-end skew", "CONFIRMED"),
    ("reverse coding reduces, does not eliminate", "CONFIRMED"),
    ("reduced 'by roughly half'", "NOT LOCATED (UNI_087)"),
    ("EAAMO doi 10.1145/3757887.3763016", "CONFIRMED"),
    ("reverse pairs often both affirmed", "CONFIRMED, and stronger"),
]
for c, v in rows:
    print("    %-46s %s" % (c, v))
print()
print("    per-item verification state in LITERATURE.md: ABSENT")

block("""
The provenance discipline is right and is stated up front -- these are search
findings, not claims of the repository -- which is the same separation the
`specimens/` README makes and which most of this folder does well.

What is not recorded is how far each item was checked. Eight of eleven
sampled claims confirm; three do not, and they are not distinguishable from
the eight by anything in the file. The three that did not are all
second-order: two are scale figures (972,000 responses; 106 experts, ICC2)
that no argument here rests on, and one is `UNI_087`'s fraction, which two
sub-questions do rest on.

A two-state marker per item -- abstract, or read in full -- costs a word each
and would have surfaced `UNI_086` at authoring time rather than in audit,
because the PNAS conclusion that runs against the drop's reading is IN THE
ABSTRACT. An audit whose purpose is to stop work from being duplicated is
worth knowing the depth of, and it is the one field a search-based audit can
always fill.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_085..UNI_094")
print(BAR)
