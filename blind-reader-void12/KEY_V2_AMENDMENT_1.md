# Key v2, amendment 1 (a1)

Drafted 2026-11-19 by Manus, from decisions the owner wrote in their own words. This text replaces the received drafts (`amendment_options/as_received/`) and the patch revisions that were relayed from another session; nothing in those is adopted unless it appears below. Status: proposed, on a branch, not merged. It takes effect when the owner has read it, it is merged, and its sha256 is recorded in `PREREG.md` before any further reading.

## 1. What the owner decided, and how it is recorded

The owner's message of 2026-11-19, 09:31 Central, verbatim:

> Yes please. Q1 Reading. Q2 undetermined, packet unchanged. Q3 accept the corrected K1 wording. Q4 yes.

It answers four questions that were put to the owner in this thread. Recorded as:

| question | owner's answer | effect in this amendment |
|---|---|---|
| Q1 what is "the instance" of `cplay:CRASHED` | the Reading (the Reading with status CRASHED) | T08 `slots_specific` becomes `[exception, path]` (section 3) |
| Q2 what is "the instance" of `taf:UNKNOWN` | undetermined; packet unchanged | T09 `slots_specific` becomes undetermined (n/d); no file is added to the packet |
| Q3 the replacement wording for K1 | accepted, with the correction that numcheck and TAF lists were read from source text | the statement in section 5 |
| Q4 the rule, N1, C1 and ND | "yes" | adopted (sections 2 and 4) |

One ambiguity, recorded rather than resolved silently: Q4 had been put as "do you object?", and "yes" read literally could mean "I object". It is recorded as "adopt" because the owner's other four answers adopt, the same reply had been proposed in the thread as the adopting reply, and the owner wrote "Yes please" first. If that reading is wrong, the owner says so and sections 2 and 4 are withdrawn; section 3's T08 and T09 entries do not depend on Q4.

Lines in earlier messages that were drafted by another session ("OWNER: ..." lines, items S1, S2, ND, N1, C1, K1 as first worded, R-a, R-b, the T10 list of revision 1, and the remark "two routes agree") are not decisions and are not used here, except that N1, C1 and ND are now adopted by the owner's Q4 answer above, in the wording of section 4.

## 2. The rule for `slots_specific`

A field is a slot of a term when:

- TAG: it is defined on every instance of the term and on no instance of any other term; and
- INDEPENDENCE: it is an independent input of the term's record, that is, not computed from other candidate fields (it is passed in or recorded raw).

It is applied the same way to all 15 terms by `amendment_options/derive/derive_specific.py` from the packet's sources, with INDEPENDENCE tested on every route (cplay constructors by running them, the TAF section record on a corpus of 13 exceptions, numcheck records on a corpus of 13 records). Evidence for adopting it, with the criteria fixed before the checks were run: `amendment_options/decide/DECISION_EVIDENCE.md`. Limits stated there stay in force: the rule was written after the first reading and its score had been seen; A5 and A6 are weaker checks than A1 to A4; independence on the TAF record is empirical on 13 exceptions.

The two owner rulings of section 1 settle the two terms on which the sources give two routes.

## 3. What changes in the key

`scoring/key_v2_a1.json` is built by `build/make_key_a1.py` from `scoring/key_v2.json`, the rule and the two rulings. The script stops if any list other than these four would move.

| id | term | key v2 `slots_specific` | key a1 `slots_specific` | why |
|---|---|---|---|---|
| T08 | cplay:CRASHED | n/d | `[exception, path]` | Q1: the instance is the Reading; the fields a rule requires for CRASHED and for no other status (axes.py 59-60; COMBINED_SPEC line 53) |
| T09 | taf:UNKNOWN | `[]` | n/d | Q2: the glossary defines the term as a slot, the code builds a coverage entry; the sources do not fix the instance |
| T10 | taf:GAP_INSTRUMENT_CRASH | `[kind, module, input, reason, missing_path, expiry_condition]` | `[missing_path, error]` | the rule on the section record built in the one handler that assigns the GAP status; `exception_type` is a function of `error` (unified_audit.py 486-488) and drops out |
| T12 | cplay:UNKNOWN | `[reason, triggers]` | `[triggers]` | the rule: `reason` is required by every non-verdict token, so it is not this term's alone |

The other 11 `slots_specific` lists are unchanged, as is every cluster, label, `slots_carried` list and the pair list. The `key_tier_specific` of the two pairs that contain a changed list is recomputed from the lists (T10|T08 becomes PARTIAL, T09|T12 becomes n/d). `key_v2.json` is not modified.

## 4. Scoring rules (`scoring/score_v2.py`)

A key names the rules it uses in `meta.scoring_rules`. `key_v2.json` names none, so its output is byte-identical to before; `key_v2_a1.json` names N1 and C1.

- N1: before comparing slot names, strip one pair of surrounding backticks, then one pair of surrounding `<` `>` (after the existing strip and lowercase). It changes one name in the filed readings (`<value>` becomes `value`; two occurrences, one of them in a v1 reading that `score_v2.py` does not score).
- C1: beside the existing equal / differ count, report per term the set relation of the reader's list to the key's (equal, reader-superset, reader-subset, overlap, disjoint), with the counts. Nothing is combined and no existing number changes.
- ND: a list the sources do not determine is `null` in the key and is scored as "not determined", never as a match or a miss (this is the existing v2 convention; a1 adds T09 to it).

## 5. Statement about how the carried lists were derived

Accepted by the owner (Q3), in the wording the owner accepted:

> The key's slots_carried lists were derived from the record each term's source builds: for cplay terms by running the constructors and taking the record's fields (vars for plain objects, _fields for namedtuples); for numcheck and TAF terms by reading the record's keys in the source. Class attributes are not included. A reader who names a class attribute is scored as having an extra name.

This describes how the key was made. It does not change the brief, which the readers saw and which says "every named field of every record that the source's code or text builds, returns or documents". No `slots_carried` list changes. (The phrase "instance fields, checked by running it" that appears in some of the key's derivation notes was never in the brief; see `decide/DECISION_EVIDENCE.md`.)

## 6. What this amendment does not change, and what it leaves open

Not changed: the reader brief, the packet (v2 readers stay poolable), the grouping key, `slots_carried`, `key_v2.json`, `PREREG.md` except for the dated section that records the hashes, and every filed reading and score.

Left open, for the owner, not decided here:

1. T10 carried versus specific. Key v2's `slots_carried` for T10 is the six keys of the coverage entry. The a1 `slots_specific` for T10 is taken from the section record the same handler builds (`error`, `exception_type`, `missing_path`), so `error` is in specific and not in carried. The scorer does not require specific to be a subset of carried, so nothing mis-scores. But under the brief's wording the section record is also "built when this term is reported", so the v2 carried list for T10 may be short by `error` and `exception_type`. Changing it would change a carried list, which this amendment does not do.
2. T09 derivation note. Key v2's note says the glossary "names no fields" for UNKNOWN; glossary lines 127 and 128 do document `expiry_condition` and `expiry_source` for the slot. That does not change T09's n/d, but the old note is imprecise. a1 appends its own note and leaves the old text.
3. The consequence for the one filed v2 reading is reported in `readings/2026-11-18_claude-v2-A/`, as a second score beside the first. Because the rule was written after that reading had been scored, that reading is not independent evidence that a1 is right; the safeguard is that the amendment is fixed and hashed before any other reader reads.

## 7. Procedure

1. This file, the key, the key builder, the scorer and the tests are committed. 2. The sha256 of this file, of `key_v2_a1.json` and of `score_v2.py` are written into a dated section of `PREREG.md` before any further reading. 3. Every existing v2 reading is scored under key v2 and key a1 and both are filed (one exists: Claude-v2-A). 4. Only after that is the v2 packet sent to another reader, unchanged.

To rebuild the key: `FORMULA_AUDIT_DIR=<formula-audit checkout> python3 build/make_key_a1.py` (it needs a `numcheck/check.py` with the packet's sha256). To test: `python3 -m unittest test_score_v2 test_score test_key_a1` from `scoring/`.
