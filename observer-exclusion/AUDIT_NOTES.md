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

## Where it sits

`question-availability/` is the parent and `OE_006` is the connection that
matters. `criterion-symmetry/` is the sibling whose seed set failed the
selection discipline §5 gets right. `null-harness/` supplies §6's
argument. `sim-span/` and `conversation-type/` are the methodological
neighbours — all three find that the **measurement window or the recording
process**, not the mechanism, is what decides whether an effect is visible.

CC0. Stdlib only. Parses under Python 3.9.
