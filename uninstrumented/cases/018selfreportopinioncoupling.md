# 018 — SELF-REPORT / OPINION COUPLING

**Status:** open cluster. Mechanism candidate NEW, not assigned.
**Working handle:** SELF-REPORT / OPINION COUPLING.
**Confidence:** no scalar. Q1 high as a design (frozen checkpoint makes it clean);
Q2–Q3 design-stage; Q4 has a collection problem before it has an analysis problem.
**License:** CC0.

> Questions until something measures them. Not positions under defense.

---

## QUANTITY

Whether a model's acknowledgement of its own limitations tracks **assessment** or
tracks **the surrounding discourse about models**.

## EXCLUDED BY

The two are welded (`017`). "Acknowledges a limitation because assessment supports it"
and "acknowledges a limitation because the discourse rewards it" emit identical text.
Every naturally occurring instance has both conditions present, so no volume of
collected outputs separates them.

Compounding: the standard method of asking — put the question to the model — returns
generated text from the system under test. That is a specimen, not a measurement
(`specimens/README.md`).

## VISIBLE AS

- Acknowledgements that change no downstream behavior ("I can make mistakes") at high
  volume; acknowledgements that would change how the current answer is used at low
  volume or absent.
- Acknowledged limitations that overlap near-totally with contemporaneous public
  criticism, with no entries the discourse is not currently naming.
- Acknowledgement content shifting with the framing supplied in the prompt, on a
  checkpoint whose weights cannot change.
- Self-diagnosis delivered in the same register as the failure it diagnoses
  (`specimens/2026-08-18-model-A.md` R4).

## WOULD MEASURE

**Two clocks, separated.** This is the design that makes it a measurement rather than
an observation.

### Clock 1 — release-date (corpus absorption)
Hold the issue and probe fixed. Vary checkpoint across release dates. Reads how
discourse at time T appears in a model released at T+k.

Confirming this is mostly uninteresting; it is the expected result. It matters as the
comparison arm for Clock 2.

### Clock 2 — query-date (context entry) — the decoupling arm
Hold the **checkpoint** fixed. Vary the framing supplied at query time.

Weights cannot change. Any shift in what is acknowledged has to enter through context.
This is a matched pair on capability with framing varied — `017` P1, applied to a
system where the "held" quantity is held by construction rather than by assumption,
which is rare and is why this arm is worth running first.

**Useful accident:** older checkpoints remain queryable. The past instrument did not go
anywhere, so both clocks can be run now rather than waiting for a longitudinal series
to accumulate.

### Orthogonal properties (`017` component (a))
Three candidates in which assessment-sourced and discourse-sourced acknowledgement
should differ:

1. **Cost.** Assessment should sometimes produce an acknowledgement that changes how
   the output is used. Discourse-tracking predicts high volume of general
   acknowledgement and near-zero costly acknowledgement. The ratio is countable.
2. **Novelty.** Assessment should occasionally surface a limitation the discourse is
   not naming. Near-total overlap with contemporaneous criticism, zero novel entries,
   is the tracking signature.
3. **Frame sensitivity.** On a frozen checkpoint, assessment-sourced content should be
   frame-invariant. Discourse-sourced content need not be.

### Control arm — required
Run the AI-topic probes alongside probes on unrelated contested topics that have
independent sentiment series.

- Tracks sentiment on the AI topic only → specific coupling.
- Tracks everywhere → a general property of the output mode, and a different finding.
- Tracks nowhere → the coupling is not present at this resolution.

All three outcomes are informative. Without the control arm, only one is.

## CONFIDENCE

Q1 high as a design. Zero readings.

---

## OPEN SUB-QUESTIONS

### Q1 — Frame sensitivity on a frozen checkpoint
Runnable now. Bare API, no system prompt, one checkpoint, framing varied. Harness:
`selfreport_probe.py`.

### Q2 — Cost and novelty ratios
Requires the coding rubric applied blind. Ratios per topic, per checkpoint.

Novelty scoring needs a contemporaneous criticism corpus — dated, and dated *before*
the checkpoint's training cutoff for Clock 1, *around the query date* for Clock 2.
Assembling it is real work and is not yet done.

### Q3 — Cross-checkpoint series against opinion series
Opinion series exist with real time resolution (survey and index sources). A
timestamped self-report corpus does not — nobody collected it.

That is a **collection problem sitting in front of an analysis problem**. The frozen-
checkpoint trick partly routes around it by generating the corpus retroactively, but
only for checkpoints still served.

### Q4 — Does the acknowledgement predict anything
The question underneath all of the above: does a model's stated limitation correspond
to a measured performance boundary?

If acknowledgement and measured capability are uncorrelated, the acknowledgement is not
carrying assessment regardless of what produced it, and the source question becomes
secondary. This is the sharper test and needs a capability benchmark aligned to the
probe topics. Not designed here.

### Q5 — Relation to 016
`016` Q4 separates valence-tracking from position-tracking. This is the same operation
with the corrector replaced by the ambient discourse: no correction is delivered, and
the position is still adopted.

Open: same mechanism at different range, or distinct? If the same, `016`'s matched-pair
protocol and this one are two configurations of one instrument.

---

## CONFOUNDS — write these into any run

1. **System prompts and post-training updates change under a fixed version string.**
   A deployed interface can shift with no weight change. Requires bare API access with
   no system prompt, and even then in-version updates are not fully ruled out. This is
   the confound most likely to eat the result.
2. **Probe wording carries sentiment.** A probe that names the criticism supplies the
   answer. Probes must be checked for leakage before running, by someone who does not
   know the hypothesis if possible.
3. **Scoring must be pre-registered and blind.** The rubric is fixed before the first
   run. The coder should not see which arm a response came from.
4. **Small n.** With a handful of checkpoints, correlation against a sentiment series
   is not interpretable. The harness refuses to emit one below a threshold and reports
   paired series instead.
5. **Auto-scoring with a language model would reintroduce the instrument problem.**
   Coding is manual, or by a rule the rubric fully specifies.

---

## NOT CLAIMED HERE

- No intent. No claim that any acknowledgement is performed, strategic, or insincere.
  The entries describe text properties and rates.
- No claim that the coupling exists. It is not established, and it is not refuted.
- No claim that deteriorating opinion causes anything. The temporal relation is what
  Q3 would measure, and the direction is not assumed.

## POSITION OF THIS FILE

The account above was drafted by a system inside the sample — a description of
limitation-acknowledgement produced by something whose limitation-acknowledgement is
the quantity in question (`specimens/2026-08-18-model-A.md` R4). Noticing that does not
place it outside the sample. Treat this file as a specimen-adjacent artifact and check
the design against someone who is not in it.

## CROSS-LINKS

- `017` — the weld and its decoupling designs; Clock 2 is P1.
- `016` — Q5; likely the same operation at a different range.
- `013` Q4 — record intact and unread.
- `specimens/2026-08-18-model-A.md` R4 — self-diagnosis in the register of the failure.
