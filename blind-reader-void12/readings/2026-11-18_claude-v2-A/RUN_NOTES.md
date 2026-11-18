# Run notes: Claude-v2-A (2026-11-18)

**Filed against packet v2 and key v2. Status `UNCERTAIN`: not counted. A Claude reader counts with the first reader as one family in any case (PREREG rule 5).** This is the second Claude reading to come from a Claude Code cloud session with another of the owner's repositories attached, so neither Claude reading is a clean blind one.

| fact | value |
|---|---|
| packet / brief | v2. The reader's label ends in "A" but the variant was not stated; to be confirmed by the owner. |
| raw output | `raw_output.txt`, 23817 bytes, sha256 `c86f2211d110ec9b8f6e4c1abb37fc77c75bdcc4145d5b2c77f310b8fcb5d95a`; `response.json` is the same bytes. Delivered as a pasted text file. |
| validation | passed |
| blindness | **UNCERTAIN** (q1 no, q2 no, q3 unsure, q4 no); q5 `unsure`, q6 `yes` |
| grouping | 7 of the key's 9 groups reproduced; ARI 0.823; both-join 5, reader-only 1, key-only 1 |
| `slots_specific` | 4 of 7 determined pairs agree; 7 of 14 determined slot sets equal the key's |
| `slots_carried` | 5 of 7 determined pairs agree; 2 of 14 determined slot sets equal the key's |
| references (hand-worked) | nothing grouped 2 of 7 under both; label-only 3 of 7 (`specific`), 2 of 7 (`carried`) |

## What the reader says about its session (its words, condensed)

It could not start a fresh conversation. It worked inside an existing Claude Code cloud session with another repository of the owner's attached and checked out, and that repository's project instruction file loaded into its context automatically. The file names the Simulators project as a sibling and describes its own state vocabulary, and contains no pair table, cluster count or predicates for these terms. It says it did not consult it. Tools on: shell, file tools, sub-agents, web search and GitHub tools (the last two unused). It answered q3 `unsure`, q5 `unsure`, q6 `yes`. These are its claims; we have not checked them.

## Reading the result

**Grouping is identical to the other Claude reading, in the same place.** `HOLDS` goes with `OK` instead of with `CLOSED_WITHIN` (LOW confidence, `CLOSED_WITHIN` named as the alternative). Both readings are the same model family, taken in the same kind of session, so this is one family's reading twice, not two independent readings. It does not confirm the disagreement and it does not retire it.

**The two slot meanings behave differently, and the carried list shows a gap in the brief.** Under `slots_carried`, 2 of 14 determined sets equal the key's. Of the 12 that differ, 11 are the key's list plus extra names (the other is T02, where the reader wrote `[]` for carried and the key has the one notation name). The extras are one level up from the record the key stopped at: the `check_all` wrapper (`tool`, `input`, `counts`, `proposals`, `records`), the demonstration table's row fields in `closure.py` (`case`, `m`, `tol`, `branches`, `split`, ...), the report wrapper in `unified_audit.py`, and the register's row tuples. The brief says "every named field of every record the source builds ... when this term is reported" and says a wrapper that only carries the term counts. It does not say how many levels. The key took one level; this reader took the wrappers it found. Adding the extras to the key now would be fitting the key to a reader, so we have not.

**Four places where the key itself may be the problem** (not changed; see the key issues below):

1. `GAP_INSTRUMENT_CRASH` `slots_specific`. The key lists all six coverage-entry fields. But the `UNKNOWN` coverage entries (`unified_audit.py` 345-355) carry five of those six, so by the brief's own wording ("tied to this term and to no other") only `missing_path` qualifies, plus the section record `error` / `exception_type` / `missing_path` that the reader gave (479-492). The key applied its rule differently here than for other terms.
2. `taf:UNKNOWN` `slots_specific` is `[]` in the key. The glossary row attaches `expiry_condition` and `expiry_source` to an UNKNOWN slot, and this reader and `claude-fresh-1` both listed them. The key's reason (the glossary names no fields for UNKNOWN itself) is a judgement.
3. `ABSENT_AT_SENSITIVITY` (T02): the key spells the notation parameter `value`; both Claude readings wrote `<value>`, as the glossary does. The scorer counts that as a miss on a spelling.
4. `covers_effect` (T05): the key leaves it out of `specific` because it is derived, not a parameter; the reader put it in because the code sets it on this token only.

**What looks like reader reasoning worth keeping.** The reader put nested keys of the bisection and subbox records (`straddle_at_depth_limit`, `undecided_at_depth_limit`) in `specific` for `UNDECIDED` and said it was unsure. It noted the source uses `UNDECIDED` in two senses (a point straddling the tolerance edge; an intersection whose subboxes are still undecided at the depth limit) and said it used the point sense. It noted `HOLDS` appears only on point records (intersections use `BOTH_HOLD`).

**One source claim, checked.** The reader says the comment at `unified_audit.py` 113-117 (`ALL_MODULES_GAP_INSTRUMENT_CRASH` "not reachable on this branch (a raise is RED here)") contradicts `_dispatch` at 479-492, which routes a raise to `GAP_INSTRUMENT_CRASH`. We read both: the comment says what the reader says, and the code does what the reader says. Holds. Other source claims in the reading are not checked.

## Key issues raised by this reading (open; no change made)

`key_v2.json` is as pre-registered. Any change is a dated amendment with its own hash, made so as not to depend on any one reader's answer. Candidate amendments, for the owner to decide: (a) state the depth for `slots_carried` in the brief, in a v2.1, and say which wrappers count; (b) re-derive `slots_specific` for `GAP_INSTRUMENT_CRASH` by the brief's own rule; (c) accept `<value>` and `value` as the same name for T02; (d) decide whether derived attributes count as fields. (a) changes what readers are asked, so a v2.1 reader cannot be pooled with v2 readers; (b) to (d) change only the key.
