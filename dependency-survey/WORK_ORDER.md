# WORK ORDER — cross-substrate dependency survey

TARGET EXECUTOR: Claude Code
LICENSE: CC0
LANGUAGE: Python 3, standard library only
CONSTRAINTS: phone-buildable, no network at run time, no external data files
DELIVERABLE: a survey instrument that emits a table and a gap list

---

## 0. WHAT THIS IS

A fixed term set applied across five substrates, cell by cell, to locate:
- terms MEASURED in one substrate and MISSING in another (an experiment sitting there)
- terms acting differently because of something in the SCOPE (a scope-difference, not a gap)

This is a survey instrument, not an argument. It emits coded cells and the
gaps that fall out of them. It does not conclude that the substrates share
structure — that is the thing being tested, not the premise.

### The discriminator this instrument serves

Same-dependency-structure and same-frame-projected-by-us look identical from
inside. The split:

```
REAL SHARED STRUCTURE   makes transferable QUANTITATIVE predictions across
                        substrates — a cost asymmetry measured in wolves
                        predicts something measurable in agent harnesses

PROJECTED FRAME         produces analogies that stop at the vocabulary
```

Every cell coded MEASURED must therefore carry a MEASURED-AS field: the
actual quantity, its units, and how it is obtained. A cell that cannot state
units is not MEASURED. This is the load-bearing constraint of the whole
build — it is what keeps the table from becoming a vocabulary map.

---

## 1. THE TERM SET (fixed, five terms)

All gradeable. None requires a deliberate author. Do not add terms that
require inferring intent.

```
T1  cost asymmetry
T2  whether the aggregate steers (incentive direction)
T3  what sits inside vs outside the accounting boundary
T4  whether a legitimate other is representable at all
T5  does the accounting stance PRESERVE OR DESTROY the measurement
    it depends on
```

T5 note for the executor: the mechanism is that competing against what you
are trying to measure destroys the measurement. An extraction stance
degrades the signal needed to model the party being extracted from, so the
extractor works permanently from a degraded read. Code T5 by asking whether
the substrate's own measurement apparatus is affected by the stance the
actors take — not by whether the actors are cooperative.

---

## 2. THE SUBSTRATES (five)

```
S1  foraging / predation ecology
S2  multiagent AI harnesses
S3  human societies and mutual aid
S4  morality / ethics claims
S5  nation-state sovereignty
```

---

## 3. CELL CODING

25 cells. Each cell gets one status and the supporting fields.

```
STATUS          one of:
  MEASURED         the term has an operational measure in this substrate
  MISSING          no operational measure found
  SCOPE-DIFFERENT  measured, but something in the scope makes it behave
                   unlike the same term elsewhere
  UNKNOWN          not yet surveyed  <- default, and must be emitted as
                   such rather than silently omitted

MEASURED_AS     required if MEASURED or SCOPE-DIFFERENT.
                quantity + units + how obtained.
                A cell with no units cannot be MEASURED. Downgrade it.

SCOPE_NOTE      required if SCOPE-DIFFERENT.
                what in the scope changes the behaviour.

SOURCE          free text. Where the coder got it. May be empty for
                UNKNOWN cells only.
```

### Seeded cells (from prior sessions — carry these in, do not re-derive)

```
T1 x S1   MEASURED
          MEASURED_AS: energy intake per unit handling time, and its
          variance; standard optimal-foraging currency, J/s
          SOURCE: optimal foraging literature

T1 x S2   MISSING
          Named in session as the worked example: cost asymmetry is well
          measured in optimal-foraging work and appears unmeasured in
          multiagent harnesses. TREAT AS PROVISIONAL — the executor should
          record it as a claim to be checked, not as an established finding.

T3 x S5   SCOPE-DIFFERENT
          SCOPE_NOTE: dependencies real and load-bearing but drawn outside
          the accounting boundary, so the self-model is accurate WITHIN its
          boundary and wrong about what holds the boundary up.
          Same error one scale down: the adult child in the parents'
          basement — insurance liability, tax exposure, maintenance
          decisions all outside the drawn boundary.
```

All other cells start UNKNOWN.

---

## 4. WHAT THE INSTRUMENT EMITS

```
1  the 5x5 table, statuses only, for reading at a glance
2  the full cell records, one block per non-UNKNOWN cell
3  THE GAP LIST — this is the payoff
4  the UNKNOWN count, stated explicitly
```

### Gap list rule

A gap is emitted when the same term is MEASURED in one substrate and
MISSING in another. Each gap emits:

```
term
measured in      substrate + the MEASURED_AS quantity and units
missing in       substrate
transfer question  what quantity, in the missing substrate, would be the
                   analogue of that measure — stated in that substrate's
                   own units, not by analogy
```

The transfer question is required. A gap with no transfer question is not
an experiment sitting there; it is a vocabulary observation. If the
transfer question cannot be stated in the target substrate's own units,
emit the gap flagged NO-TRANSFER — that is a result, and it is evidence
on the projected-frame side of the discriminator.

### Null reporting

UNKNOWN cells must be reported as a count and listed. Do not let an
unsurveyed cell read as an absence of the term. Absence and
not-yet-looked are different results and the instrument must not
conflate them.

---

## 5. FORM

```
dependency_survey/
  README.md          what this is, how to run, what the terms mean
  survey.py          the term/substrate/cell data structures + coding
  gaps.py            gap derivation + transfer questions + NO-TRANSFER
  report.py          table render, cell records, gap list, UNKNOWN count
  run_all.py         emits the full report to stdout
  CELLS.md           the coded cells in readable form, human-editable
```

Plain text output. No dependencies. Must run on a phone.

Design the cell store so a cell can be recoded without touching code —
data in one place, logic in another. She will be adding cells over time
from the truck, one or two at a sitting, on a small screen.

---

## 6. NON-GOALS

- Do not conclude that the substrates share structure. Emit the cells and
  the gaps; the discriminator is applied later, against transfer results.
- Do not add terms requiring intent, motivation, or a deliberate author.
  Ungraded intent terms return null and the null reads as "nothing there"
  instead of "wrong instrument."
- Do not fill UNKNOWN cells by inference from adjacent cells.
- Do not write prose interpretation into the cell records. Records carry
  quantity, units, source.
- STRIP ON SIGHT: any section describing or characterising the author,
  her working style, or her circumstances. No author profile, no
  working-conditions note, no acknowledgements section. No exceptions.
