# Run notes: claude-fresh-1 (2026-11-18)

**Filed against packet v1 and key v1. Status `UNCERTAIN`, so it does not count toward confirming any pair (`PREREG.md`); and by rule 5 a Claude reader would count together with the first reader as one family even if it were `BLIND`.** The label "fresh" was the label the work order asked the reader to write; the reader says the session was not fresh.

| fact | value |
|---|---|
| brief | variant A (as written), v1 packet |
| how it was run | by the owner, in a Claude Code cloud session, with the packet files and the work order text. Details are the reader's own account, below; not independently checked. |
| raw output | `raw_output.txt`, 15041 bytes, sha256 `f2ca48909b7677d3a2e459e591c279b9e6b5508ff2d4d55fff9e8e346bb71edb`; `response.json` is the same bytes. Delivered to us as a pasted text file. |
| validation | passed |
| blindness status by the PREREG rule | **UNCERTAIN** (q1 no, q2 no, q3 unsure, q4 no); q5 `unsure`, q6 `yes` |
| declared pairs | 5 of 8 agree with the key v1 |
| all 105 term pairs | both join 5, reader only 1, key only 1; adjusted Rand index 0.823; 9 groups against the key's 9 |

## What the reader says about its session (its own words, condensed)

The session had shell and file tools, and GitHub access to eight other repositories by the same owner (none of them Simulators, formula-audit or thermodynamic-accountability-framework). Those eight repositories' `CLAUDE.md` files were placed in its context before the task; they mention the sibling Simulators repository, a reading protocol and an audit contract, status vocabularies across layers, and a blind held-out set for a different pilot. It says it did not use them for any grouping or slot, but it read them, so it answered q3 and q5 `unsure` and q6 `yes`. It used no web search and no cross-session memory.

## Where it parts from the first reading

- **Grouping: one real disagreement.** The reader puts `HOLDS` (T11) with the generic pass `OK` (T13) and leaves `CLOSED_WITHIN` (T14) alone. The key, and both pilots, join `HOLDS` with `CLOSED_WITHIN`. The reader marked this LOW confidence and listed T14 as the alternative. Its reason, from `source_lines_read`: "HOLDS has no sigma/noise-band notion and also covers exact agreement, so I put it with the generic pass". This changes two groups: the key has {T11, T14} and {T13}; the reader has {T11, T13} and {T14}. The other 7 of the key's 9 groups are reproduced exactly (both pilots reproduced all 9), including keeping the two `VOID`s apart.
- **Tiers: 5 of 8.** Three differ: `HOLDS | OK` (follows from the grouping), `HOLDS | CLOSED_WITHIN` (same), and `GAP_INSTRUMENT_CRASH | CRASHED`. For the last, this reader listed three fields for `CRASHED` (`exception, path, reason`), so the slot lists differ from the six of `GAP_INSTRUMENT_CRASH`. The pilots listed thirteen. Three readers, three different lists for that term.
- **Slots: 5 of 15 sets equal the key's, and the reader used the word two ways.** For the three numcheck terms (T01, T07, T11) it gave the whole 17-name record. For T08 it gave 3 names, T06 2 (the wrapper record's), T13 2 and T14 2. Pilot A gave 27, 27 and 21 for the numcheck terms, 13 for T08, 0 for T09. The same word, "slots", produced a whole record for some terms and a term's own fields for others, within one reading. This is the pattern that led to packet v2.

## Things the reader noticed that are about the packet or the sources (its claims; the first two we checked, the rest we did not)

- **Packet leak, confirmed and fixed in v2.** `PACKET_MANIFEST.json`'s leak-check note said the branch table was "unrelated to the vocabulary mapping", which tells a reader what the packet is about. v2 drops that phrase.
- **Work-order leak, confirmed and fixed.** The work order's pasted text began with a line pointing at an owner's section that the reader was not shown. The line is replaced and now sits outside the text to be pasted.
- The three source claims in the line above this one were first reported without a check. They are now checked; see the next section.

## Follow-up from the reader, and our check (2026-11-18)

After seeing how it scored, the reader re-checked its own three source claims against the pinned v1 files and sent the result back. As received: `followup_as_received.txt`, 3721 bytes, sha256 `8f91f6eb2e9ec447f1c87bb41e2ffea68231dc79a602491223d4b41076879149`. The reader could not push (read-only clone); the text below is ours, written after we re-read the same lines. Packet files matched `PACKET_MANIFEST.json` when we checked.

| claim | what the pinned files say | our check |
|---|---|---|
| Absence token: the spec says "three things", the code needs four | `COMBINED_SPEC.lines_1-390.md` 129-133: the limit "and how it was established", the effect size, the conditions. `tokens.py` 92-100: `limit`, `basis`, `effect_size`, `conditions` all required, plus `ladder` when `basis == "LADDER"`. | **Holds.** The spec's first item is the limit and its basis together; the code splits it. A difference in count, not a contradiction. |
| Expiry items worded three ways | `glossary.md` 127: "Instrument class, sensitivity or protocol". `expiry_register.py` 5-8: "an instrument class, sensitivity, and protocol", inside a quotation of the Kimi audit. `expiry_register.py` 28-31 and 53: a dict of four keys, `provenance` added, `sensitivity` may be "void". | **Holds as to the wording.** The reader reads the glossary's "or" as "any one of three"; the sentence can also be read as naming the kinds of thing an exit may be, so that reading is the reader's, not stated by the source. The "and" is a quotation of an audit, not the register's own rule. |
| Crash inputs | `COMBINED_SPEC` 85-89 (R-A2): a crash record carries exception type, call path and inputs; the next sentences say the coverage entry carries kind, module, input, reason, missing_path, expiry_condition. `axes.py` 44: `reading()` has no inputs parameter. `axes.py` 78-88: `crash()` returns `(rd, cov)`, a `CRASHED` reading (reason, exception, path) and a `GAP_INSTRUMENT_CRASH` entry (`input=inputs`, `missing_path=path`). | **Holds, with one addition.** `crash()`'s own docstring says "an INSTRUMENT reading plus a coverage entry", so the source states that a crash is a pair. R-A2 is met by the pair. The spec's `inputs` becomes the entry's `input`, and `path` is kept twice (`path` on the reading, `missing_path` on the entry). |

**The reader's reading of why the crash pair differed, and where we stand on it.** The reader says the `CRASHED | GAP_INSTRUMENT_CRASH` tier difference, and three different slot lists for `CRASHED`, come from one event being split over two objects, so comparing their field lists measures the split and not what the terms mean. That fits what we see: this reader listed 3 names (the reading's own), pilot A listed 13 (the union of both objects), and the v1 key listed 6 (the entry's). It is an explanation consistent with those counts. We have not shown it is the only one. It is also the reason `slots_specific` for `CRASHED` is `n/d` in key v2 and its `slots_carried` is the union of both objects. A v2 reader will show whether the split removes the disagreement.

**One transcription note from the reader.** In T04's `source_lines_read`, `__init__` arrived as `init` (the paste dropped the underscores). It has no effect on scoring, and `raw_output.txt` is kept as received.

