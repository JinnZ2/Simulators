# Key v2, amendment 1: options and evidence

Status: OPTIONS ONLY. Nothing here is adopted. `key_v2.json` is unchanged, `PREREG.md` is unchanged, no hash is recorded as adopted.
Written 2026-11-18 (UTC afternoon) on branch `manus/key-v2-a1-options-2026-11-18`.

Each statement below carries one of three labels, so the kind of support is visible:

- **SOURCE** a sentence or line in the pinned packet sources or the brief, quoted with file and line.
- **RULE** what the amendment's own text (S1, S2, S3, ND) says, quoted or paraphrased from `KEY_V2_AMENDMENT_1.md`.
- **COMPUTED** something I ran; the script is in `evidence/` and its output is filed beside it.

## 1. What arrived, and what I checked

A git patch (`as_received/KEY_V2_AMENDMENT_1.patch`, 52,419 bytes, sha256 `8ea98d4cd6cc4702b239a626b4f45c54ad1174f209d8a03ce70fe65fa75452bb`), made in a separate Claude Code session. It adds `scoring/KEY_V2_AMENDMENT_1.md`, `scoring/key_v2_a1.json`, scorer rules N1 and C1, tests, and a dated `PREREG.md` section. The earlier draft is filed beside it (`as_received/KEY_V2_AMENDMENT_1_DRAFT.md`).

COMPUTED, in a scratch worktree of `main` (`5ad784b`), nothing committed to the repo:

| check | result |
|---|---|
| `git apply --check` | clean |
| sha256 of the amendment, `key_v2_a1.json`, `key_v2.json` against the values the patch states | all three match |
| `test_score_v2.py` and `test_score.py` after applying | 37 tests OK; the v1 tests OK |
| patched scorer on the filed Claude-v2-A reading under `key_v2.json` | `score.txt` and `score.json` byte-identical to the filed ones (so "v2 scoring unchanged byte for byte" holds) |
| the patch's hand-worked a1 baselines (specific: nothing-grouped 2 of 6, label-only 2 of 6) | agree with my run |
| `key_v2_a1.json` differs from `key_v2.json` | only T09, T10, T12 `slots_specific` and the `UNKNOWN | UNKNOWN` specific tier, as stated |

Three things about the patch that are not about the rules:

1. **Adoption is asserted, not shown here.** The patch's `PREREG.md` section and the amendment's status line say the owner fixed S3 as S3-out and accepted S1, S2, ND, N1, C1, K1. In this thread the owner's last word on it was to make a branch with options. If S3-out was decided somewhere else, this document is evidence for a decision already made; if not, the patch text is ahead of the decision. Either way the PREREG hash block should be written only when the owner says which.
2. **Location.** The owner's instruction was `blind-reader-void12/KEY_V2_AMENDMENT_1.md`. The patch puts it in `scoring/`. The patch's own tests read it from `scoring/`.
3. **The drafter is not independent.** The amendment says so (it was drafted by the Claude-v2-A model after seeing key v2 and its own score). The numbers in section 3 inherit that: one reading, from the model the amendment was written after.

## 2. The open choices

Three choices change the key. Each has a source basis on both sides. The evidence does not decide any of them.

### Choice 1. T14 `cplay:CLOSED_WITHIN`: `[sigma, basis]` or `[]`

- SOURCE `axes.py` 61-63: `raise AxisError("CLOSED_WITHIN needs a numeric sigma >= 0 and a basis (Q2)")`. A rule requires both fields for this status.
- SOURCE brief line 22, for `slots_specific`: examples include "a rule that says this status needs certain fields"; and the same line says "Not fields that every term sharing a record has."
- COMPUTED (`check_rules_output.txt`, part B): `axes.Reading` is a namedtuple with 8 fields, so every status has `sigma` and `basis`; removing either makes `reading()` raise only for CLOSED_WITHIN.
- RULE S1(c) collects `sigma, basis`. RULE S2 removes a collected name "if every other status that shares the same record or constructor also has it or also requires it", and adds "Presence counts, not value: a key present on every record of a kind is shared even when it is None on the other paths."
- COMPUTED: read literally, S2's presence sentence removes `sigma` and `basis` (every Reading has them), giving `[]`. Read as "requires" only, S2 keeps them. The patch keeps them, so it applies the presence sentence to numcheck records (T01, T07, T11) and not to `Reading` (T14). The same inconsistency in the other direction: the requires-only reading would also leave T08's `exception, path` (T08 is n/d anyway).
- The patch's tests derive the lists of T10, T12, T05, T09 and the three numcheck terms from the sources; no test derives T14's list (its test only checks that T14 did not change).

Effect on the filed reading (section 3): with `[]`, the pair `HOLDS | CLOSED_WITHIN` has key tier MAPS (both lists empty) instead of PARTIAL; the reader put the two terms in different clusters (tier NONE), so it disagrees under both and the pair count does not change. One fewer slot set equals the key (T14 was equal, becomes a superset).

Two ways to remove the inconsistency without touching the key: edit S2 to say presence applies to S1(b) and S1(d) names and requirement applies to S1(c) names (the patch's key follows from that text), or change T14 to `[]` (the S2 text as written).

### Choice 2. T01 `fa:UNDECIDED`: `[]` or the 14 fields of the `proposal` record

- SOURCE `check.py` (numcheck), `_identity_candidate`: builds a record with `lhs, rhs, domain, fixed, units, source_check, status, polynomial, proof, proof_attempted, why_not_proved, evidence, human_interest, ai_interest`. COMPUTED: it is set only on an UNDECIDED point record at tolerance 0 with no piece against it; it is `None` on every other record I built (12 records, 7 verdicts), and the top-level key `proposal` itself is on every record.
- RULE S1(b): "a field of a class or record built only on this term's path". The `proposal` record is built only on UNDECIDED's path. Literal S1(b) collects its 14 fields.
- RULE (the patch's table) gives `[]` for T01 because "bisection / subbox keys exist on every record of that kind; S2 removes them." COMPUTED: that holds for the bisection record (identical key set on all four bisected records, whatever the verdict). It does not address `proposal`, whose inner keys are exclusive to UNDECIDED.
- SOURCE brief, carried meaning only: "if a field holds another record, name the field and do not open it." The brief has no such sentence for `slots_specific`. A "nested records are not opened" rule would give `[]`; it is not in the amendment.
- Note that the check's own docstring says the proposal is an add-on: "The check's own verdict is not changed" (`check.py`, header).

Effect: this is the choice that moves the most. With the 14 fields, the pair `UNDECIDED | UNRESOLVED` has key tier PARTIAL (T01 non-empty, T06 empty) instead of MAPS, and the Claude-v2-A tier (PARTIAL) now agrees: pairs agreeing under `specific` go from 3 of 6 to 4 of 6.

### Choice 3. S3: derived attributes out (the patch) or in

- RULE S3-out (the patch): a slot is an input degree of freedom; an attribute computed after construction from the parameters is excluded. S3-in is struck, kept in the text.
- SOURCE `tokens.py` 17-18: "Reading added here: `covers_effect` (limit <= effect size) is reported on a scoped absence. It refuses nothing; the spec requires the fields, not the comparison." The source itself describes `covers_effect` as something reported on this term. That is a sentence a reader could use for S3-in; S3-out answers that it is computed, not an input.
- SOURCE `tokens.py` 87-88: `t.typed` and `t.untyped` are set after the check that at least one typed trigger exists, from `triggers`. They are derived.
- COMPUTED: `vars()` of the objects: T05 has `covers_effect` (plus `state`, `reason`) beyond its parameters; T12 has `typed`, `untyped` (plus `state`).
- A related unlisted ambiguity: `ExpiryTrigger.is_exit = True` is a class attribute (`tokens.py` 67; in `vars(class)`, not in `vars(instance)`); `untyped()` sets it on its own token (line 77). The amendment's K1 says class attributes are not instance fields for `slots_carried`; S3 says "declared class / record fields count" for `slots_specific`. Nothing in the key moves on this (T04 is `[kind, target, condition]` either way), but a reader could list it.

Effect: S3-in changes two lists (T05 `+covers_effect`, T12 `+typed, +untyped`), after which the filed reading's T05 and T12 equal the key.

## 3. How much each choice moves the filed reading

COMPUTED (`evidence/build_candidates.py`, output `evidence/build_candidates_stdout.txt`). One reading, Claude-v2-A; `slots_carried` and grouping are the same under every key (ARI 0.823; carried 5 of 7 determined pairs agree, 2 of 14 slot sets equal). `specific` only:

| key | pairs agree | slot sets equal | T01 | T05 | T12 | T14 |
|---|---|---|---|---|---|---|
| v2 as filed | 4 of 7 | 7 of 14 | differ | differ | differ | equal |
| P: the patch as received | 3 of 6 | 9 of 13 | superset | superset | superset | equal |
| P with T14 `[]` | 3 of 6 | 8 of 13 | superset | superset | superset | superset |
| P with T01 = 14 proposal fields | 4 of 6 | 9 of 13 | disjoint | superset | superset | equal |
| P with both of the above ("literal") | 4 of 6 | 8 of 13 | disjoint | superset | superset | superset |
| P with S3-in | 3 of 6 | 11 of 13 | superset | equal | equal | equal |

("superset" = the reader listed every key name and more; "disjoint" = no name in common. Candidate keys are rebuilt on the patched key, pair tiers recomputed from the term lists with the first reader's tier rule; the builder first reproduces the stored tiers of `key_v2.json` and `key_v2_a1.json` exactly. The candidate key files are not kept in the repo because they are not keys.)

What the table does and does not say:

- Slot sets equal go from 7 of 14 to 9 of 13 under the patch, but pairs agreeing go from 4 of 7 to 3 of 6. The reason is T09: under v2 the pair `UNKNOWN | UNKNOWN` was PARTIAL/PARTIAL (agreed); under the patch it is n/d and drops out. A reading of "the amendment moves the key toward the reader" holds for slot sets and not for pair tiers.
- Choice 2 is worth one pair; choice 3 is worth two slot sets; choice 1 is worth one slot set and no pair. No choice changes grouping.
- None of this shows a choice is right. A candidate that raises agreement for this reader may do so because it follows this reader's habit. The amendment says the same ("a reader from another family is the test"); the table only shows how much the unsettled choices could matter to that test.

## 4. What I would do, labelled as a view

Not evidence. The choices are about what the rule text means, so they can be settled by reading the text, before any further reading is scored.

- Choice 1: the smallest change that makes the amendment consistent with itself is to edit S2 (presence for S1(b)/(d) names, requirement for S1(c) names). That keeps T14 as the patch has it and says why. The alternative, T14 `[]`, follows S2 as written. Both are defensible; picking one in the text before a non-Claude reader is scored is what matters.
- Choice 2: add one sentence to the amendment ("a record held in a field is not opened for `slots_specific`, as for `slots_carried`"), or collect the 14 fields. Without one of them the amendment is silent on a case that flips a pair tier.
- Choice 3: S3-out has a stated reason; the `tokens.py` sentence is a counter-reading. If S3-out stays, record the `tokens.py` 17-18 sentence in the amendment as the considered counter-evidence.
- Procedure: apply the patch, then adopt only after the owner confirms the three choices; write the PREREG hash block in the same commit; score the one filed v2 reading (Claude-v2-A) under both keys and file both scores (step 5 of the amendment's procedure) before the Kimi packet is sent. The fresh-1 and pilot readings were made on the v1 packet and are not v2 readings.

## 5. What this does not cover

- Only the readings filed in this folder were available to score; I scored one under candidate keys (Claude-v2-A). The other Claude reading was made on the v1 packet and is not a v2 reading.
- The `slots_carried` lists, the grouping key and the brief are not examined here beyond the places that touch the three choices.
- I did not run the patch's N1 and C1 on any reading except the one above.

## 6. Decision record, the rule, and the derivation (2026-11-18, after PR #315 merged)

### 6.1 Who decided what

Quoted from the owner, in order, 2026-11-18 (Central time 17:37, 17:53, 17:56):

- "s3 was Claude's proposal"
- "I will Chose on évidence, the closest base to physics, proven mathmatics or has the most proven science behind it…"
- "Yes please, both" (to an offer that read: "If you choose it on that basis, record it as a decision made today. The patch's claim that you fixed it earlier is still unsupported", together with a derivation script)

Recorded on the strength of those replies; the owner can correct this record.

- **S3: out.** Decided by the owner on 2026-11-18 (about 23:57 UTC), on the criterion above, after seeing the evidence in section 6.2. It was not decided earlier: the received patch's statement that the owner had already fixed S3 is not supported, and a PR that only recorded that (#316) is closed in favour of this section.
- **Not decided here:** S1, S2, ND, N1, C1, K1 (the received patch says the owner accepted them as drafted; nothing in this folder shows that), R-a, R-b, and the T10 list of revision 1. No key, scorer, brief, reading or `PREREG.md` is changed by this section.

### 6.2 The rule, as one statement

A field is a slot of a term when (TAG) it is defined on every instance of the term and on no instance of any other term, and (INDEPENDENCE) it is an independent input of the term's record: it is not computed from other candidate fields (it is passed in or recorded raw). This replaces R-a and R-b with one test: R-a's two tests are the same test on two kinds of definedness (a record has the field; a rule requires it), and R-b's question of whose record it is becomes a property of the data (is the field on every instance).

Why this rule, in the owner's terms: INDEPENDENCE is the distinction a measurement model draws between input quantities and the output quantity (a function of the inputs adds no degree of freedom); TAG is the condition that a field's definedness is equivalent to the term (a biconditional). Both are about what the sources contain, not about what any reader wrote.

### 6.3 What the rule gives (`derive/derive_specific.py`, output in `derive/`)

The script reads only the packet's sources (numcheck run on 13 records, the cplay constructors run, the TAF code parsed). It reads no key. Compared afterwards with three keys:

| key | same | differs | undetermined on one side only |
|---|---|---|---|
| key v2 | 12 | 2 (T10, T12) | 1 (T09) |
| the patch as received (first patch's key) | 14 | 1 (T10) | 0 |
| revision 1 | 14 | 1 (T10) | 0 |

- T01 `[]`: the `proposal` record is on one of three UNDECIDED records (exclusive to UNDECIDED, not on every instance).
- T10 `[missing_path, error]`: one assignment of the GAP status, in the handler that builds the section record; nothing returns or assigns it elsewhere (TAG). `exception_type` is dropped by INDEPENDENCE: it is `type(e).__name__` and `error` is `f"{type(e).__name__}: {e}"`, so on a corpus of 13 exceptions `error` determines `exception_type` and not the reverse. `missing_path` is not determined by `error` (the corpus has two exceptions with the same message and different `filename`). No key lists exactly this: key v2 lists six coverage fields, the first patch's key has one name more (`exception_type`) and revision 1 one name fewer (`error`).
- T14 `[sigma, basis]` (required only for CLOSED_WITHIN), T12 `[triggers]`, T05 unchanged (`covers_effect`, `reason` are set by the constructor and are not parameters, so they are computed from them and are not slots; T12's `typed`, `untyped` likewise). The parameters of T03, T04, T05 vary freely (4 of 4, 8 of 8, 32 of 32 combinations of two values accepted); T12 accepts 2 of 4 because an empty `triggers` list is refused (a constraint on a value, not a dependence between fields), T08 and T09 undetermined because their routes disagree.
- Five mutation checks pass: with a corpus where every UNDECIDED record carries a proposal, T01 gets the proposal fields; with the GAP status also returned elsewhere, T10 falls back to `[missing_path]`; with a second status requiring `sigma`, T14 drops it; with `exception_type` made an independent input (`len(e.args)`), T10 gets it back; with `exception_type` computed from `error` by another route, it is dropped. The rule changes its answer when the evidence changes.

### 6.4 Limits

- I wrote the rule after seeing the first patch's key and the candidate scores (`evidence/`). Agreement with the first patch's key on 14 of 15 shows the rule is mechanical and applied the same way to all terms, including T01, where the patch's own text was inconsistent. It does not show the key is right.
- The numcheck lists depend on the 13-record corpus. Adding records can only shrink the "every instance" set and grow the "other terms" set, so the three empty lists are robust; a non-empty list would be an upper bound.
- The independence test on the TAF section record is empirical: a dependence it finds holds on the 13-exception corpus, and an exception class that breaks it would be a counter-example. The corpus was built to break each dependence that is not real (same message, different filename; same message text, different `args`); it cannot prove a dependence in general. For numcheck records there is no independence test, because every numcheck list is empty.
- The T10 result relies on one file. A runner outside `unified_audit.py` that returns the GAP string would break the biconditional; none is in the packet.
- T09's text route is noisy: it picks up `MIXED_UNKNOWN_AND_GAP_INSTRUMENT` (a status label, not a field) beside `expiry_condition`. It differs from the code route (`[]`) either way, so T09 stays undetermined; the script reports the route as found and does not tidy it.
- Whether the brief's word "slot" means an independent coordinate is a definition, not a physical fact. The mathematics says which definitions are coherent; whether readers follow it is a question for readers.

### 6.5 Open

The owner has not yet decided whether to adopt the rule above. Its T10 list (`[missing_path, error]`) is neither the first patch's (`[missing_path, error, exception_type]`) nor revision 1's (`[missing_path]`); the other 14 terms agree with revision 1, and 14 with the first patch's key. If the rule is adopted, the amendment text needs its own edit to say it, drop the sentence that cites the reading's agreement as a reason, and correct the T01 explanation ("every key on it is on every record" is not true of `bisection` and `formula`; `[]` follows from the tag test).

### 6.6 Review finding on the first version of this section (2026-11-18, later the same hour)

A second Claude session, reading PR #317, pointed out that the first version of the script applied INDEPENDENCE only to the cplay constructors (and by a weak test: building each object twice passes for any deterministic constructor). Checked against `unified_audit.py` lines 486-488: correct. `exception_type` is a function of `error`. The script now tests independence on every route (see its docstring), the first version's T10 list `[missing_path, error, exception_type]` was wrong under the rule's own text, and the table and bullets above are corrected. The same session expected `[missing_path, error]` before the script was run; the script gives that result from the sources.

The same message said the owner had written "S3: DECIDED BY THE MEANING OF 'SLOT' -> S3-out" and "THE OTHER RULES: accept as drafted" in an earlier conversation. That message is not in this session's record. It is recorded here as a relayed claim, not as a decision: section 6.1 stands until the owner confirms the other rules in this thread.

Update, 2026-11-18 18:14 Central: the owner wrote in this thread, about those lines, "Yes those were from Claude." So S1, S2, ND, N1, C1 and K1 are recorded as not decided by the owner (drafted by Claude), and section 6.1 stands as written. Each still needs the owner's own yes or no before the amendment text is hashed.

A suggested precedence rule ("only lines marked OWNER are my decisions") was also relayed from Claude, and the owner said so ("So is this"). It is not an owner decision and is not added to `PREREG.md` or `PROTOCOL.md`. If the owner wants it, it takes effect when the owner sends it in a message of their own.

