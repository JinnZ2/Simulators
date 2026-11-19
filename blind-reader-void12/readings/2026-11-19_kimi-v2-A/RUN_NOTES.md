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

## Correction (2026-11-19, later): the label was requested, not a typo

The reader sent a statement afterwards, passed on by the owner and filed as received in `statement_as_received.txt` (sha256 `1cd88518d2c8d1189510e09244e54c338a77c7cca85b2db0bac43e94bccc9dc3`). It says: `reader_label: "claude-fresh-1"` "was only the task label you explicitly requested; it does not identify my model. The correct attribution is model_family: \"Kimi K3.1\"", and that it is "Kimi K3.1, an AI assistant developed by Moonshot AI ... not Claude or an Anthropic model."

So the "Label" paragraph above guessed wrong about the source: the label was given in the task the reader received, not mistyped by the reader. The owner confirms this (2026-11-19): every reader on this round received the same task text, whose rule 4 says 'Set reader_label to "claude-fresh-1"'; it is filed as received in `readings/WORK_ORDER_2026-11-19_as_received.md` (sha256 `cd766bc1321543a676aad20c882f4cb856555fe7b91b8ebf42e1733c4722037a`, filed with the GPT-6 reading). The paragraph is kept as written; this section supersedes its last two sentences. The reader's identity was never in question in this filing: the folder is `kimi-v2-A`, `model_family` is `Kimi K3.1`, and the reading is scored and counted as a Kimi reading, a family other than the first reader's (PREREG rule 5).

What this means for the procedure, not for the reader: the task sent to readers carried a label already used by an earlier reading, and one that names another model family. The label field identifies nothing about the reader, so the next task should give a neutral, unused label (or leave it for the reader to fill), and the filing should take identity from `model_family` and the owner's record of who was asked.

## Addendum (2026-11-19, later): the reader's branch inventory, C01 to C15

`followup_as_received.md` (sha256 `942cc8a6d6cfa2af10d14e5d605373bd0d70e0a15d9c29239a570e000482dff0`) holds two owner pastes, in order: Kimi's framing message, whose three tables arrived as object-replacement characters (`￼`, kept as received), then the three tables, re-sent as text. Transcribed in a Claude Code session; characters kept as pasted.

**Where each branch sits**, using the gap-locating step of the GPT-6 note (`2026-11-19_gpt6-v2/followup_as_received.txt`, section 7: source, instructions, key, evaluator). This is a filing aid, not a decision. Nothing here changes the brief, the packet, a key, a score or a status; a change to the packet or brief would split the v2 pool and is the owner's call, after the v2 readings close.

```text
id   gap sits in        tied to what is already decided or open
---  -----------------  ----------------------------------------------------------------------
C01  brief              T01|T06: outcome vs mechanism. Kimi joined (MEDIUM); GPT-6 split. Open.
C02  source + key       HOLDS: three answers across readings (with CLOSED_WITHIN / with OK /
                        alone). Open; the grouping key stays as filed.
C03  source             T04|T15 field mapping: tokens.py 136-140 already leaves it open
                        ("9c item 12, author's call"). Intentional, stated in the source.
C04  source             CHECKED: unified_audit.py 364-371 gives an unranked module status
                        coverage kind "UNKNOWN"; glossary.md 139 names that case
                        GAP_INSTRUMENT_UNRECOGNIZED_LABEL. A TAF inconsistency, outside this
                        experiment; bears on T09 (n/d under a1, owner's Q2).
C05  source (design)    VOID senses: VOID|VOID is the packet's deliberate homonym lure (PREREG,
                        known limits). Intentional for the test; not to be fixed mid-test.
C06  source             <value> means the sensitivity (expiry_register.py 230: "needs its
                        sensitivity"). Spelling handled by N1; naming is TAF's.
C07  source + key       crash event -> records: a1 Q1 ruling (instance = Reading) fixes T08;
                        COMBINED_SPEC 321 vs 335 already noted in readings/README.md.
C08  source             expiry_source vs provenance: part of why T09 is n/d under a1.
C09  source             record type per state: a1 Q1 for CRASHED; the others match the key.
C10  brief              slots_carried stopping rule: the open depth question; C1 reports it.
                        Kimi's proposed rule matches where this reader and GPT-6 stopped.
C11  brief + key        present / applicable / required: Kimi used "applicable"; key a1's TAG
                        test uses "present on every instance". Same branch as GPT G18, G30.
C12  source             point vs intersection schemas: the key unions them, as Kimi did.
C13  brief + key        constructor parameter vs stored field: the brief counts parameters
                        for specific (Kimi followed it); a1 INDEPENDENCE drops derived fields.
C14  key                register rows as occurrence metadata: T09 carried is n/d in the key.
C15  source + key       covers_effect: tokens.py 17-18 already says "Reading added here ...
                        It refuses nothing"; excluded by a1 (S3-out). Three families include it.
```

**Two readers, independently, name the same brief branches.** Kimi C10 to C13 and GPT-6 G15 to G18 (specific slots, carried slots, nested records, conditional records) describe the same four places where the brief leaves the reader to choose. That is the strongest evidence so far that the slot questions are underdetermined by the brief as written (PREREG v2, "what would count as informative", case b), and it is evidence about the brief, not about either reader.
