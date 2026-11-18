# Running a blind reader

For whoever carries the packet to a reader. Nothing here needs the first reading, and the reader must not be shown it.

## Choosing a reader

A reader is useful for this test when it has not seen the first reader's predicates or the table of tiers, and when it is as unlike the first reader as you can arrange. In order of usefulness:

1. A person who works in measurement, audit or software quality and has not read these repositories.
2. A model from a different family than the first reader, started fresh, with no memory, no files from these projects, and no web access if the tool allows turning it off.
3. A fresh session of the same family as the first reader. It can be filed, but under rule 5 of `PREREG.md` it counts together with the first reader as one family, so it cannot confirm a pair by itself.

Two readers already know too much: the second reader whose notes are in `second-reader-kimi-k3/` was given the first reader's table (its notes say so), and the session that built this packet has seen the key. Neither can be a `BLIND` reader. Anyone who has read this repository's log of VOID-12 should answer `yes` to q3.

## What to hand over

Only the contents of `reader_packet/`, as a zip or folder. Not `scoring/`, not `PREREG.md`, not this file, not the repository link. The packet's `PACKET_MANIFEST.json` lists every file's hash; give the reader the manifest too, so a changed file shows.

Say nothing beyond: "Read READER_BRIEF.md and follow it. Return only the filled response file." Do not say how many groups to expect, which terms are thought to match, or that there is a first reading. If the reader asks, tell it to put the question and your answer in `attestation.notes`, and record that you answered.

## While it runs

For a model reader, note and file with the response: whether web access was on, whether file tools were on, what the system prompt was if you wrote one, and the model name and version if the tool shows it. For a human reader, note how long it took and whether they used other sources. None of this changes the status rule; it is context for whoever reads the result.

Do not retry a reader to get a "cleaner" answer. If a reader fails to return valid JSON, file what it returned. A second try is a second reading, with its own attestation (q6 will be `yes` or `unsure` for a model that remembers the first try).

## After it returns

1. Save the response unchanged as `readings/<date>_<reader_label>/response.json` together with a `RUN_NOTES.md` holding the facts above. Compute and record its sha256.
2. `python3 scoring/score.py readings/<date>_<reader_label>/response.json --json readings/<date>_<reader_label>/score.json > readings/<date>_<reader_label>/score.txt`
3. For every declared pair that differs, put the first reader's predicate sentence and the blind reader's beside each other in `RUN_NOTES.md`, quoted from their sources.
4. File the reading whatever it shows. A reading that agrees on 8 of 8, one that agrees on 2 of 8, and one that fails validation all go in.
5. Anything that changes the log in `COMBINED_SPEC.md` is a separate, additive pull request for the owner. Nothing in this folder edits the spec.

## Anonymity

Reader labels may be a code. The response asks for `model_family`, which for a person is `human`. The packet and the scorer hold no names, addresses or paths.

## If the key is ever rebuilt

`scoring/test_score.py` fails if `vocab_branches.py` changes after the key was built. Rebuild with `build/make_packet_and_key.py` (usage in its header), say in a dated section of `PREREG.md` what changed in the first reading and why, and treat any reading taken against the old packet as filed against the old key.

## For packet v2

Give the reader `reader_packet_v2/` (zip below) and the brief in it; nothing else. Use `scoring/score_v2.py`, not `score.py`. Everything else in this protocol is unchanged. A response in the v1 shape (`slots`, `slots_basis`) is refused by `score_v2.py` and is not silently scored.
