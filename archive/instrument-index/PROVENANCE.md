# PROVENANCE -- archive/instrument-index/

The build of `instrument-index/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      b57c625  (Merge branch 'main' into claude/revision-survival-frame-d8sjfm)
parents           209af6d (^1)   d23741d (^2)
winning build     b57c625^1  209af6d 2026-09-22 instrument-index: rebuild the index builder from the recovered design
losing build      b57c625^2  d23741d 2026-09-23 Merge pull request #90 from JinnZ2/claude/claude-md-repo-audit-skng5x
pick rule         tools/known_answer.py registers build_index.py::claim_only_fraction, present only in ^1; ^1 carries tests/, CLAIM_TABLE.md, README.md. Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      (none -- this build ships no suite)
last state        ^2 ships no test file. Its build_index.py imported nothing that fails; nothing here runs it.

Files (4 moved, 2 written from the parent blob, 0 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show b57c625^2:instrument-index/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `INDEX-SPEC.md` | `f3b421255943` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob aabaefada56b (not edited; item 5) |
| `INSTRUMENT-INDEX.tsv` | `f7794a09aed3` | MOVED (git mv; live copy was this blob) | absent now |
| `STATE.md` | `c98d0284d71d` | MOVED (git mv; live copy was this blob) | absent now |
| `build_index.py` | `80e8086417ac` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob b4dc64c6a1d9 |
| `coverage.py` | `2d39fbb49d8c` | MOVED (git mv; live copy was this blob) | absent now |
| `index-overrides.json` | `6d4519ccea8c` | MOVED (git mv; live copy was this blob) | absent now |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
