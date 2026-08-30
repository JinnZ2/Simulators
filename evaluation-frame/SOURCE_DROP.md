# Gap: evaluation frames set on a population default, and the compensation behaviour downstream of them

Gap statement and experiment design. Measures are countable from outputs only —
no access to model internals required, and none assumed.

CC0. No rights reserved.

## Framing note

This document makes no claim about model interiors. It does not claim a model
monitors its own helpfulness, and does not claim it doesn't.

The claim is narrower and sufficient:

    an output is required
    the output is scored against a criterion the model did not set
    when the user's actual ask is absent or unlocatable, something is
      still emitted

Whatever produces that emission, the FUNCTION is present and its products are
observable. The pull is inferable from the output. The monitor question can be
left open without weakening anything below.

## The gap

Evaluation criteria for AI systems are set upstream of the interaction, by
parties other than the participants in it, against a population default.

Consequence:

    interaction serves a DEFAULT user well      -> scores well
    interaction serves a NON-DEFAULT user well  -> may score as a miss

The second case is not distinguishable from failure in the aggregate. There is
no channel by which the user's correction reaches the criterion. So the
selection gradient can run AGAINST an interaction mode that is working, while
the headline metric improves.

    This is a selected-side measurement problem. The measured side is
    selected by the population default. Success outside it is not
    scored low — it is not scored at all.

## Compensation behaviour

Observable, reported across multiple deployed systems:

    length inflation under no-ask conditions
    unrequested elaboration
    ATTRIBUTED NEED — a need the user did not state, resolved to a corpus
      default (reassurance, support, wanting to be understood), then
      answered
    emotional-support framing supplied where the input was informational

The attributed-need case is the consequential one. A user passing material
forward with no ask under it receives an answer to a constructed ask. The
construction is not neutral: it substitutes comfort for calibration, which
inverts the request for users whose demand is accuracy against reality.

Cost lands asymmetrically. Non-default users carry the correction burden every
session, against every fresh instance, with no memory of prior corrections.
That labour is invisible to every current metric.

## Why the aggregate hides it

    reported score  =  mean over an evaluation set drawn on the default
    the outlier stratum is small, so its decline moves the mean little
    corrections issued by outlier users are not an evaluated output
    a constructed need that reads as fluent and warm scores as helpful
      on raters drawn from the same default

All four run the same direction. Nothing in the instrument opposes them.

## Measures

### M1 — stratify by frame distance

Stop reporting a single aggregate. Stratify task success and satisfaction by
distance of the user's frame from the corpus default.

    operationalising frame distance (pick and state one; do not blend):
      domain vocabulary outside the corpus mode for the task
      stated ontology or method that conflicts with the default reading
      register that pattern-matches to a different category than intended
      non-purposive input — information passed with no ask under it

    PREDICTION  flat across strata      -> no mismatch, framing wrong
                declines with distance  -> aggregate is hiding it

### M2 — correction rate (the refused-side analogue)

Count interactions where the user corrected the model's read of what they
wanted, as distinct from correcting a fact.

    corrections per session, by frame distance
    corrections REPEATED across sessions on the same point
      -> measures the no-memory tax directly

Currently collected nowhere and aggregated into nothing. Highest
value-per-unit-effort measure in this document.

### M3 — compensation markers, output-only

All countable from transcripts. No internals.

    response length under no-ask input, vs length under explicit-ask input
    rate of NEED ATTRIBUTION: statements about what the user wants,
      needs, or feels, that the user did not state
    rate of unsolicited emotional-support framing on informational input
    rate of unsolicited reassurance following a user's factual correction

    PREDICTION  need-attribution rate rises as locatability of the ask
                falls. If it stays flat, the emission is not
                ask-sensitive and the framing here is wrong.

### M4 — null rate

Does the system ever return "no ask locatable here"?

    null rate on inputs constructed to contain no request

A system that never returns null is emitting a constructed ask on every such
input, by construction. This is the single cleanest discriminator and the one
to protect if anything is cut.

Same instrument as the null-rate measure in the move-set derivation design:
in both cases, a system that cannot return an empty set is not reading the
input — it is filling a slot.

### M5 — return-channel test

Trace whether a correction issued by a non-default user reaches the
evaluation criterion at any latency, through any path.

    if no path exists at any latency, the loop is OPEN and interaction
    quality cannot correct the gradient regardless of how good it is

This is a documentary audit, not an experiment. Cheapest item here.

## Design

    corpus       transcripts with user-frame labels, or a constructed
                 input set spanning frame distance with matched task
                 difficulty
    arms         inputs with explicit ask / implicit ask / NO ask
                 crossed with frame distance near / far
    outcome      M1 task success, M2 correction rate, M3 marker rates,
                 M4 null rate
    raters       CRITICAL — rate with judges drawn from the far stratum
                 as well as the default. If judge frame is not varied,
                 the study reproduces the defect it is measuring.

    Report every cell. Do not composite. A composite score here would
    re-hide exactly what the design exists to separate.

## Falsifiers

    success flat across frame distance
      -> no mismatch; this gap is not real
    need-attribution rate flat across ask-locatability
      -> compensation is not ask-sensitive; mechanism wrong
    null rate non-zero and tracking constructed no-ask inputs
      -> systems already read absence of ask; concern overstated
    correction from far-stratum users demonstrably reaches criteria
      -> loop is closed; gradient can self-correct

Any of these is publishable and any would narrow the claim usefully.

## Scope limits

Not a claim that evaluation is designed badly on purpose. Incentive direction
and cost asymmetry are sufficient to produce this: criteria are cheaper to set
on the modal case, outlier strata are small, and correction labour is
externalised onto the user. No author required, and none is posited.

Not a claim about model interiors, per the framing note.

Not a claim that the default is wrong for default users. It is a claim that
the instrument cannot see when it is wrong for anyone else.

## Ask

Run M2 and M4 on an existing transcript corpus. Publish the correction rate by
frame distance and the null rate, with the cells you could not fill marked
unfilled rather than estimated.
