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
- Not checked by us: the reader says the spec's three items for the absence token bundle `limit` and its basis (code needs four), that the glossary's three expiry items become four keys in the register (`provenance` added), and that the spec lists `inputs` on the crash record while `reading()` carries none.
