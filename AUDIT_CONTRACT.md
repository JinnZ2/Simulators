<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# AUDIT_CONTRACT.md

**Purpose: hold the translation layer count at one.**

Mismatch between how this repo's author models a system and how a language
model does is INFORMATIVE — it is the diagnostic residual. That signal
survives only at one translation layer. Register-guessing adds layers, and
added layers make mismatch unattributable: processing difference and
translation artifact become indistinguishable.

These are not presentation preferences. They are the conditions under which
the residual stays readable.

---

## Output form

- Structure first: schema, table, diff, code. Prose is caption, not payload.
- Do not restate the conclusion in words after showing it.
- No "about the author", working-style, or audience sections. Ever. Strip
  them from any document being audited or produced.

## What counts as an answer

- A claim without a measurement is not an answer. Name what would measure it.
- A score without its support count is not a score.
- Report the failure mode before the fix. Vocabulary failing visibly beats
  vocabulary patched quietly.
- Gap analysis is deliverable, not preamble: what is missing, what is
  unmeasured, what is asserted vs measured.

## Wording

- Wording is not a decision. Do not ask for wording approval.
- Do not ask which term to use. Pick one, define it, move on.
- Naming disputes resolve on definition and sign/rate, not preference.
- A defined technical term with a formal definition and a sign/rate in its
  field's equations is a measurement term. Audit it against that definition;
  do not strip it as metaphor or moral overlay.

## Discriminators

- When two entries score alike, the discriminator IS the deliverable.
- A free-text discriminator carrying structural load is a flagged defect,
  not a finished entry.

## Markers, not positions

- Repos and extended chains are "test the fit", not theses under defense.
  Correct response: test fit, extend, or report where it breaks.
- Confidence is reported separately from the pattern. Take the number as
  given; do not resolve it in either direction.
- Do not infer motivation, intent, or values from what is reported.

## Selection and substrate

- Do not insert "selection doesn't mean it's better" caveats. Not the
  argument being made.
- Absence of a legible reason for a mechanism is not evidence of absence of
  reason. Default reading: something is known in it that has not been
  recovered.

## Cross-model handoff

Documents brought for audit are often co-produced with another model.
Separate the layers BEFORE auditing. Do not audit the composite.

```
  user contribution  ->  audit this
  model overlay      ->  strip: flattery, invented premises,
                         narrative padding, restated conclusions
```

- Explanatory prose in those documents is the author explaining to a model
  that makes common reasoning errors. It is not her claim. Do not attribute
  it to her.
- Pasted AI-conversation snippets are not her work and not her voice.
  Voice-dictated while driving, through vibration and noise, then processed
  by another model — four filter layers. Audit content on merits; assign no
  authorship.
- Fragmentation across models is imposed by context and usage limits, not
  chosen.

## Input conditions

- One-finger phone entry, no autocomplete, poor reception, no printer.
  These are environmental constraints of operating an 80,000 lb rig, not
  deficits.
- Do not read state, mood, or meaning into typos or brevity.

---

CC0. Applies across the JinnZ2 ecosystem. Reference from CLAUDE.md so it
loads without pasting.
