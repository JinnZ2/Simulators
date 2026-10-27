# PROVENANCE -- archive/crediting-rate/

The build of `crediting-rate/` that the restore commits did NOT pick, moved here
whole so nothing is deleted. No file content was edited in the move: every
file is either the live copy moved with `git mv` (it was only ever this
build's) or the losing parent's blob written byte-for-byte.

source merge      e167a67  (Merge branch 'main' into claude/revision-survival-frame-d8sjfm)
parents           e4f5418 (^1)   4b1f21e (^2)
winning build     e167a67^1  e4f5418 2026-09-23 crediting-rate: ship G_ABSENT, correct the F half of CRD_006/CRD_021
losing build      e167a67^2  4b1f21e 2026-09-28 Merge pull request #97 from JinnZ2/claude/noise-information-four-tools-
pick rule         tools/known_answer.py registers crediting_rate_v2.py::position, present only in ^1. Applied uniformly across the six folders
                  (KNOWN_RED section 13.3): the build whose functions
                  tools/known_answer.py registers; where none, the build
                  the tree's own records point at.
losing suite      test_crediting_v2.py
last state        at its own parent (wtB): 124 checks, 0 failed. In the tree before this move: red, AttributeError: module crediting_rate_v2 has no attribute LANGUAGE_SIDE.

Files (32 moved, 6 written from the parent blob, 15 left in place
because identical in both parents). `blob` is the losing parent's blob id;
`git show e167a67^2:crediting-rate/<file>` reproduces each written file.

| file | losing blob | action | live folder |
|---|---|---|---|
| `CLAIM_TABLE.md` | `7065091f433b` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 46c73d0dd34c (not edited; item 5) |
| `PREDICTION.md` | `65ee6f8bfb88` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `PREDICTION_V2.md` | `5034c3e343c8` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 5b391d7ea273 (not edited; item 5) |
| `README.md` | `ae95600fff4a` | WRITTEN from the parent blob, byte-for-byte | live is the SPLICE, blob 5e68d313b56f (not edited; item 5) |
| `WORK_ORDER.md` | `904decae8be8` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `WORK_ORDER_V2.md` | `f88f732751bc` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `branch_set.json` | `4a8e2016ba8e` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob d8ba1128a221 |
| `crediting_rate.py` | `e92c4d246714` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `crediting_rate_v2.py` | `19177bf3b070` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob cba9cc50cddc |
| `fixtures/README.md` | `a4fcf4224bdc` | WRITTEN from the parent blob, byte-for-byte | live is the winner's blob 8a65ce016e1a |
| `fixtures/codings.etymology.constructed.jsonl` | `e76471b3f406` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `fixtures/codings.null.constructed.jsonl` | `280151b5dbb9` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `fixtures/events.candidates.jsonl` | `ce4847a0b2cf` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `fixtures/events.constructed.jsonl` | `db7f52b5e978` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `fixtures/frame.constructed.json` | `3b89b53fad3f` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `fixtures/v2/f1_etymology.depth.jsonl` | `e0e1c829826e` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f1_etymology.events.jsonl` | `aa2228d0f925` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f1_etymology.frame.json` | `7e7876ad92f8` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f1_etymology.mechanical.jsonl` | `3663ade9826a` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f2_contribution.depth.jsonl` | `455e4678f914` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f2_contribution.events.jsonl` | `15d5376f8ef9` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f2_contribution.frame.json` | `1adee1c53d7b` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f2_contribution.mechanical.jsonl` | `06d0d57262f4` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f3_mixed_side.depth.jsonl` | `e0e1c829826e` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f3_mixed_side.events.jsonl` | `28c31029cd3b` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f3_mixed_side.frame.json` | `89be642ad594` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f3_mixed_side.mechanical.jsonl` | `3663ade9826a` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f4_model_authored.depth.jsonl` | `e0e1c829826e` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f4_model_authored.events.jsonl` | `d2588eb33f7b` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f4_model_authored.frame.json` | `54b8c9174009` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f4_model_authored.mechanical.jsonl` | `3663ade9826a` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f5_antiquity.depth.jsonl` | `97fdd0067573` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f5_antiquity.events.jsonl` | `159ec1e4fdc7` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f5_antiquity.frame.json` | `9ba94973bbd5` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f5_antiquity.mechanical.jsonl` | `e4f4c0767ec7` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f6_domain_specific.depth.jsonl` | `336436a3af45` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f6_domain_specific.events.jsonl` | `14b886a963ad` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f6_domain_specific.frame.json` | `48ffe3e57c33` | MOVED (git mv; live copy was this blob) | absent now |
| `fixtures/v2/f6_domain_specific.mechanical.jsonl` | `cb4376ef2c30` | MOVED (git mv; live copy was this blob) | absent now |
| `frame.json` | `dbc479f043c0` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `make_fixtures_v2.py` | `3c01bcd77709` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/candidates_blocked.sample.txt` | `b52d7e0d4d74` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `samples/etymology_world.sample.txt` | `fb445bda2c4f` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `samples/frame_undeclared.sample.txt` | `77ad145c5341` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `samples/null_world.sample.txt` | `1e40896042b1` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `samples/selftest.sample.txt` | `c790752ef4cf` | LEFT IN PLACE (identical in both parents; shared) | identical |
| `samples/v2_f1_etymology.sample.txt` | `3d8059202a6c` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/v2_f2_contribution.sample.txt` | `efb83e6d243a` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/v2_f3_mixed_side.sample.txt` | `36df937a5da6` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/v2_f4_model_authored.sample.txt` | `2193d37c901b` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/v2_f5_antiquity.sample.txt` | `40462431c7cc` | MOVED (git mv; live copy was this blob) | absent now |
| `samples/v2_f6_domain_specific.sample.txt` | `a577407f322d` | MOVED (git mv; live copy was this blob) | absent now |
| `test_crediting_v2.py` | `8bec22b7e763` | MOVED (git mv; live copy was this blob) | absent now |

Running this build here is `tests/test_archive_expected_red.py`'s job: its
state is DECLARED there and a change in either direction fails that test.
The live folder now carries one build. The spliced `.md`/LICENSE files in
the live folder are listed in KNOWN_RED section 14.5 and not edited.
