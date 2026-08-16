# declared-frame

A six-field block to attach to any measurement, and a checker that tests two
of them for comparability.

```
frame:
  boundary:         what is inside the accounting
  horizon:          over what time the outcome is scored
  who_counts:       whose outcomes enter the total
  sign_source:      where "better" was set, and by whom
  logic:            which formal system
  observer_access:  unknown | partial | verified
```

The block holds. The checker inverts the one rule the doc calls
load-bearing.

## Contents

| File | What it is |
| --- | --- |
| [`THE_DECLARED_FRAME.md`](THE_DECLARED_FRAME.md) | The delivered document, **verbatim**. |
| [`check_frame.py`](check_frame.py) | The delivered checker, **verbatim**. |
| [`frames/`](frames/) | The delivered worked example, plus its counterpart so the comparison runs. |
| [`frame_audit.py`](frame_audit.py) | Null-tests the comparability verdicts. |
| [`layer_zero.py`](layer_zero.py) | Every field is switchable, so nothing adjudicates. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Seven claims (`DF_001..007`). |
| [`samples/`](samples/) | Pinned output. |

```bash
python3 check_frame.py frames/panel_conversion.json
python3 check_frame.py frames/panel_conversion.json frames/leaf_conversion.json
python3 frame_audit.py
python3 layer_zero.py
```

Standard library only, deterministic.

## What holds

**The three-way split.** The fields are not interchangeable:

```
boundary          core -- must match
horizon           core -- must match
who_counts        core -- must match
logic             separate mismatch line
sign_source       recorded, never compared
observer_access   recorded, never compared
```

`sign_source` and `observer_access` are not comparability conditions. Two
results can share a boundary and disagree about which direction is better,
and that disagreement is legible precisely because both declared it. Making
them core would refuse comparisons that are sound. (`DF_001`)

**UNKNOWN as a legal value.** A declared gap stays explorable. An omitted
one does not.

## What does not

### The checker inverts its own load-bearing rule

```
core field `horizon` on side B:

  omitted      NOT DIRECTLY COMPARABLE      rc 1
  'unknown'    UNDETERMINED                 rc 0
```

The doc says omission "converts an open question into a settled one by
silence". `compare()` does exactly that: it reads
`str(a.get(f, "")).strip()`, a missing field becomes `""`, and it is
compared as a value. The `unknown` branch is checked first and never
reached.

Omission produces the **more confident** verdict, in the function shipped to
prevent that. Three-line fix: treat a missing core field as undetermined,
labelled omitted rather than declared. (`DF_002`)

### Comparability is exact string equality on free text

Two frames whose boundary differs only in clause order come back
`NOT DIRECTLY COMPARABLE`.

This is the inverse of [`measurement-fork/`](../measurement-fork/)'s
classifier failure — there a token matcher **over**-matched and marked
questions covered that no probe reached; here exact equality
**under**-matches and marks frames different that are the same.

Under-matching is the safer direction. The problem is that there is no band
for it: a textual difference gets a verdict that reads as substantive. There
is no string fix — whether two free-text boundaries denote the same
accounting is a judgement, and the honest output is the not-resolved-here
the doc already uses for its own middle band. (`DF_003`)

### The exit code reports the wrong thing

```
two complete blocks, genuinely different frames   rc 0
one block missing a field                         rc 1
```

`rc` tracks whether the blocks are well-formed, not whether the results
compare. A caller scripting `check_frame.py a b && use_both` gets a pass on
two results the tool has just said do not compare. Document it, or add a
distinct code. (`DF_004`)

## The worked pair

```
                    panel                        leaf
boundary   photon→product only.          photon→product PLUS assembly,
           Excludes fabrication,         repair, replication, load-bearing,
           mining, smelting,             transpiration, soil formation.
           transport, installation,      All fabrication, maintenance and
           maintenance, decommission.    disposal inside the same budget.

horizon    steady-state operation        whole lifecycle incl. growth
                                         and decomposition

who_counts the conversion step           the organism and the systems
                                         it substrates
```

All three core fields differ, so the efficiency ratio between them is a
frame difference and `check_frame.py` reports it as one.

That is `measurement-fork/`'s VOID RATIO arriving by a different route —
there two quantities do not divide because their `object_of` differs; here
two results do not compare because their boundaries differ.
`reasoning-gate/`'s `G-DIM` is the same check at report time. **Three tools,
three stages, one rule.** (`DF_005`)

## What is unrun

Both frames here are written from the drop's own example. The load-bearing
question is untouched: **does declaring the frame change what anyone does?**

The stated benefit is that frame disagreements stop being argued as data
disagreements. That is a claim about a process, and the measurement is
whether two parties given both blocks locate the disagreement faster than
without. (`DF_006`)

## Cross-repo

- [`measurement-fork/`](../measurement-fork/) — VOID RATIO is this check on
  quantities instead of results, at design time instead of report time. Its
  classifier fails in the opposite direction to this one.
- [`reasoning-gate/`](../reasoning-gate/) — `G-DIM` voids a ratio whose
  operands belong to different objects. Same rule, report stage.
- [`triad-playground/`](../triad-playground/) — `observer_access` is its
  reasoning-agent calibration reduced to one field, and `unknown` is the
  honest entry for the three checks that are self-report only.
- [`null-harness/`](../null-harness/) — `frame_audit.py` is its
  known-null/known-signal invariant applied to a comparability verdict.

## License

CC0-1.0, matching the repository default and the delivered files' headers.
