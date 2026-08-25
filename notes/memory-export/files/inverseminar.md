---
name: inverseminar
description: Tacit-knowledge capture tool — the model reconstructs the reasoning, and the human's correction is the product.
sources: [field]
aliases: [inverseminar.py, micro-inverseminar, TACIT.jsonl, TACIT.md]
---

Single-file, CC0, stdlib-only, phone-buildable.

## Purpose

An AI should ASK QUESTIONS where connective steps are missing, rather than guess. This tool
inverts the usual direction to make that happen.

## Design

The model presents the human's reasoning back CONFIDENTLY — hedging provokes nothing. The
human interjects only where it is wrong. **The delta is the tacit knowledge.**

Provenance is separated at capture: the reconstruction is model-authored, the correction is
verbatim human. Mixing them at capture makes the product unrecoverable later.

## Components

Triage (an overlay-density scan to find artifacts where the model wrote most and the human
wrote least); PROMPT; `record()` to TACIT.jsonl; `emit()` to TACIT.md.

Overlay-density triage scores known model-flattery signatures — "this changes everything,"
"symbiotic intelligence," emoji, bolded bullet walls — against substance markers: units,
scientific notation, FALSIF, def.

## Audit findings

- **silence = correct** scores absences as confirmations, which is the DOMINANT failure mode
  when most connective steps never left the human's head
- `[A-Z]` patterns dead against lowercased text
- No word floor on density, so tiny files top the triage
- `ratio` computed but unused; no .git pruning; no CLI

## Rewrite

Added a third channel — **CANNOT DERIVE**, which routes to questions rather than guesses — and
four explicit verdicts: corrected, answered, unprobed, confirmed. **Confirmed is never
inferred.** Plus miss-tracking and a LINKS section in emit.
