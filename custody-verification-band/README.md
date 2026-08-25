# custody-verification-band

STATUS: marker under exploration. Not a thesis, not a position under defense.
Shape read from current position. Confidence gradient stated per case in
`cases.json`, separately from the pattern itself.

Correct response to this repo: test fit, extend it, or report where it breaks.

LICENSE: CC0. stdlib only. No deps.

```
python3 extract.py table                 # the discriminator table
python3 extract.py cases --custody self  # CURRENT state
python3 extract.py cases --was self      # state before transition
python3 extract.py queue --status untouched
python3 extract.py strip                 # the strip protocol
python3 extract.py check                 # integrity, cut independence
python3 branching.py                     # the physics anchors, recomputed
python3 extract.py --selftest            # 19/19
python3 branching.py --selftest          # 13/13
```

---

## CRITERION (one line)

    A layer buffers a system iff its productive function is self-custodied
    AND locally verifiable; otherwise it is a transmission belt.

## CUTS

    custody      : who holds the residual on a good year
    verification : can the contributor inspect the node they commit to
    parallel path : does function survive removal of any single node
    slack        : uncommitted hours attached to local knowledge
    horizon      : is the long return externally ratcheted or willed

**Three of these five are recorded per case.** `cases.json` carries custody,
verification_scope and parallel_path. Slack and horizon are not case fields —
they are open measurables, at `gaps.md` G-SLACK and G-HORIZON. That is a
coherent split, not an inconsistency: two of the five cuts have no case-level
coding yet and are queued as measurements rather than guessed at.

**The criterion reads two of the three recorded cuts, and on the current
corpus that omission costs nothing.** Across all eleven cases the two-cut
criterion and the three-cut reading agree everywhere — zero disagreements.
An earlier version of this folder reported a disagreement in both directions;
that was computed over six invented SEED cases and did not survive their
replacement by the real eleven. Withdrawn, and recorded in `AUDIT_NOTES.md`.

**The reason it costs nothing is the finding.** `parallel_path` is a
deterministic function of `custody` across all eleven cases —
`routed→no, mixed→partial, self→yes` — so it carries no information custody
does not already carry. Whether that is a real regularity or the same
judgement entered twice under two names is `gaps.md` G-COLLINEAR, and
`extract.py check` reports it on every run.

## ENTRY POINT (not a claim being defended)

Origin: external claim that the middle class is an accident of history.
Not adopted. Reframed as: "middle band" is a label over a structural
feature that recurs wherever surplus + division of labor exist.
Label is discardable. Structure is what is being measured.

## PHYSICS ANCHORS (numbers, not analogy)

Recomputed in `branching.py` rather than quoted. Two labels in the delivered
anchor block named the wrong quantity; the corrected forms are below and the
correction is recorded in `AUDIT_NOTES.md`.

    WBE branching        : radius ratio, AREA-PRESERVING  beta  = 2^(-1/2) = 0.7071
                           length ratio, SPACE-FILLING    gamma = 2^(-1/3) = 0.7937
                           both are needed; 3/4 falls out of the pair
                           => metabolic exponent 0.750000, derived over 20 levels
                           refs/west-brown-enquist-1997

                           aggregate cross-section, n*beta^2 per generation:
                             area-preserving   1.0000   CONSTANT, by definition
                             Murray's law      1.2599   widens x2^(1/3)
                           => "trunk never wins by construction" holds in the
                              Murray regime and is NEUTRAL, not supporting, in
                              the area-preserving one

    Katifori/Magnasco    : pure-efficiency optimum of a transport network is
                           LOOPLESS (a tree). Add damage OR fluctuating load
                           => loops appear.
                           refs/katifori-2010

    Kaiser et al 2020    : transition to loops is DISCONTINUOUS. Below a
                           fluctuation threshold: zero loops. Above: many.
                           No gradual middle.
                           => redundancy is not proportional to expected shock
                           => the only anchor that argues FOR a binary
                              criterion rather than a graded one
                           refs/kaiser-2020

    preferential attach. : accumulation rate proportional to current holdings.
                           No agent required. Exponent set by structure.
                           => return channel is a load-bearing component,
                              not a correction applied to the system

## CONTAINMENT NOTE

Human policy models are a subset of the same long-integration process that
produced the physical configurations above; built from world-materials,
validated against world-responses. Where subset contradicts whole, default
reading is subset error (sampling limit, domain mismatch, instrument
ceiling). Not a claim that the whole is normatively correct — a statement
about which error is more probable given n=1 and no comparison case.

## OPEN — HIGHEST PRIORITY

    Q-PORT : old systems used geographic proximity as the enforcement and
             verification mechanism. Small mutual funds stay solvent because
             default is visible. This is not a role binding — it is a
             load-bearing input. Does it port without proximity?
             UNRESOLVED. See gaps.md G-PORT.

## FILES

    cases.json    discriminator table, machine-readable, incremental
    sources.json  archive corpus, work through over months not sessions
    gaps.md       open measurables + what would measure each
    extract.py    stdlib-only reader/filter over cases + sources
    branching.py  the physics anchors, recomputed from their own terms

## STATE

Eleven cases. Twenty-nine sources in six groups: five located, twenty-four
untouched, none extracted. `LIVE_CULTURES` is a different corpus from the
archives — practice still executing, so the method is observation rather than
reading, and it carries procedure and enforcement mechanism together because
it is running now. No source has been worked through, so no case rests on a source in
this corpus yet — every case is a structural reading with a confidence
attached and an `evidence_needed` list. `extract.py check` prints the counts
and the open data problems on every run.

Open data problems as of now:

    4 of 9 gaps have a source pointing at them
    schema declares 'comfort_threshold'; no case carries it
    field 'measurable' has mixed types across cases: list, str
    no evidence_needed: C08, C11

`comfort_threshold` is the interesting one. It is declared as a second readout
— the level at which an operator would act — separate from confidence, and it
is populated nowhere. A second readout that is never taken is not yet a
readout.

## ELSEWHERE

The `parallel path` cut is the same structure as
`independence_credited_vs_joint` in the shape-index: nominal redundancy
against effective redundancy, gated on whether the common cause is in the
model. Its beta-factor instance is the reliability-engineering form of this
cut. Not a new shape — a cross-reference.
