# Decision evidence for the rule and for N1, C1, ND, K1

Prepared 2026-11-18 (evening, Central). The criteria are in `CRITERIA.md`, committed as `d7b7687` (sha256 `e3df8f8f18510e36083a3eb7d3ce77046ca94314718162fce9db07c38d1b4c74`) before any check script in this folder existed. The owner's instruction (18:16 Central, the owner's own words): adopt the rule "if the évidence supports the build; then yes", and for N1, C1, ND and K1 "let évidence decide for engineering stability". Nothing here changes a key, scorer, brief, reading or `PREREG.md`. This file recommends; the amendment text is a later step and is the owner's to approve.

## Result in one table

| item | criteria | result | recommendation under the criteria |
|---|---|---|---|
| the rule (tag + independence) | A1 to A6 | all six hold | adopt as the derivation method for `slots_specific` |
| N1 (strip one pair of `<>` and backticks before comparing names) | N-a to N-d | all hold | adopt |
| C1 (report the set relation beside equal / differ) | C-a to C-c | all hold | adopt |
| ND (a list is undetermined when the sources still support two) | D-a to D-c | procedural criteria hold; T08 has 3 lists, T09 has 2 | adopt as a fallback; T08 and T09 are n/d under it |
| K1 ("`slots_carried` means `vars(instance)`") | K-a to K-c | K-a and K-b hold, **K-c fails** | **not adopted as worded**; replacement wording proposed below |

## The rule (`check_rule_stability.py`, output beside it)

The derivation reruns byte-identically (A1). On 600 generated numcheck records (verdicts `VOID` 330, `FAILS` 86, `HOLDS` 64, `UNDECIDED` 52, `ONE_FAILS` 50, `MIXED` 15, `BOTH_HOLD` 3; seed fixed in the script) the lists for T01, T07 and T11 stay empty, and `proposal` is on 21 of 52 `UNDECIDED` records, so it is exclusive but not universal (A2). Removing any one of the 13 exceptions leaves T10 at `[missing_path, error]` (A3); removing a pair changes it in 3 of 78 cases, which are the three pairs among the three same-message exceptions that differ only in `filename` (`p1`, `p2`, none). That is the stated limit: with two of those three gone the corpus cannot show that `error` does not determine `missing_path`. A second filler value and a second, disjoint parameter pool leave every cplay list and every free-variation count unchanged (A4). The derivation functions mention no key, reading or scorer path (A5, a text search of their source). Every route that yields a list from instances has an independence test (A6).

What these results do not show. A5 and A6 are weaker than A1 to A4: A5 is a string search over function source, and A6's route table is written in the script, not discovered by it. T02 (`value`) and T15 (the four expiry keys) come from a notation and a constant and have no dependence test. The criteria were written after the derivation had run, so the derivation results were not blind to the criteria; the stability checks are new runs, not reruns.

## N1 (`check_nck.py`)

N1 makes no two distinct names equal in any of 130 lists (keys v2 and v2-a1, four filed readings) (N-a). It changes exactly one name, `<value>` to `value`, in two readings (Claude-fresh-1 `T02`, a v1 reading not scored by the v2 scorer, and Claude-v2-A `T02` `slots_specific`); the wrapped form is the glossary's own placeholder notation (`ABSENT_AT_SENSITIVITY(<value>)`, glossary line 129) and appears verbatim in the packet sources (N-b). With the patch's scorer and the unchanged key v2, the Claude-v2-A score text and JSON are byte-identical to the filed ones (N-c). Effect (N-d): switching N1 on moves Claude-v2-A's `specific` slot-set agreement from 7 to 8 of the determined terms (T02), with no change to `carried` and no change to any tier. The criterion was harmlessness and source-grounding, not size of effect.

## C1 (`check_nck.py`)

Over all 1,024 ordered pairs of subsets of a five-name universe, exactly one of the five relations is true and it is the one returned (C-a); `equal` coincides with the existing equal flag; the empty set against the empty set is `equal`, the empty set against a non-empty one is `reader-subset`. On Claude-v2-A with C1 on, every existing number is unchanged once the C1 fields are removed, and `relation == equal` exactly when `status == equal` on every determined row (C-b). C1 removes no output key and adds only `relation`, `relations`, `key_version` and `scoring_rules` (C-c). Filed relation counts for Claude-v2-A: `specific` equal 7, reader-superset 4, overlap 2, disjoint 1; `carried` equal 2, reader-superset 11, reader-subset 1.

## ND (`check_nd.py`)

The criteria for ND asked that the rule be applied to the instances themselves, not to the two crude routes in `derive_specific.py`. Done, under every definition of "instance" a source supports.

T08 (`cplay:CRASHED`) gives three lists. If the instance is a Reading with status CRASHED, the list is `[exception, path]` (axes.py 59-60, the two fields required for that status and no other). If it is the pair `crash()` returns, adding the one coverage key exclusive to the GAP kind in the TAF vocabulary gives `[exception, path, missing_path]`, where `crash()` sets `missing_path == path` on all nine probes so the two determine each other. If it is a call of `crash()`, the parameters give `[exc, path, module, inputs, expiry_condition]`, all independent (32 of 32 combinations accepted). The sources do not say which object "CRASHED" names.

T09 (`taf:UNKNOWN`) gives two. As a coverage entry of kind UNKNOWN in code (unified_audit.py 328-376) no key is exclusive, so `[]`. As the slot the glossary documents (lines 126 to 128) the candidate fields are `expiry_condition`, which fails TAG because both other kinds' entries carry it, and `expiry_source`, which no packet code mentions and which is exclusive by documentation only; the file where the glossary says the slot lives (`docs/expiry_register.json`) is not in the packet, so "defined on every instance" cannot be tested. So `[expiry_source]` rests on text alone.

Correction to my earlier statement: I had expected T09 to come out determined as `[]`. It does not, once the documented slot counts as an instance. The earlier glossary route in `derive_specific.py` also listed a status label (`MIXED_UNKNOWN_AND_GAP_INSTRUMENT`) that is not a field; applying the rule removes it. One owner sentence settles each term: which object is "the instance" of CRASHED, and which object is "the instance" of UNKNOWN (and, for the second, whether the packet should include `docs/expiry_register.json`).

## K1 (`check_nck.py`)

K-a holds: for all eight cplay terms, the key's `slots_carried` equals the fields obtained by running the constructors (K1 changes no list). K-b holds: `ExpiryTrigger.is_exit` is a class attribute, not in `vars()` of an instance and not in T04's carried list.

K-c fails, and the failure is in my criterion, not only in K1. I wrote K-c on the premise that the reader brief says "instance fields, checked by running it". It does not: that phrase appears only in key v2's derivation notes for T04, T05 and T12, which readers never saw. The brief's wording for `slots_carried` is "every named field of every record that the source's code or text builds, returns or documents". So K1 is not "the literal reading of the brief's phrase"; it narrows the brief's wording to the key's. Whether a documented class attribute such as `is_exit` is a "named field of the record" is a reading question the brief does not settle.

A finding I did not pre-register (reported as K-0, not counted as a criterion): `vars(instance)` raises `TypeError` for the records behind T06, T08, T13 and T14 (`Reading`, `closure.FieldToken`, `CoverageEntry` are namedtuples). The key's lists for those terms come from `_fields`. So K1's literal wording does not apply to 4 of the 8 cplay terms, though no list changes. And `tokens.untyped()` sets `is_exit` on the instance, so "is_exit is not an instance field" is true of `ExpiryTrigger` and false of an `UNTYPED` Token (no term in the packet is UNTYPED).

Proposed replacement for K1, as a description of how the key was derived, not a claim about the brief: "The key's `slots_carried` lists were derived by running the constructors and taking the record's fields (`vars` for plain objects, `_fields` for namedtuples); class attributes are not included. A reader who names a class attribute (e.g. `is_exit`) is scored as having an extra name, as for any other extra." Under C1 that case shows as `reader-superset`. This is for the owner to accept or change.

## How these checks went wrong once, and were fixed

My first run of `check_nck.py` printed `C-b FAILS` and `K-a FAILS` (T06, T13). Both were bugs in my script, not in the amendment: C-b compared a JSON round-trip against an object holding tuples, and for T06 and T13 I had built plain Tokens where the key means a `FieldToken` and a `Reading` status. A diff of the two score objects showed no change in any number before I corrected the comparison. The output file is from the final run only.

## What this does not decide

Whether "slot" means an independent coordinate is a definition. The criteria do not prefer any existing T10 list; the rule gives `[missing_path, error]`. The wording of the amendment text, and whether the owner accepts any of the five items, are separate steps. S1, S2 and the other relayed lines remain not decided by the owner.
