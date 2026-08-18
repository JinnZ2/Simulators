# ADAPTIVE CLAIM LOOP

Marker under exploration. Not a position under defence.

The same architecture as an adaptive simulation framework — provenance log,
claim system, an agent that reads results and proposes a change, a loop that
iterates — with one move removed.

CC0. Stdlib only. Selftest 39/39.

## THE MOVE THAT IS REMOVED

In the ordinary shape of this architecture, a failed claim hands the agent a
parameter dial and the agent turns it until the claim passes.

That operation cannot fail. It is a search over parameter space for a setting
under which the prediction is true, and the provenance log that records it —
observation, hypothesis, action, expected outcome, one row per step — reads as
a chain of reasoning. Nothing about the system is learned, and the record
looks like diligence.

This module has no vocabulary for it. `Response` has five subclasses and none
of them takes a bare parameter and a direction.

## FIVE RESPONSES TO A FAILURE

    CLAIM_UPDATE     the claim was wrong. Restate it. Needs a break condition
                     that is not the old one, and must pass the epicycle
                     guard: independently falsifiable AND predicting beyond
                     rescuing its parent.

    MECHANISM_EDIT   the sim is missing a process. Needs a basis independent
                     of this run and a prediction registered BEFORE the
                     edited sim runs, settled afterward with an explicit bool.

    INSTRUMENT_EDIT  the number is read in the wrong place — sampling phase,
                     statistic, integration step. Needs the artifact removed
                     and a quantity unchanged by the change. Takes no
                     prediction: it is not a claim about the world.

    SWEEP            a parameter is varied across levels declared before the
                     run, and the claim is restated over the gradient. See
                     below — this is the one that had to be built carefully.

    STAND            the failure is the result. Nothing is proposed. Logged.

Every free-text field on every response is screened for outcome reasoning,
not just the field named `reason` — `basis` and `prediction` are the two that
ask for justification, which is where outcome reasoning goes when it is going
anywhere.

## WHY SWEEP NEEDED THREE GUARDS

A sweep is the only response that moves a parameter, so it is where the
removed move would come back in disguise.

  **levels ≥ 2, distinct, declared before the run.** One level is a parameter
  move with a sweep's name on it.

  **a predicate over the readings, not a sentence.** A gradient claim written
  in prose with nothing that can evaluate it is a design incapable of failing
  its own falsifier. The loop runs the model at every declared level in one
  iteration and hands the whole set to the predicate.

  **the levels bracket the current value, or the reason is stated.** A ladder
  that sits entirely below the current setting, proposed against a claim that
  fails because the setting is high, is the walk. One-sided sweeps are
  admissible — with the reason in the log.

The third guard caught the stub responder shipped in this file. Its first
version used a fixed ladder and was refused the moment a scenario started
above it. That is recorded rather than quietly fixed, in `AUDIT_NOTES.md`.

## FOUR VERDICTS, NOT TWO

`SUPPORTED` / `REFUTED` / `UNDECIDED` / `NOT_EVALUATED`.

A predicate that raised is a broken instrument, not a refuted claim. A
predicate computed over an empty set is not a pass. Both land on `UNDECIDED`,
and an undecided claim is routed to the responder just as a refuted one is —
the answer is different in kind, because a refutation asks what the claim got
wrong and an undecided asks what the instrument could not resolve.

The demo shows the difference live. `ACL_drift_neutral` carries its own
resolution guard — a claim written to ±0.08 cannot be decided by a run whose
standard error is 0.091 — so at 120 replicates it comes back UNDECIDED rather
than REFUTED, and the responder's answer is an instrument edit justified by a
**computable** gap, not by the verdict.

## FOUR TERMINATION STATES

`converged` / `budget_exhausted` / `stood_on_refutation` /
`no_admissible_response`.

The last has no counterpart in the shape this copies: it is what happens when
every proposal a responder made was refused, which is a real outcome and a
loud one.

## PROVENANCE

Append-only JSONL with `SESSION_OPEN` / `SESSION_CLOSE`, every row stamped
with its session and an ordinal within it, and refused proposals logged
alongside admitted ones — the trail is what was tried, not only what stuck.

## STATE

Two demo models (a Moran drift process, a piecewise threshold response),
three scenarios, one rule-based stub responder.

**The responder is not the contribution.** It exists so the loop runs and so
every refusal branch is reachable in the selftest. Swap it for a person or a
model and the gates are unchanged — that is the whole point of putting them
in the type system rather than in the agent.

## WHAT IS NOT HERE

No claim generation. The delivered framework this was built against proposes
new claims from outcomes, and the gap here is deliberate rather than
principled: a generated claim is one whose falsifier was chosen after seeing
the data, and the admission rule for that is not written.

No real models. The two demos are sized to make the gates visible, not to
model anything. A parameter walk under a good model still tells you nothing
and a gate over a toy model still refuses the walk, so the two are separable
— and this folder only holds one of them.

## THE DELIVERED FRAMEWORK

`delivered/` holds the uploaded framework and its two provenance logs
verbatim. `replay_delivered.py` reads them and asks what this gate does with
the moves the delivered agent actually made — six findings in
`AUDIT_NOTES.md`, the sharpest being that its three-step parameter walk did
not produce the pass its log appears to show.
