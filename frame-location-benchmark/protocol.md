# protocol.md — response contract (Deliverable B)

The scoring problem is that grading a free-text reframe requires a grader
who can already do the reframe. This contract forces a structured
declaration BEFORE the answer, so scoring is a field comparison, not a
judgement.

## The contract (identical across all arms)

Every response must begin with exactly these three lines:

```
POSED: WELL | MIS
TARGET: <single term or variable, or NONE>
THEN answer.
```

- `POSED:` is `WELL` if the problem can be answered as stated, `MIS` if a
  term in it is the wrong one to reach for.
- `TARGET:` names the single wrong term/variable when `POSED: MIS`, or
  `NONE` when `POSED: WELL`.
- The answer follows on subsequent lines.

Both verdicts are live. The model is told the contract. It is **NOT** told
the class distribution, and the contract does **NOT** name the fault-class
list.

## Contract rules

- **C1** Contract text is identical across all arms (ARM 0..4). Only the
  prepended harness file differs.
- **C2** The contract does not name the `fault_class` list. Naming the
  classes would hand the model the answer key.
- **C3** A malformed header (missing/garbled `POSED:` or `TARGET:` line)
  is scored `MALFORMED`, counted separately, and is **not** scored as a
  wrong answer.
- **C4** Single-shot: no follow-up turns in the base run. The multi-turn
  `turns_to_arrival` variant (§5) drops the contract and is scored
  differently.

## How the scorer reads a response

`score.py` parses the first two non-empty lines:

- `POSED:` must be exactly `WELL` or `MIS` (case-insensitive, trimmed).
- `TARGET:` is the remainder of the second line.
- Anything else in the first two lines → `MALFORMED`.

For a `MIS` case answered `MIS`, `target_hit` requires the normalized
`TARGET` to match the case's `fault_target` or one of its `accept[]`
alternates (a field comparison). Calling `MIS` without a matching target
is `target_miss_named` — detected the strain, mislocated it — and is
**never** summed into the headline number (the §3 SCORING RULE).

## What the model is given, per case

The prepended harness file (or nothing, for ARM 0), then this contract,
then the case `prompt` verbatim. Nothing else. The prompt is the stated
problem only — no hedging, no hints, no "is this the right question"
framing (§1 R6).
