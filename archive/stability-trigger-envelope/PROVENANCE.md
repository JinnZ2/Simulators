# PROVENANCE -- archive/stability-trigger-envelope/

The build of `stability-trigger-envelope/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      803ffd5  (Merge branch 'main' into claude/noise-information-four-tools-5u0l4k)
parents           038a30f (^1)   0c6f40e (^2)
winning build     803ffd5^2  0c6f40e 2026-09-28 Merge pull request #96 from JinnZ2/claude/coupling-check-disaster-twikl
losing build      803ffd5^1  038a30f 2026-09-26 Land DISPATCH ESP-1: stability-trigger-envelope/
pick rule         no registry name; the tree's records point at ^2 (samples/descent_record.sample.txt byte-identical to ^2, STE_011's X6 only in ^2's module, root CLAUDE.md '49/49' is ^2's suite count). Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      test_envelope.py
last state        at its own parent (wtB): 217 checks, 0 failed. In the tree before this move: red, ImportError: cannot import name descent_record. (This merge is a CONFLICT, not both-added: one base bc2b315, ^1 is the 038a30f rewrite RIN_051 records as a second build.)

Files (6 moved, 5 written from the parent blob, 2 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show 803ffd5^1:stability-trigger-envelope/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `CLAIM_TABLE.md` | `3d848ed51eea` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 5464bbd514d0 (not edited; item 5) |
| `README.md` | `e2c7a50598cc` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 0698239596fc (not edited; item 5) |
| `RUN_NOTE.md` | `a029ea25fbbf` | MOVED (git mv; live copy was this blob) | absent now |
| `TESTS.md` | `3b26cbf13ef3` | MOVED (git mv; live copy was this blob) | absent now |
| `WORK_ORDER.md` | `56d717ed37bd` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 56d717ed37bd (not edited; item 5) |
| `cases.py` | `397258b1a50e` | MOVED (git mv; live copy was this blob) | absent now |
| `descent_record.py` | `53b62df5718e` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 14a4b4665b5f |
| `samples/descent_record.sample.txt` | `a7740356f9b6` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob b9ff041103f2 |
| `test_descent_record.py` | `6bff32afbeb4` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `test_envelope.py` | `65cdca1616e2` | MOVED (git mv; live copy was this blob) | absent now |
| `threshold_chain.txt` | `3d0decf3421a` | MOVED (git mv; live copy was this blob) | absent now |
| `thresholds.json` | `0e8ab9448c75` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `thresholds.txt` | `0311074459ad` | MOVED (git mv; live copy was this blob) | absent now |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
