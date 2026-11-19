# Reading: Kimi K3.1, packet v2 variant A (2026-11-19)

**What this is.** The first reading by a reader of another family, made after key v2 amendment 1 was merged (PR #318) and after its hashes were pinned in `PREREG.md`. It was read from the unchanged v2 packet (variant A, sha256 `94836e79b966a89fe9a14464e0930462d039aba052cc44377b9b092d7ca24a63`) and sent through the owner. Nothing in the key, scorer or packet was changed for or after it.

**Filed as received.** `raw_output.txt` is the owner's paste, byte for byte (sha256 `3370d36e42558b95842a3650b7dc11b776877cfdec20ff4cbe02dfb612d5cd4c`, 15,865 bytes). `response.json` is the same JSON re-indented, nothing else. `score.*` is under key v2; `score_a1.*` under key a1. Both ran with exit 0, so the scorer's validation passed.

**Label.** The reader wrote `reader_label: "claude-fresh-1"` (the template's label is empty). That string is the label of an earlier reading, and it is not in the packet. The work order the owner pasted lists the labels already filed, so the likeliest source is that list, not a leak from the packet; this is a guess. The folder is named `kimi-v2-A` and the reader's own `model_family` is `Kimi K3.1`. Treat the label as a typo, not as identity.

**Blindness (self-report, not checked).** All six attestations are "no". The reader's notes add: web search and code execution were available and could not be disabled, neither was used for the task (it says no packet code was run); shell and file tools were used to unpack and read the archive; an unrelated memory profile was present and not used. The scorer's header says BLIND.

## Results (the numbers are from `score.txt` and `score_a1.txt`)

| | key v2 | key a1 |
|---|---|---|
| grouping, adjusted Rand index | 1.000 | 1.000 (grouping is not amended) |
| `slots_specific`: declared pairs agreeing with the key | 6 of 7 | 6 of 7 |
| `slots_specific`: slot sets equal to the key's | 8 of 14 | 7 of 14 |
| `slots_carried`: declared pairs agreeing | 7 of 7 | 7 of 7 |
| `slots_carried`: slot sets equal | 11 of 14 | 11 of 14 |

The one specific pair that disagrees is UNDECIDED | UNRESOLVED: the key has MAPS (both lists empty); the reader gave T01 `[proposal, first_undecided_subbox]` and so PARTIAL. Under a1, UNKNOWN | UNKNOWN is n/d on both meanings.

Under a1 every unequal `specific` list is a reader superset (extras, nothing missing): 7 supersets, 0 subsets, 0 overlaps. Under `carried` there are 2 supersets (T10, T12) and 1 subset (T02, where the reader gave `[]` and the key has `value`).

## Comparison with the other v2 reading (Claude-v2-A), under key a1

The grouping differs: this reader did not join HOLDS with OK, which both Claude readings did, and matched the key's grouping exactly (ARI 1.000 against 0.823). On `carried` this reader's lists are far closer to the key's (11 of 14 equal against 2 of 14): the Claude readings reached one level of wrapper higher, this one did not. Those are observations on two readers of two families, with one reading each.

The `specific` supersets are largely the same across the two readers:

- T01: both add `proposal`, `first_undecided_subbox`
- T05: both add `covers_effect`
- T07: both add `first_subbox_with_no_value`, `void_reason`
- T10: both add `exception_type`
- T12: both add `typed`, `untyped`
- T08: both add `inputs`; this reader also `exc`, the first parameter of `crash()`, and has the key's `exception`, `path` (it took the union of two routes); Claude adds `call`
- T15: only this reader adds `instrument` (a parameter of `E()` in `tokens.py`, whose record key is `instrument_class`)

What this is evidence for, and what it is not. Two readers of different families make the same additions on five terms. Under the rule the key now uses, these names are excluded because they are computed from other fields (`covers_effect`, `typed`, `untyped`, `exception_type`) or are not on every instance (`proposal`, `first_undecided_subbox`, `void_reason`, `first_subbox_with_no_value`). So readers following the brief's wording ("tied to this term and to no other") do not apply the INDEPENDENCE half of the rule or the every-instance half. That is a statement about the brief and the definition of "slot", which `OPTIONS.md` section 6.4 already lists as a definition and not a physical fact. It is not a finding that the key is wrong, and it is not a finding that the readers are. It is the thing the amendment's own text said a reader would test.

**Bearing on the open T10 question (not decided here).** In `slots_carried`, both readers add `error` and `exception_type` to T10 (the key lists the six coverage-entry keys), and both add `expiry_condition`, `input`, `kind`, `missing_path`, `module` to T12 (cplay UNKNOWN), and on T09 both add the same eight names. For T10 this agrees with the earlier observation that the carried list may be short by `error` and `exception_type`, because the brief also counts the section record the same handler builds. It is one more piece of evidence for the owner's pending choice, and not a change: no key list was edited. If the owner amends carried, it should be a separate amendment with its own hash, and this reading would then be scored under it as well as under a1.

## Limits

One reader per family, one run each; no repeat, so reader noise is not estimated. The scorer's Clopper-Pearson intervals for 7 pairs are wide (0.42 to 0.996 for 6 of 7). The key lists are derived by the same people who wrote the rule; this reading is independent of the amendment's content, not of the key's author.
