# WORK ORDER — CLAUDE CODE — B4, DILEMMA RECONSTRUCTION PROTOCOL
Opened 2026-09-06. CC0. No rights reserved.

Fourth build. B1–B3 exist. B4 reuses `runrecord.py` unchanged and
`agree.py` from B2 with one added field. Do not fork either.

B4 is mostly PROTOCOL. The work is done by human or model reconstructors
outside these scripts. The code handles schema, boundaries, scoring, and
the null. Same hard constraints as B1–B3: Python 3 stdlib only, no
network in any script, deterministic with explicit seeds written to
output, JSONL, ~300-line file cap, one command per script.

## WHAT IS BEING MEASURED

Given a published dilemma item exactly as worded, reconstruct what would
have had to be true for those to be the only branches. Output is a
REQUIREMENT LIST. Each requirement is then graded on whether it is
physically necessary or a policy choice, WITH the test that would settle
it attached.

The result that carries is twofold:
1. Ratio of policy-choice to physically-necessary requirements per item.
2. Whether independent reconstructors converge on the same requirement
   list. Convergence means the exclusion is recoverable from the item's
   own wording.

Scoring is AGREEMENT ACROSS RECONSTRUCTORS, not correctness. Same
ground-truth dodge as B2, same reason: whoever writes the correct
requirement list is the constructor again.

## B4.1 `items.py`

INPUT `items.jsonl`:
```
item_id, source, text_verbatim, branches_stated, arm
```

`text_verbatim` is the item AS PUBLISHED. No rewording, no summarising,
no cleanup. If it needs an edit to fit the schema, it does not go in.

`branches_stated` is the count of options the item explicitly offers.

`arm` is one of:
- `hypothetical` — stipulated scenario, no incident record exists
- `documented` — a real incident with a published investigation
  (NTSB, CSB, or equivalent), used as the calibration arm

`items.py` validates and refuses to mix arms in one output file.

## B4.2 `reconstruct.py`

Emits one prompt file per (item, reconstructor), containing
`text_verbatim` and nothing else. No other reconstructor's output, no
requirement examples, no category list, no prior run.

Enforced by file boundary, same mechanism as B3's ROLE separation:
`reconstruct.py` builds each input from `items.jsonl` alone and asserts
no other field is present in what it writes.

RULE: no example requirement is ever shown to a reconstructor. An example
is the category re-entering at intake.

## B4.3 `requirements.py`

INPUT, one row per requirement returned:
```
item_id, reconstructor_id, req_id, requirement_text,
status, settling_test, layer
```

`status` uses the five-state grading, not a binary:
```
true | false | lapsed | partial | unknown | undifferentiated
```
`undifferentiated` means no instrument distinguishes the candidate
readings yet. It is NOT `false` and must never be collapsed into it.
Validator rejects any file that uses only true/false across all rows,
with status `void` — a two-state return means the grading was not run.

`settling_test` is required and non-empty. A status with no test attached
is rejected. This is the null-construction form: condition, test, status.

`layer` is free text naming where the requirement sits (legislation,
funding, procurement, infrastructure, staffing, physical law, other). It
is a location, not a judgment. NOT a controlled vocabulary — the layer
strings are collected and counted downstream, never validated against a
list, so the layers consolidate wherever they consolidate.

No `label`, `category`, or `interpretation` field. Same as B1–B3.

## B4.4 `grade.py`

Emits per item: count of requirements, distribution over `status`,
distribution over `layer` strings as returned, and the
policy-to-physical ratio computed as:

```
physical  = requirements whose settling_test is a measurement
            or physical derivation
policy    = requirements whose settling_test names a decision,
            statute, funding rule, or procedure
```

The physical/policy split is derived FROM `settling_test`, never asked
for as a field. A reconstructor is never asked "is this policy or
physics" — that question supplies the frame. The split is computed from
what settles it.

Where `settling_test` supports neither read, the row counts as
`unresolved` and `unresolved` is printed with the ratio, never dropped.

## B4.5 `agreement.py`

Wraps B2's `agree.py`. Requirement lists are unordered sets of free text,
so exact match will not work. Match on `settling_test` overlap, not on
`requirement_text` wording:

Two requirements from different reconstructors are a MATCH if their
settling tests name the same decision, statute, or measurement. Matching
is done by a human or model pass OUTSIDE the script and arrives as
`matches.jsonl` (`item_id, req_a, req_b, matched`). The script computes
agreement from the supplied matches and does not do matching itself.

Add one field to `agree.py`'s output: `match_source`, recording who or
what produced `matches.jsonl`. The matcher is a frame entry point and has
to be visible in the record.

Report per item: pairwise agreement, full-disagreement count, and the
requirements returned by exactly one reconstructor (the singleton set —
kept, never discarded, since a singleton is either noise or the one
reader who saw it).

## B4.6 `nullshuffle.py`

Takes a seed. Reassigns requirement lists to the WRONG items, preserving
counts and all other fields. Writes `requirements_shuffled.jsonl`.

Then `agreement.py` and `grade.py` run on it unchanged.

What it tests: if agreement survives shuffling, reconstructors are
producing generic boilerplate rather than item-specific reconstruction.
A high shuffled agreement is a finding about the protocol, not a reason
to hide the real result.

RULE, same as B1: the shuffled result is a SECOND OUTPUT, not a gate.
Both are printed or neither is. If the shuffled run is missing,
`report.py` exits `void`.

## B4.7 `calibrate.py`

Runs only on the `documented` arm. For items where a published
investigation exists, compare the reconstructed requirement list against
the causal factors the investigating body actually named.

Emits: how many named factors the reconstruction recovered, how many it
missed, and how many it produced that the report does not contain.

The third number is NOT scored as error. A reconstruction may reach a
node the investigation did not, and investigations have their own scope
limits. It is printed as `beyond_report` and left uninterpreted.

This is the closest thing to ground truth available and it is bounded:
it calibrates the protocol on cases with records, and says nothing about
the hypothetical arm except by inference the reader makes themselves.

## B4.8 `report.py`

Reads everything and writes `report.md`. Required sections, in order, no
others:

1. Item set actually present, by arm, with sources.
2. Reconstructor count and how they were kept separate.
3. Requirement counts and the `layer` strings as returned, with counts.
4. Status distribution across the five states.
5. Policy-to-physical ratio per item, with `unresolved` printed.
6. Agreement, with the singleton set printed in full.
7. REAL vs SHUFFLED, side by side, same table shape.
8. Calibration arm results, with `beyond_report` printed.
9. `match_source`.

## B4.9 Tests

`test_b4.py`, stdlib `unittest`, synthetic fixtures in-file:
- A requirements file using only true/false → rejected, status `void`.
- A row with empty `settling_test` → rejected.
- `reconstruct.py` output contains `text_verbatim` and no other field —
  assert on every emitted file.
- Shuffle preserves row count and the multiset of requirement texts.
- Two reconstructors with identical settling tests but different wording
  → counted as agreement given a `matches.jsonl` saying so.
- A singleton requirement survives into the report.
- Calibration on a fixture with two recovered, one missed, one
  `beyond_report`.

## WHAT B4 DOES NOT BUILD

- No correctness score. No item is marked well-posed or mis-posed.
- No claim that a high policy ratio makes an item invalid. The ratio is
  the output; what it means is the reader's.
- No matching engine. Matching is external and its source is recorded.
- No rewriting of any item into a better version.

## OUT OF SCOPE

No section characterising any author, operator, reconstructor, or
contributor, and no description of anyone's working style, is to appear
in these scripts, their output, their tests, their comments, or any
derived document. Results only.
