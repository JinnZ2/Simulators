# Decision criteria for the rule and for N1, C1, ND, K1

Written 2026-11-18 (after the owner's message of 18:16 Central), BEFORE any of the checks below was run, and committed before the check scripts exist. The owner's instruction: adopt the rule "if the évidence supports the build", and for the other four "let évidence decide for engineering stability".

Meaning of "engineering stability" used here: a rule is adopted only if it (a) is deterministic, (b) does not change any already-filed score or list unless that change is the stated purpose, (c) gives the same answer when the evidence it ran on is perturbed in ways that should not matter, (d) changes its answer when the evidence changes in ways that should matter, and (e) does not depend on one reader or one drafter. A rule that fails a criterion is not adopted as written; the failure is reported and a change is proposed, not applied.

What was already seen before these criteria were written, so the reader can discount it: `derive/derive_specific.py` ran (five mutation checks pass; output identical on rerun; lists compared with three keys); the amendment's text for N1, C1, ND, K1 was read; the filed Claude-v2-A score under key v2 and under the earlier a1 keys was seen. Nothing below was run.

## The rule (tag + independence)

Adopt if ALL hold. Each is measured by `decide/check_rule_stability.py`.

- **A1 determinism**: two runs give byte-identical output. (Already seen: holds.)
- **A2 numcheck corpus stability**: on an enlarged corpus of at least 200 randomly generated numcheck inputs that produce all of HOLDS, FAILS, MIXED, UNDECIDED, VOID, the derived lists for T01, T07, T11 are still `[]`, and `proposal` is still not on every UNDECIDED record. If a non-empty list appears, the rule is not adopted for numcheck terms as written.
- **A3 exception corpus stability**: removing any ONE exception from the 13-exception corpus leaves T10 unchanged. Removing a pair that contains both exceptions that break `error -> missing_path` is expected to change it; that pair is reported by name and is a stated limit, not a failure.
- **A4 constructor stability**: every cplay list (T03, T04, T05, T12, T14) is unchanged when the parameter value pools used to probe the constructors are replaced by a second, disjoint pool.
- **A5 no reader dependence**: the script reads no key and no reading. (Checked by reading the script: it opens no file under `scoring/` or `readings/` except through the `COMPARE` option, which is applied after derivation.)
- **A6 coverage of "every route"**: the independence test is applied on each of the routes that yield a non-empty list (cplay constructors, TAF section record, TAF coverage entries, Reading requirement table). Where a route has no test, the script says so.

If A2, A3 or A4 fails, the rule is not adopted as written. If A1, A5, A6 fail, likewise.

## N1 (strip one pair of surrounding `<` `>` and surrounding backticks before comparing names)

Adopt if ALL hold:

- **N-a** across every key list and every filed reader list (all filed v2 readings), N1 causes zero collisions: no two distinct names in one list become equal.
- **N-b** across the same, every name N1 changes is changed only by removal of the wrapper, and the wrapper form appears in a packet source as notation for a placeholder (not as part of a name).
- **N-c** applied only when the key names N1 (as the patch does), scoring against `key_v2.json` stays byte-identical to the filed `score.txt` and `score.json`.
- **N-d** the number of names in the filed readings that N1 changes is reported, with which readings and which terms; N1 is adopted even if that number is 1, because the criterion is harmlessness and source-grounding, not effect size.

## C1 (report the set relation beside equal / differ)

Adopt if ALL hold:

- **C-a** over every pair of subsets of a 5-name universe (1,024 ordered pairs) the five relations (equal, reader-superset, reader-subset, overlap, disjoint) are exhaustive and mutually exclusive, and `equal` coincides with the existing equal flag.
- **C-b** on every determined list pair in the filed Claude-v2-A score, the C1 relation is consistent with the existing flag (equal iff `equal`), and the existing numbers are unchanged.
- **C-c** C1 adds no combined score and removes no existing column.

## ND (if the sources still support two different lists after the rule, the list is undetermined)

ND is adopted only if its use is shown to be about the sources and not about the script's route choices. Measured by `decide/check_nd.py`:

- **D-a** for T08 and T09, the rule is applied to the instances themselves (what `crash()` builds, what the TAF coverage entries and register entries carry), not only to the two crude routes in `derive_specific.py`. The routes in that script were chosen by me and the glossary route for T09 is known to be noisy; they are not evidence of ambiguity by themselves.
- **D-b** if the proper application determines the list, ND is not needed for that term, and the key and the script should say the determined list. If two different lists still remain, with both derivations printed and each backed by a source line, ND stands for that term.
- **D-c** ND is adopted as a rule (a stated fallback, which PREREG v2 already defines as n/d) either way; what is decided is whether T08 and T09 are n/d under it.

## K1 (`slots_carried` means vars(instance); class attributes are not instance fields)

Adopt if ALL hold:

- **K-a** for every cplay term, the carried list in the key equals the set of instance fields obtained by running the constructor (vars(instance)), and K1 changes no list.
- **K-b** the one class attribute known (`ExpiryTrigger.is_exit`) is not in vars of a constructed trigger, and is not in the carried lists of T04.
- **K-c** the brief's own phrase is "instance fields, checked by running it", and K1 is the literal reading of that phrase.

If K-a fails, K1 is not adopted as a clarification; the failing list is reported.

## What this does not decide

- Whether "slot" means an independent coordinate (a definition).
- T10's list is whatever the script gives; the criteria do not prefer any existing key's T10.
- The wording of the amendment text, which is a separate step after this one.
