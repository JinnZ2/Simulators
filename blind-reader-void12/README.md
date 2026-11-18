# blind-reader-void12

A packet and a scorer for a blind second reading of the vocabulary mapping that section 9c of `playground-crossrun/COMBINED_SPEC.md` calls VOID-12. CC0 1.0 Universal, like the rest of the repository.

The first reading (`combined-playground/cplay/vocab_branches.py`) gives 15 terms from three projects a one-sentence predicate each, and sorts eight pairs into MAPS, PARTIAL, HOMONYM or NONE from those sentences. One reader wrote all the predicates. This folder lets a second reader do the grouping without seeing them, and counts where the two agree. It decides nothing.

| Path | What it is |
|---|---|
| `PREREG.md` | what is compared, the blindness rule, what is reported, proposed reading rules, known limits, hashes. Fixed before any reading. |
| `PROTOCOL.md` | how to choose a reader, what to hand over, what to file afterwards |
| `reader_packet/` | the only thing a reader sees: brief, 15 definitions in shuffled order under neutral ids, pinned sources, response template, manifest |
| `scoring/key.json` | the first reader's predicates, slots and tiers, keyed by the neutral ids. Not for readers. |
| `scoring/score.py` | validates a response and reports agreement; no pass or fail |
| `scoring/test_score.py` | 15 tests: key and packet counts, packet holds none of the first reader's vocabulary, manifest hashes, hand-worked baselines, scorer behaviour |
| `build/make_packet_and_key.py` | rebuilds the packet and key from the first reader's module and the pinned commits; checks each source's sha256 against the module's own pin |
| `readings/` | filed readings (none yet) |

Run the tests from `scoring/`: `python3 -m unittest test_score`. Python 3 standard library only.

What the packet leaves out: every predicate sentence, tier name and branch name from the first reading; the section of the spec from 9c onward (where VOID-12 is discussed); any count of groups or pairs. What it keeps: each definition as quoted, the file it comes from at its pinned commit, byte for byte.

Blindness here is declared by the reader, not enforced, because the first reading is public. See `PREREG.md`.
