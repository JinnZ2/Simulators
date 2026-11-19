# Pre-registration: blind second reading for VOID-12

Written 2026-11-18, before any blind reading exists. Everything below is fixed by the commit that adds this file. A later change goes in a new dated section at the end; nothing above it is edited.

## What is being tested

`combined-playground/cplay/vocab_branches.py` holds 15 terms from three projects and eight declared pairs. Each term carries a one-sentence predicate written by one reader (the build session). The module assigns each pair a tier, MAPS, PARTIAL, HOMONYM or NONE, from two things only: whether the two predicates are the same string, and whether the two slot lists are equal. The log in `playground-crossrun/COMBINED_SPEC.md` (section 9c) records that the predicates were assigned by a single reader and that a blind second assignment has not been run.

The question this protocol answers is narrow: **if a reader who has not seen those predicates or tiers is given the same 15 definitions and sources, does that reader group the terms the same way?** It does not ask whether the first reader is right. Neither reading is treated as ground truth; the key is called "the key" only because it is the thing being compared against.

## What a reader gets and returns

The packet is `reader_packet/` (files listed with sha256 below). It holds the 15 definitions in a fixed shuffled order under neutral ids T01 to T15, the pinned source files, a brief, and a response template. It holds no predicate, tier or branch name from the first reading, no hint of how many groups to expect, and nothing from section 9c of the spec onward; a test checks this (`scoring/test_score.py`). The reader returns the filled template.

## Blindness is declared, not enforced

The first reading is public in this repository, so no packet can make a reader blind. The reader says what it had seen in six attestation questions. The rule, fixed now:

| Attestation q1 to q4 (seen a verdict table, seen a predicate sentence, seen any mapping or second-reader report, told how many groups) | Status filed |
|---|---|
| all `no` | `BLIND` |
| any `yes` | `NOT_BLIND` |
| otherwise (any `unsure` or blank, none `yes`) | `UNCERTAIN` |

q5 (used anything outside the packet) and q6 (reachable notes from earlier sessions) do not change the status; a `yes` or `unsure` on either is printed beside it as a flag. A reading with status other than `BLIND` is still scored and filed; it is not counted toward the rules below.

## What is reported for each reading

For each response that passes validation, `scoring/score.py` reports, with no pass or fail:

1. for the eight declared pairs, the tier the reader's grouping gives, the key's tier, and whether they agree, with the count out of 8 and a Clopper-Pearson 95% interval;
2. over all 105 pairs of terms, how many the reader joins that the key joins, only the reader joins, only the key joins, and the adjusted Rand index;
3. per term, the Jaccard overlap of the reader's slot names with the key's, and the reader's stated basis for them;
4. three references: a reader who joins nothing (expected 2 of 8, checked by test), a reader who joins by label only (expected 3 of 8, checked by test), and the distribution over 20000 random regroupings that keep the key's group sizes (seed 1).

A response that fails validation (missing term, empty cluster, unknown basis value, missing attestation answer) is filed as received with the list of failures, and is not scored. It is not corrected by us. Every returned response is filed, whatever it shows.

## Rules proposed for reading the results (the owner fixes or changes these before the first reading)

These are written as proposals because they decide what the repository does with a result, which is the owner's call. If the owner changes them, the change is recorded here in a dated section before a reading is requested.

1. A declared pair is **reader-confirmed** by a `BLIND` reading when the tier agrees. It is **contested** when it differs.
2. A pair is **confirmed** in the log only when at least two `BLIND` readings from at least two different families (a human counts as a family) both confirm it. One reading, or two from the same family, can only make a pair "reader-confirmed by one family".
3. A contested pair is logged with the first reader's predicate and the blind reader's predicate side by side. Disagreement is recorded as disagreement. It does not replace the key's tier and it does not count against the first reader.
4. The `OPEN` line for VOID-12 in section 9c is changed only by the owner. This protocol produces counts and side-by-side sentences; it does not close anything.
5. Readers from the same family as the first reader (the branch names suggest a Claude model) are not independent of it in the way this test needs. They can be filed as readings but count as one family together with the first.

## Known limits, stated before any result

- One reading gives a count out of 8. Even 8 of 8 has a Clopper-Pearson lower bound of 0.63. A single reading cannot show strong agreement.
- Three of the eight pairs share a label (UNKNOWN, ABSENT_AT_SENSITIVITY, VOID). That is deliberate: it is the lure the HOMONYM tier exists for. It also means a reader who joins by label gets 3 of 8 without reading anything.
- The brief defines "predicate" as what a term is used to record, "even if the second system attaches different extra fields". That wording carries the first reader's idea of PARTIAL. It may push a reader towards joining. If two readers are available, give one the brief as written and one the brief with that clause removed, and file both; the difference is then data.
- Tier agreement depends on slot spelling. A reader who names a slot differently turns MAPS into PARTIAL with the same grouping. The scorer reports grouping (ARI, term pairs) separately for that reason.
- The key is the first reader's work, seven of whose 15 terms (T01, T02, T06, T07, T11, T12, T13) were given slots by declaration, not read from code (see `scoring/key.json`, `slots_from`).

## Pinned hashes

Base commit of Simulators main when the packet was built: `b5e8614bef123a445f247f69803e1fa4361eeed6`. Shuffle seed: 20261118. The packet was built with `build/make_packet_and_key.py`; each served source file's sha256 was checked against the pin in the first reading's module before it was written.

| file | bytes | sha256 |
|---|---|---|
| `reader_packet/READER_BRIEF.md` | 4719 | `6f33a9528e477efc03363136d7037319687037a417811a5ea0ee7d4a8469f86f` |
| `reader_packet/response_template.json` | 2887 | `e54ee502cfbc5c8b067d351e722c74a561e8517fe48d10c1f4bea9dc9caca403` |
| `reader_packet/sources/Simulators/combined-playground/cplay/axes.py` | 7786 | `0e40b7e5ce87de2226103593782e78015534e196005f6c06ed2f460d700453a7` |
| `reader_packet/sources/Simulators/combined-playground/cplay/closure.py` | 22158 | `827d681c8b08003519a60967d3b61ef891254a38bb8c02e29cacba51633c3188` |
| `reader_packet/sources/Simulators/combined-playground/cplay/tokens.py` | 5832 | `8c43890bf90ab49931a3947ff420b00368e5ce23ed82f8e57bd7aec3be6337e6` |
| `reader_packet/sources/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md` | 24327 | `72bbd97749918468a862ab72ec2af5211eb1c1c99e3f1b3e512a65b9f30160a8` |
| `reader_packet/sources/formula-audit/numcheck/check.py` | 30102 | `f6df0dc196f5ac273f864f1cab1a5a0d6c67fa88eaba53ca822f94412fb7fd83` |
| `reader_packet/sources/thermodynamic-accountability-framework/calibration/expiry_register.py` | 23071 | `ddaf2cc5b6539df340ceb84dab98e249d00a5def9f5d9f374a8ff875a04db0ae` |
| `reader_packet/sources/thermodynamic-accountability-framework/calibration/unified_audit.py` | 27122 | `fcccb9af8d8edb01940a09a639be2ff376c53781097b5562f8745a084c368a49` |
| `reader_packet/sources/thermodynamic-accountability-framework/docs/glossary.md` | 9629 | `412ed3abf4c2a546fe16def60fcb223bd496e4f297db995fcfb7232ad56c712b` |
| `reader_packet/terms.json` | 6514 | `467f4fe6769e2ee2e0fed26e91dca25e3c4c04b8f61f339adc2b01d4ab19e0ce` |
| `reader_packet/PACKET_MANIFEST.json` | 5174 | `c7327f9d3d5281dabba1c409c2e4007d87d98ed8f8bc1f5de83fb76e6f790bfc` |
| `scoring/key.json` | 6034 | `5c1a6caba4e3b0f1bc7d1a93b8e2503158e343a67d58fae5c77fe91a710a500b` |
| `scoring/score.py` | 12848 | `3f7b10c8b8319ca9ab64334aedaf6687559824010122c74b5319546e7b67540f` |
| `scoring/test_score.py` | 9758 | `7754586a18624390a48f97e102e5e823c27a003abf241bab663000c7e50b22a1` |
| `build/make_packet_and_key.py` | 9937 | `e70ad6dc49817e876d816eff56f46bede900f0cfa5c1b13b92a7f4edd8e8b21f` |
| `combined-playground/cplay/vocab_branches.py (the first reading)` | 10297 | `30fe580e4e8b6b54ded496be420fe36b0260ce9f0707dae1f71c9f00d9a94f3f` |

This file's own hash is not listed; the commit that adds it identifies it.


## 2026-11-18, later: owner's reply and pilot plan (added before any reading exists)

The owner replied "Yes please, and I agree" to the three open decisions. Read as follows; the owner can correct any of it.

1. **Reading rules 1 to 5 above are accepted as proposed.** They are now fixed.
2. **Brief variants.** Two briefs exist. **Variant A** is `reader_packet/READER_BRIEF.md` as written (sha256 `6f33a9528e477efc03363136d7037319687037a417811a5ea0ee7d4a8469f86f`). **Variant B** is `variants/READER_BRIEF.variant_B.md` (sha256 `cdaca465b8b1636990d49c653f4ded55965ec18e097d347bdcb578c42772158b`): identical except that the words ", even if the second system attaches different extra fields or detail" are removed from the definition of predicate. Both are filed whatever they show. A difference between A and B readings is a difference between two readings, not evidence about the brief: one reading each cannot separate the brief from the reader.
3. **Pilot.** One reader per variant, each a fresh isolated session of an AI model of the same family as this build, given only the packet zip and told only to read the brief and follow it. Filed as `pilot`, status as the reader attests, and by rule 5 not counted toward confirming any pair. What a pilot can show is whether the brief, template and scorer work end to end and where a reader gets stuck. It cannot show that the first reading is right or wrong.

The packet zip for variant B differs from variant A's in the brief and in that file's line of `PACKET_MANIFEST.json`; nothing else.


---

## Packet v2: the two meanings of "slots" (added 2026-11-18, before any v2 reading exists)

**Why.** In v1 the word "slots" covered three things: the fields tied to one term, the fields of the shared record that carries it, and the input names of a calculation. Three readings used it three ways, and the key used a fourth. Of the 15 key lists, 7 were written by the first reading from prose ("declared"), not read from code. The v1 slot scores therefore measure which reading of the word each reader chose more than they measure the sources. v1 results stand as filed; nothing in `readings/` is changed.

**What changes in v2 (nothing else does).** `READER_BRIEF.md` asks for two lists per term: `slots_specific` (fields the source ties to this term alone) and `slots_carried` (every named field of every record built or documented when the term is reported), each with its own basis. The calculation-input meaning is dropped; it was a third question and the first reading's `declared` lists for T01, T06 and T11 used it. The 15 terms, their order, the sources, and the grouping question are byte-identical to v1 (test `test_sources_and_terms_identical_to_v1`). The leak-check note in the manifest loses the phrase "unrelated to the vocabulary mapping" (a Claude reader named it as a hint).

**Key v2** is `scoring/key_v2.json`. Each list has its derivation written beside it and is checked by `test_score_v2.py` against the packet's own files: the cplay lists by running the pinned code, the TAF and numcheck lists by matching names in the pinned text. Two lists are **undetermined** because the sources support more than one reading: `slots_specific` for `cplay:CRASHED` (call parameters or `CoverageEntry` fields) and `slots_carried` for `taf:UNKNOWN` (no record is named). A pair that needs an undetermined list is reported `n/d`, and counts as neither a match nor a miss, so each meaning is scored out of 7 declared pairs, not 8. Key v2 was written by the same party that wrote the v1 key and this packet; it is not independent of them.

**Scoring v2** (`scoring/score_v2.py`) reports grouping once (it does not depend on slots) and the two slot meanings separately. It does not add them into one number and does not say which meaning is right. Under `specific`, two terms with no tied fields have equal empty sets and so count as `MAPS` if grouped together; that is the first reading's tier rule applied as written, and it makes `UNDECIDED | UNRESOLVED` come out `MAPS` under `specific` where the first reading declared `PARTIAL`. That difference is a result of the split, and is shown beside the first reading's declared tier in every report.

**Hand-worked references, before running the scorer.** Nothing grouped: 2 of 7 under both meanings. Label-only: 3 of 7 under `specific`, 2 of 7 under `carried`. The tests assert these.

**What would count as informative.** (a) Readers agree with each other on a meaning but not with the key: the key's derivation for that list needs a second look, and the pair is not evidence about the first reading. (b) Readers split on a meaning while agreeing with each other across the other: that meaning is still underdetermined by the sources. (c) A reader agrees with the key on `carried` and not `specific`, or the reverse: the split mattered. Anything else is reported as it comes. No threshold is set; the unit here is 7 pairs and 15 terms, and a count alone cannot carry a claim.

**Variants.** Variant A is the brief as written. Variant B (`variants/READER_BRIEF.v2.variant_B.md`) removes the clause "even if the second system attaches different extra fields or detail", as in v1. Both stay in the design. Readers of v1 cannot be reused for v2 and should not be given v2.

**Hashes.** `key_v2.json` sha256 `c88a910a03a6456900efabd130c57a19f1a0133c9566ebce34ae0b6e813b18d1`; `make_packet_v2.py` sha256 `37e0dd55c76231359c4060ef8f3a703cf5865eefa63bd1ca9fe18f04c4923e48`; v1 key sha256 `5c1a6caba4e3b0f1bc7d1a93b8e2503158e343a67d58fae5c77fe91a710a500b` (unchanged).

## Key v2, amendment 1 (added 2026-11-19, before any further reading)

The owner decided the content of amendment 1 in their own words on 2026-11-19 at 09:31 Central (recorded verbatim in `KEY_V2_AMENDMENT_1.md`, section 1). The text was drafted by Manus. Manus is not independent of the key: the rule it applies was written after the one filed v2 reading (Claude-v2-A) had been scored, and Manus ran the scorer on that reading under the new key once, to check that the scorer works, before committing the text; no list or rule was changed after that run.

What changes: four `slots_specific` lists (T08, T09, T10, T12), the scoring rules N1 and C1 (named in the key, so key v2 output is byte-identical), and a statement about how the carried lists were derived. What does not: the brief, the packet, the clusters, `slots_carried`, `key_v2.json`, every filed reading and score. v2 readers stay poolable.

Pinned (sha256 of the files at commit `1c45e1e`):

| file | sha256 |
|---|---|
| `KEY_V2_AMENDMENT_1.md` | `2f881227942f06322b122a1890b4c5d814ab635e9eaf93adf36832dcd29baf74` |
| `scoring/key_v2_a1.json` | `a7309046319e62210018dd3c48c88174abf63282200c8bb0a40a1c698b5d8ba4` |
| `scoring/score_v2.py` | `22055614cac916e0970c7a8061bb305099289e8f48c647601c3048a0d347c426` |
| `scoring/key_v2.json` (unchanged) | `c88a910a03a6456900efabd130c57a19f1a0133c9566ebce34ae0b6e813b18d1` |
| `build/make_key_a1.py` | `5c01a8fa50e34f0848ff895bae581e9834c9c5955c28577c56938ba36adaffad` |

Every v2 reading read before this section is scored under key v2 and under key a1, and both scores are filed. A reader of another family reads only after this section is merged, and reads the v2 packet unchanged. Readings from before packet v2 (one slot list) are not scored by `score_v2.py`.

---

## Study M01, slots_specific membership (added 2026-11-19, before any M01 coding exists)

Owner: "Yes please" (2026-11-19) to building the M01 instrumentation: a schema, criteria, a script that fills the source half, then coding of the filed readings. This section records the first two before the third and fourth exist.

**Criteria.** `studies/M01_CRITERIA.md`, sha256 `f194ecbcd991720b0ee1279531f5422035b6035505198aab63df0d58b2a5c467`. **Schema.** `studies/M01_SCHEMA.json`, sha256 `2e63b53a5085bed70b940a3232a10d144a93601f2e1ef8dcfb4612e9435a0f40`.

**What M01 is.** A descriptive table of the three filed v2 readings' `slots_specific` choices, one record per reader, term and field, with every value's provenance marked (SCRIPT_DERIVED / CODER_INFERRED / READER_STATED / NOT_RECORDED) and no default anywhere. It is not a test of any hypothesis: the coder has seen all three readings. It changes no brief, packet, key, score, status or reading. Readings taken after this section can be coded the same way.
