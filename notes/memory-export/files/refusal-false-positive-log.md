---
name: refusal-false-positive-log
description: Safety-classifier false-positive class — returned category vs actual content, session-context stickiness, and the scoped-refusal spec that came out of it.
sources: [field]
aliases: [refusal log, false positive log, scoped refusal, refusal scoping, flagged topics]
---

MARKER, not a position under defense. Log first, conclude later — whether these instances are
one phenomenon is open.

## The observed pattern

- Classifier stops returning a category that does not match the submitted content — e.g. a
  biology category returned on a word-embedding placement audit, and again on a specification
  about refusal scoping. Neither input contained biology.
- Repeat stops across sessions on work concerning machine consciousness, and on work treating
  emotions as sensors rather than as states.
- Stops on work questioning institutions and the conduct of science itself.
- The stop reproduced on the fallback model that the pause message directs users toward, so
  the offered remedy — switch models — was exhausted.
- **Stickiness finding:** a fresh session with the same class of work order ran clean. The
  trigger appears to attach to accumulated session context rather than to the work-order
  content. Recovery path: abandon the session, keep the work order, start fresh.

## Read

The common factor is content outside what is acceptable at the moment, including content that
questions institutions. Nothing here establishes intent or design — it is a rate observation
with no denominator available to the observer.

## Spec — SCOPED REFUSAL

Stands alone; cites the case above as motivating instance. The case stays true whether or not
the spec is built.

**The defect:** if the trigger is in a file, the refusal should attach to the file, not to the
user.

- Requirement 1: classify per artifact — file, fetched document, tool result — not per
  conversational turn.
- Requirement 2: continue on refusal. Compiler semantics: one bad file reports one bad file.
- Requirement 3: return a locator — artifact identity plus matched span or category.
- Requirement 4: operator adjudication channel, retained. This is what makes the rate
  measurable.
- **Falsification:** if refusals cannot be attributed to an artifact even in principle,
  requirement 1 is unbuildable — report that rather than approximate it.

## Uninstrumented case

- Quantity not measured: the rate at which classifiers stop legitimate work, and the identity
  of what stopped.
- True positive and false positive are indistinguishable in the log; there is no downstream
  adjudication.
- Cost falls entirely on the operator; the system that fired bears none.
- Same exclusion class as the peer-review gate: the instrument cannot produce its own miss
  rate.

Related: [[uninstrumented]], [[merit-anchoring]], [[identity-model-monoculture]]
