# RESULTS — criterion-symmetry scan, 2026-08-24

`python3 scan.py`. Built to `SCAN_SPEC`. Criterion is data, not code —
swap `criterion` in `cases.json` and re-run. Full output pinned in
`samples/scan.sample.txt`.

---

## THE RESULT

**The fired set is empty. So is the inverse set. Six of six human seed
cases return `UNDETERMINED`.**

| | count | cases |
|---|---|---|
| FIRED (C=defect, actual≠defect) | **0** | — |
| INVERSE (C≠defect, actual=defect) | **0** | — |
| agree | 1 | A1 |
| **UNDETERMINED** (C cannot read the case) | **7** | H1–H6, P1 |

**The scan does not show the asymmetry. It shows that the criterion has
not been applied to the human cases at all** — which is the marker's own
standard, stated in its CONFIDENCE section: *"needs the comparison table
populated before the asymmetry is a measurement rather than an
impression."*

The table is now built. It is not populated, and the scan says where.

## WHY, AND EITHER REASON ALONE IS SUFFICIENT

**1. No human case carries a numeric agreement value.** The spec states
them as *"near-universal"*, *"~200 units"*, or nothing. `agreement_value`
is `null` on 6 of 6. The criterion reads a rate; there is no rate to read.

**2. The quantity types differ.** C reads a
`within_body_agreement_rate` — the fraction of a deliberating body that
agreed. Every human case is a `cross_body_adoption_fraction` — the
fraction of independent bodies that converged on one form.

Those are properties of different objects. A vote rate says whether one
body dissented; an adoption fraction says whether a population of bodies
diversified. `reasoning-gate`'s **G-DIM** voids a ratio between them,
which is why `combined_statistic()` raises rather than returns — the
spec's own limits section says not to compute one, and it is enforced in
code rather than described in prose.

## THIS REFUTES THE MARKER'S STRONGEST PHRASING

`MARKER.md` says:

> Two dispositions, one measurement, selected by which side is the subject
> of evaluation.

**It is not one measurement.** The scan's own type column shows two, and
`SCAN_SPEC`'s limits section says so independently: *"a vote rate and an
adoption fraction are different quantities."* The spec contradicts the
marker's phrasing, and the spec is right.

The weaker statement survives and is the one to carry: **one criterion
form, applied to one subject class and not to another.** G-DIM voids the
ratio and leaves the comparison legal — you can ask whether a criterion is
applied here and not there without computing 0.98 against "near-universal".

That distinction is `reasoning-gate`'s own, and it is the difference
between a claim this scan could eventually test and one it never could.

## WHAT WOULD POPULATE THE TABLE

Per case, the number C actually reads. For the human cases that means
either:

- **a within-body agreement rate** for the deliberating bodies those forms
  contain — unanimous-consent and voice-vote proportions in legislatures,
  board and shareholder vote margins, appellate panel unanimity rates,
  standards-body consensus procedures. These are recorded and retrievable,
  and they are the quantity C reads; or
- **a second criterion** that reads adoption fractions, stated separately,
  with its own threshold and its own justification. The extension slot in
  `SCAN_SPEC` is built for exactly this, and swapping C is a data edit.

The first is the honest route, because it compares like with like. The
second changes what is being claimed.

**No figures are supplied here.** See LIMITS.

## THE INVERSE BRANCH IS `CONSTANT_SILENT`

The spec asks for it — *"report also the inverse"* — and **no seed case
can reach it.** All seven are high-agreement or high-uniformity cases, so
one branch of the scoring rule cannot fire on the delivered set.

A case set in which only one branch can fire cannot separate *the
criterion is applied asymmetrically* from *the set was selected on the
variable under test.* That is the spec's own admitted limit (*"case
selection is not a sample"*) arriving as a countable property rather than
a caveat.

`P1` is the **shape** of an inverse case — a legislature scored a defect
for gridlock — landed with every value unstated rather than invented. It
is marked `PROPOSED`, is not evidence, and is not scored.

**It matters because of what it would show if populated.** If low
agreement in a legislature is scored a defect *and* high agreement would
also be scored a defect, the criterion is not applied asymmetrically **by
subject class** — it returns defect at both ends for one class. That is a
different failure, arguably a worse one, and it is not the marker's claim.
Populating `P1` is the cheapest thing that could refute the asymmetry
reading while leaving the criterion just as damaged.

## THE FALSIFIERS

**Falsifier 1** — *C returns the same disposition as actual across all
human cases* — **cannot fire.** Not because C disagrees, but because 6 of
6 return `UNDETERMINED`. A falsifier that cannot be reached is not a
falsifier yet.

**Falsifier 2** — *any human case with `comparison_run == yes` and a
result favouring the dominant form exits the set legitimately* — fires on
**no case**. H4 is the only human case whose comparison was run, and per
the spec the result does not favour the dominant form, so it stays. This
falsifier is correctly reachable, and it did not fire.

Worth stating plainly: **A1 is the only case in the set whose comparison
was run with a result.** The one case scored a defect is the one with an
empirical comparison behind it; the six scored as governance have none.
That is a fact about the table as delivered, not a conclusion.

## LIMITS

Four are the spec's own, stated as required. Three are added.

**Not commensurable.** A vote rate and an adoption fraction are different
quantities. No combined statistic is computed and the function that would
do it raises.

**Case selection is not a sample.** Six seeds chosen because they are
familiar. The scan shows whether the asymmetry *exists*, not how common it
is — and on this run it does not show that it exists either, because the
criterion was not applicable.

**`retention_basis` is a literature claim and needs a source.**
`source` is `null` on **7 of 7** cases asserting one. The mechanism the
whole argument runs on carries zero sourced entries.

**"Control exists in the world" is not "control was available to the
adopters at the time."** Kept as separate fields; not collapsed.

**Added: the threshold was not in the spec.** C says *"high agreement"*
and names no value. Set to 0.90 here so the rule is mechanical rather than
hand-applied, and marked `threshold_source: UNSTATED IN SPEC`. Any value
in [0.5, 0.98] leaves every conclusion above unchanged, because no human
case carries a number to compare against it. Without an explicit threshold
the scoring rule is a hand assignment wearing an arithmetic coat, and the
divergence set would fire by construction.

**Added: `criterion_disposition` is computed, never given.** No case
carries that field, and `--selftest` fails if one appears. This is the
decision the whole scan turns on: hand-assigning `defect` to the human
cases would produce the marker's conclusion from the marker's assumption.

**Added: the author is inside the sample.** This scan is written by a
Claude instance and `A1` is a criterion applied to a Claude run. The scan
computes and does not conclude, and this folder does not score the
asymmetry — see `AUDIT_NOTES.md`. **No agreement figures for human
institutions are supplied from memory here**, because supplying favourable
numbers is precisely the move an interested party should not make. Where
such rates are recorded is named above; the retrieval is not done here.

## STATUS

The instrument is built and runs. The table is empty of the quantity it
needs. On the marker's own standard the asymmetry remains **an impression,
not a measurement** — and this run does not move it in either direction.

Nothing here says the published disposition on A1 was right or wrong.
