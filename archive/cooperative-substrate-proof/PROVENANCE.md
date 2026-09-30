# PROVENANCE -- archive/cooperative-substrate-proof/

The build of `cooperative-substrate-proof/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      e167a67  (Merge branch 'main' into claude/revision-survival-frame-d8sjfm)
parents           e4f5418 (^1)   4b1f21e (^2)
winning build     e167a67^1  e4f5418 2026-09-23 crediting-rate: ship G_ABSENT, correct the F half of CRD_006/CRD_021
losing build      e167a67^2  4b1f21e 2026-09-28 Merge pull request #97 from JinnZ2/claude/noise-information-four-tools-
pick rule         tools/known_answer.py registers p3_comprehension.py::gain_from_sizes and p5_lag.py::lag_ratio, present only in ^1. Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      selftest.py
last state        at its own parent (wtB): FAILED on two of its own checks (test_proof.py under 300 lines; test_proof.py refuses --selftest) -- checks it makes about the OTHER build's file. In the tree before this move: red, AttributeError: module scope has no attribute code_case.

Files (7 moved, 8 written from the parent blob, 0 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show e167a67^2:cooperative-substrate-proof/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `CLAIM_TABLE.md` | `1c947f0df17d` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob c051bc3f1790 (not edited; item 5) |
| `DISPATCH.md` | `7e08e9890b5c` | MOVED (git mv; live copy was this blob) | absent now |
| `LICENSE` | `0e259d42c996` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob f804fd5ee0d4 (not edited; item 5) |
| `README.md` | `cf2c87a2e748` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob fe2d61a9d793 (not edited; item 5) |
| `fixtures/methods_CONSTRUCTED.txt` | `5fe253a5898d` | MOVED (git mv; live copy was this blob) | absent now |
| `p1_dependency_records.py` | `293b8f3f6eff` | MOVED (git mv; live copy was this blob) | absent now |
| `p2_substrate.py` | `6bce98e80848` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob a10d0f07c5ae |
| `p3_comprehension.py` | `62382f7fce9c` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 94076d8da908 |
| `p4_goal_coherence.py` | `6a7b49928b96` | MOVED (git mv; live copy was this blob) | absent now |
| `p5_lag_declaration.py` | `ac59419ac554` | MOVED (git mv; live copy was this blob) | absent now |
| `run_all.py` | `34db434da232` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 044d479129c1 |
| `samples/run_all.sample.txt` | `460d64b5e92a` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 23db6235f1ab (not edited; item 5) |
| `samples/selftest.sample.txt` | `d5d1f2631d52` | MOVED (git mv; live copy was this blob) | absent now |
| `scope.py` | `97f5977dc2ca` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 4ffbc3391a06 |
| `selftest.py` | `c79feba3a8cd` | MOVED (git mv; live copy was this blob) | absent now |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
