# PROVENANCE -- archive/assessor-coupling/

The build of `assessor-coupling/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      b57c625  (Merge branch 'main' into claude/revision-survival-frame-d8sjfm)
parents           209af6d (^1)   d23741d (^2)
winning build     b57c625^1  209af6d 2026-09-22 instrument-index: rebuild the index builder from the recovered design
losing build      b57c625^2  d23741d 2026-09-23 Merge pull request #90 from JinnZ2/claude/claude-md-repo-audit-skng5x
pick rule         tools/known_answer.py registers conditions.py::pool_fraction, present only in ^1. Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      selftest.py
last state        at its own parent (scratch worktree wtB, losing blobs in place): 72 checks, 1 FAIL (its own WO-4/WO-5 named-and-absent check). In the tree before this move: red, OSError from reading the other build's conditions.py.

Files (7 moved, 4 written from the parent blob, 1 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show b57c625^2:assessor-coupling/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `CLAIM_TABLE.md` | `76a8565a4cdc` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 77664cffc448 (not edited; item 5) |
| `LICENSE` | `0e259d42c996` | MOVED (git mv; live copy was this blob) | absent now |
| `README.md` | `8764b6cf06c1` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 7f4bb82a49c3 (not edited; item 5) |
| `WORK_ORDER.md` | `68c9675a17a9` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `conditions.py` | `e85ca76a5011` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 6df434d3a3ec |
| `disclosure_audit.py` | `c715428d8197` | MOVED (git mv; live copy was this blob) | absent now |
| `pool_metric.py` | `c2749db62075` | MOVED (git mv; live copy was this blob) | absent now |
| `precedent.py` | `6f3d7b2dd905` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 906af594dbaa |
| `run_all.py` | `a9ed699e5949` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/run_all.sample.txt` | `80123fc12bec` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/selftest.sample.txt` | `e1dbbfa03d9a` | MOVED (git mv; live copy was this blob) | absent now |
| `selftest.py` | `5ae699a70a94` | MOVED (git mv; live copy was this blob) | absent now |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
