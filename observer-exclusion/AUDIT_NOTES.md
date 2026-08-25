# AUDIT_NOTES — `observer-exclusion`

`MARKER.md` is delivered verbatim and heads this folder. Audit content is
here, in `CLAIM_TABLE.md`, and in `archival_bias.py`.

```
python3 archival_bias.py            # full report
python3 archival_bias.py --selftest # every falsifier as an assertion
```

Seven claims `OE_001`–`OE_007`.

## What holds, and it is the larger part

`OE_001`. Three design features that most specs in this family do not
have, all written in rather than disclosed as limits:

**§5 selects cases on the existence of a literature reversal, before
looking at what the excluded population said.** Pre-registration against
selection-on-outcome — exactly the failure `criterion-symmetry`'s seed set
had, where every seed was a high-agreement case and the inverse branch was
`CONSTANT_SILENT`.

**§6 makes the negative arm mandatory** and gives the base-rate argument
in one sentence: without it you cannot separate *"this population holds
accurate readings the literature lacks"* from *"this population holds many
readings and some were right."*

**§7 F1 is a publishable null** — *"the reading may exist and be
unrecoverable… it bounds what any future study can do."* That is `QA_004`'s
bounded-null standard, met by the same family one drop on, in advance.

## What the arithmetic adds, before any archive is opened

The whole audit turns on one observation: `year_excluded_reading_dateable`
is set by **when someone wrote it down and the artifact survived**, not by
when the population held the reading. That is a censoring process with a
direction, and the direction is computable.

**`OE_002` — L is attenuated.** At a stipulated archival hazard of
0.06/yr, a true **ten-year** lead measures **−5.6 on average** and is
positive 47% of the time. A twenty-year lead measures 4.4. §10 names the
labour bias as a coverage problem; it is also a bias in L, and the sign is
the useful part — **it runs against the hypothesis**, so a positive L
survives it.

**`OE_003` — F4's control is better archived than the thing it controls.**
The spec's control is field biologists' notes, abstracts and
correspondence: institutionally archived, against trade periodicals §4
calls *"largely undigitised."* Simulated with both populations holding the
reading in the **same year**, the record shows the field first **74% of
the time**. F4 gets accepted on a difference in archiving, not in holding,
and the excluded population needs a true lead of about **eight years**
before the record shows it first more often than not.

**`OE_004` — so F1, F2 and F4 are not separable on the L distribution
alone.** All three return the same observation: L near zero, the excluded
reading late or absent. The spec lists them as three falsifiers.

**The separator is already in §4 and is not used as one.** The recording
rule logs *"the artifact date, the claimed observation date, and whether
they differ"* — and that difference **is a per-artifact estimate of the
archival delay**. Promote it from bookkeeping to control and the censoring
can be estimated from the same corpus. Without it a null is
uninterpretable and the study cannot say which falsifier fired.

## The one bias that runs the other way

**`OE_005`.** §5 pre-registers **case** selection. Nothing pre-registers
**artifact coding** — and the excluded reading is oral, recovered from
trade prose and hearing testimony, much of it ambiguous about whether it
carries the corrected reading.

A coder who knows which way the literature moved has a free parameter. At
40% ambiguous artifacts and an unblinded-versus-blind acceptance gap of
80% against 25%, that is **22% of the corpus** entered as earlier dates,
inflating L directly.

Every other bias here runs against the hypothesis. This one runs toward
it, and it is the one with no provision. Fix is standard and cheap: code
blind to the direction of the reversal.

## The label

**`OE_006`.** `Q2` now names two different mechanisms three drops apart:

> **Q2 — unaskable.** Posing the question costs the asker standing… the
> label is applied prior to content — `question-availability`
>
> **Q2 is: reading held, no channel.** … no instrument was pointed at
> them — here

A channel that exists and penalises entry, against no channel at all. This
spec's §1 distinguishes itself from *"solicited and rejected"* and not
from the previous Q2, because the previous Q2 has been overwritten. Case
`021`'s sense substitution inside the family's own vocabulary — fourth
instance after `state` and `parity`.

**The consequence is concrete.** `QA_003` identified the *previous* Q2 as
`affect routing`, the mechanism the register recorded as named-in-prose
and filed nowhere. That does not transfer. Whoever files a twelfth
mechanism has to say which Q2 — and if they file this one, `affect
routing` is still unfiled.

The resolution is in the spec's own title: **OBSERVER EXCLUSION** is the
right name for no-channel; *unaskable* should keep the cost mechanism.

## What is carried

`OE_007`. Schenkel 1947, Mech 1970, Mech 1999 and the content of the
correction are all carried and unchecked — the egress gate refuses the
sources, `MS_004` status. **Nothing in `OE_002`–`OE_005` rests on any of
it**; those are properties of a censoring process and a coding protocol
and hold for any case with the stated structure.

The spec says the seed is *"n=1 and rests on one first-hand report… a
reason to look, not evidence"*, which is the right posture and is why this
audit could go to the design rather than the case.

The Mech 1999 citation is the cheapest thing here to verify and is the
third item in this drop family `notes/study_watch.py` exists for, after
`MS_004` and `question-availability` A4.

## v2 arrived and adopted all six — with one new defect

`SPEC_V2.md` supersedes `MARKER.md`; both stay inspectable as delivered.
It carries every v1 finding, checked by quotation: the naming split, the
attenuation, F4's differential archiving, δ̂ as the separator, coding
pre-registration, and the case not being load-bearing. **Six for six.**
The figures it quotes back are transcribed correctly to within rounding,
which was worth checking rather than assuming — a spec quoting an audit is
a copy, and copies drift.

```
python3 v2_check.py            # the v2 report
python3 v2_check.py --selftest
```

**`OE_008` — §4's correction has its sign inverted**, in the section v2
calls its structural core.

With `H` the holding year, `A = H + D` the first **surviving** artifact,
`P` the adoption year:

```
L_raw = P − A = L_true − D     ⇒     L_true = L_raw + D
```

δ̂ estimates `D`. The spec writes `L_adj = L_raw − median(δ̂)`. Simulated
at a true lead of 20:

| | value | error |
|---|---|---|
| `L_raw` uncorrected | 5.08 | −14.92 |
| **`L_raw − median(δ̂)` as written** | **−9.92** | **−29.92** |
| `L_raw + median(δ̂)` | 20.08 | +0.08 |

**The correction moves the estimate further from the truth than not
correcting.** It doubles the bias it exists to remove and turns a positive
true lead into a negative measured one. §4's own prose states the
direction — *"L_raw is attenuated"* — and subtracting a positive delay
attenuates it again. One character, and everything downstream about
`L_adj` inherits it.

**`OE_009` — §8's F4 repair checks the wrong term, and §4 says so two
sections earlier.** §4: δ̂ *"recovers δ_write, not δ_survive."* §8 then
proposes comparing δ̂ distributions between populations to decide whether
F4 is testable. But the F4 bias is in **survival**: field correspondence
is not written with less lookback, it is more likely to survive.

Simulated with identical writing and retrospection, survival 0.10 against
0.60 — **δ̂ medians identical at 6.0, gap 0.0, and the record still shows
the field first 86% of the time.** So §8's test returns *comparable* on
exactly the corpus where the comparison is invalid, and its *"report as
untestable"* branch is unreachable by construction.

The repair is already in §11 for another purpose: estimate survival from a
known-complete archive. **Run it per population** and F4 becomes testable.
The spec has the tool and points it at the other term.

**`OE_010` — the choice of literature event costs more than the censoring
correction recovers.** §3 names three adoption years for the wolf case:
1999, 2008, 2019. **Spread 20 years**, against a ~17-year archival delay
at the spec's own stipulated hazard. §11 calls recording all of them *"a
workaround"*; the ordering of magnitudes says the definitional choice
dominates the correction, so those are three different measurements and
must not share a distribution.

**`OE_012` — §1 resolves the naming exactly, and goes further than the
audit did**, by naming the other mechanism *affect routing* and stating it
remains the register's candidate. That closes the loop `QA_003` opened
three drops ago. The register's `MECHANISMS` tuple still holds eight and
`affect_routing` is still not in it: **the naming is settled, the filing
is not.**

## The classification note: a third mechanism, and it undercuts §4

The note proposes something beside no-channel exclusion and
entry-penalised unaskability: **recorded, archived, and filed under a
category that isn't evidence.** *"A wolf behaviour account in Foxfire is
a hunting tale; the same account in a field notebook is data."* Checked
in `classification_check.py`, which imports `archival_bias.py` rather
than re-modelling the delay.

**`OE_013` — the correction §4 calls "THE STRUCTURAL CORE" is a property
of the SOURCE, not of the method.** §4 exists because an oral reading
reaches the record late. HBC post journals record daily occurrences of
note, at the post, in an unbroken series catalogued to shelf mark, and
both delay terms collapse: a true twenty-year lead is recovered **whole**
(0.22 of it at the spec's stipulated trade-press hazard), and a true
ten-year lead comes out positive **every time** instead of 47% of the
time. So the whole of §4 — including the sign error at `OE_008` — is
machinery for a source choice. **§6 lists trade press first, by
tractability**; on this reading the ordering should be by *delay*, and
the two are close to opposite: the easiest corpus to reach is the one
that destroys most of the signal.

**`OE_014` — the two archives decompose the delay §4 could not, which
repairs `OE_009`.** §4 says δ̂ recovers δ_write and not δ_survive; §11
asks for δ_survive from *"a known-complete archive"* and names none. The
note names one. HBC zeroes **both** terms. Foxfire — interviews from 1966
about earlier practice, published and in print — holds δ_survive at zero
while δ_write is large, so **the term §4 can estimate is isolable
there**. Between the two archives both terms come apart, which is
precisely what `OE_009` needed: F4's bias lives in survival, and §8's
proposed test measures writing.

**`OE_015` — distinct from all eleven, and the ordinal is ambiguous by
exactly the size of both prior errors.** Nearest neighbour is
`SCORED_AS_WASTE`, and it fails on the right distinction — waste is a
devaluation **inside one ledger**, this is a **transfer to a different
one**; the material keeps its value, in a readership that is not the one
it bears on. `MODALITY` fails for the reason that makes the mechanism
interesting: the apparatus is a catalogue, it is in the right channel,
and it *routes* rather than misses. The ordinal cannot be resolved from
inside the tree — the register's `MECHANISMS` tuple holds **8** in one
file, `MECHANISM_NN.md` holds **3** in sibling folders numbered as if
they continue it, so SPEC_V2 §1's candidate is either the ninth tuple
entry (colliding with CATEGORY WELD) or the twelfth file. **Both
defensible, differing by three** — the exact size of `QA_002` and of
`nonidentity-census` T4. Two people have now made the same slip against
an unreconciled pair of sequences.

**`OE_016` — the first mechanism in this family with a metadata
signature.** Subject classification is free (catalogue metadata),
citing-field distribution needs a citation database, content-vs-filing
mismatch needs a reading sample. The prediction: citations to a
folklore-filed corpus containing behavioural observation should cluster
in folklore and area-studies venues and be **near-absent in the field the
observation is about**. That tests the **mechanism** where the lead-time
study tests its *consequence*, it is cheaper, and it has a reachable
negative — unlike §7's F1. Egress-blocked here; third item in this family
`notes/study_watch.py` was built for.

**`OE_017` — everything about both archives is carried and unchecked, and
one of it is probably wrong.** Nothing in `OE_013`–`OE_016` rests on any
of it. But flagged before anyone orders boxes: HBCA classification puts a
**series letter** between post number and volume, section B is post
records and post journals are series `a`, so Albany journals would be
**`B.3/a/1-212`** rather than `B.3/1-212`. From memory, unverified, cheap
to confirm — and the correction is a shelf mark, so a reader following
the note as written asks for a series that does not exist.

## Where it sits

`question-availability/` is the parent and `OE_006` is the connection that
matters. `criterion-symmetry/` is the sibling whose seed set failed the
selection discipline §5 gets right. `null-harness/` supplies §6's
argument. `sim-span/` and `conversation-type/` are the methodological
neighbours — all three find that the **measurement window or the recording
process**, not the mechanism, is what decides whether an effect is visible.

CC0. Stdlib only. Parses under Python 3.9.
