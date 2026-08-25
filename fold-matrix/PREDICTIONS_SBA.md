# WO8 RUN — SBA plan set. Predictions, registered before reading.

Committed before any fetch is attempted and before any of the three
documents is opened. `git log` for this file is the timestamp.

## Files

1. SBA blank traditional business plan template
2. Rebecca's Plan — Traditional (filled example)
3. Andrew's Plan — Traditional (filled example)

All `.doc` from sba.gov.

## Registered, as delivered

**P1 — blank template:** zero quantified downward stops,
`unmeasured_span_min` uninterpretable, `enumeration_basis` UNREAD by
construction.

**P2 — filled plans:** some quantified floor exists (dollar figures), so
the downward stop resolves.

**P3 — upward triple identical across all three:** sign present,
magnitude ABSENT, unit ABSENT.

**P4 — blank template upward cells ABSENT not ASSERTED** — the document
does not reach a level where a goal could be stated.

**P3 is the finding if it holds:** filled plan purpose statements carry
no more information than the blank form.

## Not blind, recorded

Stated by the operator and recorded here: the SBA **search results** were
read, the **documents** were not. So the file set was chosen with some
knowledge of what sba.gov publishes, and nothing about the contents of
any of the three has been read by either party at registration time.

This is a stronger registration than `FM_015`'s, where the H1 source text
had already been read in-session, and weaker than a case where the file
set itself was unknown.

## What P3 would mean, and what it would not

P3 holding says the *format* of the purpose claim does not change between
a blank form and a filled one — a direction stated, no size, no unit. It
does not say the filled plans contain no information; they would contain
dollar figures at the downward stop (P2), which is a different arm of the
grid.

The claim is about the upward arm only, and P2 and P3 can both hold
without contradiction.

## Reader

`.doc` is legacy binary Word. If it is outside the current reader budget
it is declared as a capability item; if unreadable, the run is marked
NOT_RUN. **No value-only or text-heuristic substitution** — the same rule
WO6 S1 set for `.xls`, where a dependent-count ranking was refused as a
stand-in for a coupling that could not be computed (`SSS_046`).

---

# OUTCOME — one file, not three

Registered predictions are above this line, committed at `466b252`
before any fetch and before any document was opened.

## What arrived

**One file, and it is not one of the three named.**
`Sample_Business_Plan__We_Can_Do_It_Consulting_4.doc` — a fourth SBA
sample. Its author line reads **"Rebecca Champ, Owner"**, which is
evidence it may be the file the order called *Rebecca's Plan*; that is
recorded as evidence, not asserted as identity. The blank template and
Andrew's Plan did not arrive, and `sba.gov` refuses CONNECT, so neither
was read.

**n = 1.**

## The reader

Built after the file arrived, against it: OLE container → FIB → CLX
piece table → one compressed piece at fc 2048 → **7711 characters**,
exactly `ccpText`. Pinned with that file's own numbers.

## Outcomes

| | prediction | outcome |
|---|---|---|
| **P1** | blank template: zero quantified stops, span uninterpretable, basis UNREAD | **NOT ADDRESSABLE** — no blank template arrived |
| **P2** | filled plans: some quantified floor exists (dollar figures), downward stop resolves | **SPLIT.** Antecedent holds, consequent does not — see below |
| **P3** | upward triple identical across all three: sign present, magnitude ABSENT, unit ABSENT | **HOLDS on the one file**, 2 of 2 upward cells `+ / ABSENT / ABSENT` |
| **P4** | blank template upward cells ABSENT not ASSERTED | **NOT ADDRESSABLE** — no blank template |

## P2 splits, and that is the result

Dollar figures **do** exist: eight of them, `$75`–`$150`, an hourly rate
card by role. So P2's antecedent holds.

The downward stop **does not resolve**, and not because the figures are
missing. The document **stops before Funding Request and Financial
Projections** — the two sections of the SBA traditional format that carry
computed numbers. Counts in the text: `revenue` 0, `forecast` 0,
`projection` 0, `cash flow` 0, `break-even` 0, `loan` 0, `budget` 0.

Nothing in the plan derives the rates, and nothing derives anything from
them: there is no line anywhere that multiplies a rate by an hour count.
So the rate card is a **stated tariff**, and S1a's rule asks for a
quantity the organisation **computes**.

`unmeasured_span_min` is therefore `not computable`, on a filled plan
carrying eight dollar figures.

## P3 is the finding it was registered to be — with n=1

The two upward cells:

| level | goal | sign | magnitude | unit |
|---|---|---|---|---|
| +1 | *"help their companies prosper and grow"* (Mission Statement) | **+** | ABSENT | ABSENT |
| +2 | *"increase productivity and reduce overhead costs"* (Customers) | **+** | ABSENT | ABSENT |

A stated direction, no size, no unit — the same triple `FM_011` found in
the UNFCCC disclaimer. The registered reading was *"filled plan purpose
statements carry no more information than the blank form"*, and **the
blank form is exactly what did not arrive**, so the comparison it turns
on has one side. What holds is the weaker half: this filled plan's
purpose statements carry sign and nothing else.

Upload the blank template and the comparison becomes available.
