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

