# PROVENANCE -- archive/chain-position/

The build of `chain-position/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      1a9c09b  (Merge branch 'main' into claude/cooperative-substrate-proof-ybq3nw)
parents           0e77d9a (^1)   d1d3c80 (^2)
winning build     1a9c09b^2  d1d3c80 2026-09-19 Merge pull request #85 from JinnZ2/claude/revision-survival-frame-d8sjf
losing build      1a9c09b^1  0e77d9a 2026-09-19 assessor-coupling: WO-6 built as a self-contained folder
pick rule         tools/known_answer.py registers load_class.py::stability_product, present only in ^2 (the 781fb5d build on main). Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      selftest.py
last state        at its own parent (wtB): 96 checks, 0 failed. In the tree before this move: red, AttributeError: module trust_provenance has no attribute full_record.

Files (8 moved, 5 written from the parent blob, 0 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show 1a9c09b^1:chain-position/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `CLAIM_TABLE.md` | `ea5bd6c0cefc` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob c758ac9175fc (not edited; item 5) |
| `LICENSE` | `0e259d42c996` | MOVED (git mv; live copy was this blob) | absent now |
| `README.md` | `5e7ed5c83039` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 3d96a7400aa4 (not edited; item 5) |
| `WORK_ORDER.md` | `2833271d0fa9` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 1000737539d7 (not edited; item 5) |
| `clause_audit.py` | `283e54e74b96` | MOVED (git mv; live copy was this blob) | absent now |
| `dissimilar.py` | `1e0f838a7ab8` | MOVED (git mv; live copy was this blob) | absent now |
| `horn_b.py` | `0595da56b9d9` | MOVED (git mv; live copy was this blob) | absent now |
| `load_class.py` | `21801dc47110` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 74e928a23022 |
| `run_all.py` | `0149a381b486` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/run_all.sample.txt` | `5eb3f47c6ea7` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/selftest.sample.txt` | `5f6e5204ba8b` | MOVED (git mv; live copy was this blob) | absent now |
| `selftest.py` | `f00eb2639808` | MOVED (git mv; live copy was this blob) | absent now |
| `trust_provenance.py` | `33ce3b2bf0bf` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob bb8ac4dabd1a |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
