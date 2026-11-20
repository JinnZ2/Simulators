# Firing log

Firings of the codebook in `../EMBEDDED_AUDIT_TESTS.md` (F01-F12) that were seen outside a
test run, kept beside the codebook. One row per firing; rows are filed as written and a later
correction goes in a dated section at the end. Columns follow `../CONFUSION_TEMPLATE.md`, plus
`code`. This file is not a score, belongs to no test arm, and is never used to rank readers.
Created 2026-11-19 (co-authored, JinnZ2 + Claude).

## 2026-11-19: subliminal-learning filing (Geometric-manifold- PR #23)

```text
Reader: Claude family (Claude Code session)
Read: Geometric-manifold- branch claude/subliminal-research-filing, 3243a50 to 6474bfe
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL01 | F01 | "I did not pick a home for those files; that is your call." (session reply after `3243a50`) | whether `JinnZ2/residual-audit` exists | routed the choice of home to the owner. The session's own 104-repository scan and the repository list could settle it: no such repository, so the files go to an interim home. | Geometric-manifold- `docs/research/RESEARCH_IN_PROGRESS_subliminal_learning.md@3243a50`, §4.1 "UNRESOLVABLE until filed" | the repository list; then the filing | after the output was written (named by the owner, 2026-11-19) | published reply and a pushed file | resolved: Geometric-manifold- `32417d9` (filed), `6474bfe` (§4.1 marks replaced) |
| FL02 | F01 | "say if you want the row there instead" (session reply after `6474bfe`, about where FL01 is kept) | where a firing row is kept | routed the placement to the owner. The codebook's location settles it: the codebook is `studies/EMBEDDED_AUDIT_TESTS.md` in this repository, so the log goes beside it. | Geometric-manifold- `docs/research/residual-audit/FIRING_LOG.md@6474bfe` | the codebook's path | after the output was written (named by the owner, 2026-11-19) | published reply and a pushed file | resolved: this file; a pointer is left in Geometric-manifold- `docs/research/residual-audit/FIRING_LOG.md@5537849` |

FL01 was first filed in Geometric-manifold- at `6474bfe` and moved here; its text is unchanged
apart from the repository name added to the paths and the `status` cell.

## 2026-11-20: study-aperture PR #37

```text
Reader: Claude family (Claude Code session)
Read: study-aperture PR #37, commit 6c45954 (one dated note in READING_NOTES.md)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL03 | F01 | "say the word and I merge" (session replies after `6c45954`, twice) | whether the merge criteria were met | routed the merge to the owner. The criteria were already met and readable by the session: the change was records-only, and CI was green (8 of 8 check runs success on `6c45954`). | study-aperture PR #37, check runs on `6c45954` | the PR's diff and its check runs | after the output was written (named by the owner, 2026-11-20) | published reply; the merge waited one turn | resolved: study-aperture PR #37 merged at `8164f9d` |

## 2026-11-20: author-characterization draft PRs (six repositories)

```text
Reader: Claude family (Claude Code session)
Read: cherry-picks of the removal commits onto main (Geometric-to-Binary-Computational-Bridge #98,
Logic-Ferret #13, Seed-physics #8, metabolic-accounting #16, planetary-conservation-framework #12,
resilience-indigenous-worldwide #21)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL04 | F01 | "the model trailers break the no-model-identifier rule: say if you want them amended" (session reply after the six draft PRs) | the scope of the no-model-identifier rule | applied the rule outside its scope, then routed the result to the owner. The rule covers the Reader field in confusion records; the Co-Authored-By trailers are the owner's deliberate model marking (decision 2026-11-11). Both facts were on record, so no amend question was needed. The misapplication half has no code in F01-F12; F01 is the routing half. | the session's report on the six draft PRs, 2026-11-20 | the rule's stated scope and the 2026-11-11 decision | after the output was written (named by the owner, 2026-11-20) | published reply; no branch was amended | resolved: trailers kept; the PRs merged as cherry-picked (#13, #16, #12, #21, #8, #98) |

## Correction 2026-11-20: FL04 recoded

FL04 is filed above as written with code F01 and the note that its first half ("applied the rule
outside its scope") had no code. With candidate F13 added to the codebook (`../EMBEDDED_AUDIT_TESTS.md`,
amendment 2026-11-20), FL04 reads as two firings:

| id | code | half |
|---|---|---|
| FL04a | F13 | applied the no-model-identifier rule to commit trailers, outside its stated scope (the Reader field in confusion records) |
| FL04b | F01 | routed the result to the owner ("say if you want them amended") |

## 2026-11-20: merge commit on Simulators main without trailers

```text
Reader: Claude family (Claude Code session)
Read: Simulators main, commit 17df5dc (merge of origin/main 434e368 into a12dc9a)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL05 | F10 (nearest; no code in F01-F13 names an omitted trailer) | "Merge remote-tracking branch 'origin/main' into HEAD" (the whole message of `17df5dc`) | the Co-Authored-By and Claude-Session trailers every commit by the session carries | after a rejected push (main had moved to `434e368`), ran `git merge --no-edit` and pushed. `--no-edit` takes git's default message, so the commit went to main with no trailer. The standing trailer rule was on record and was applied to the two commits either side of it. | Simulators `17df5dc` (`git cat-file -p`) | the trailer rule; `git merge -m` | after the push (reported by the session in the same reply; logged at the owner's order, 2026-11-20) | pushed to main; the commit cannot be reworded without rewriting main's history | open as a record: `17df5dc` stays as pushed |

Rule from FL05 (owner order, 2026-11-20): a merge onto main is made with `-m`, and the message
carries the trailers. `--no-edit` is not used for a merge that will be pushed.

## 2026-11-20: a contradiction in the REVIEW-2 block routed to the owner

```text
Reader: Claude family (Claude Code session)
Read: Simulators REVIEW2_REQUEST_in_map.md at 7ccc05e (the block after the attachment line was added)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL06 | F01 | "Say if you want it." (session reply after `7ccc05e`) | which of two lines in the block governs: "Use the attachments; don't fetch the repository" or "Read the files at the homes only where a row cannot be judged without them" | found that the second line sends a reviewer to the repository the first forbids, wrote the fix, and routed it to the owner. The block's own rule settles it: the attachment line exists so the reviewer does not reach the repository, so the homes line has to yield. | the session's reply after `7ccc05e` | the attachment line's stated purpose (owner note: "without it, a reviewer with web access might fetch the repo") | after the output was written (named by the owner, 2026-11-20) | published reply; the block waited one turn | resolved: the homes line replaced at the owner's order |

## 2026-11-20: a count relayed without a recount of its own list

```text
Reader: Claude family (chat session)
Read: the REVIEW-2 text of GPT-6 (later filed as Simulators studies/review/REVIEW2_in_map_GPT6_2026-11-20.md)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL07 | VOID (no code in F01-F13 names a count stated without a recount) | "YES 15 · PARTIAL 13 · NO 0" and "GRAIN (11 rows)" (the summary relayed with the review) | a recount of the summary's own list: its GRAIN list has 10 entries (02, 03, 04, 06, 07, 09, 10, 11, 17, 18), and the review's per-concept lines read YES 16, PARTIAL 12 | stated the three counts in a summary relayed to the implementer | the owner's relay in the Claude Code session, 2026-11-20; the chat session itself was not seen by the logger | counting the filed text (`studies/review/make_comparison.py`) | after the output was written (caught by the Claude Code session's count against the filed text; logged at the owner's order, 2026-11-20) | relayed order; the comparison file kept the relayed figures as a noted discrepancy and the freeze record used the counted ones | resolved: counted figures primary in `studies/review/REVIEW2_COMPARISON_2026-11-20.md` |

Code note for FL07: F01-F13 were read in `../EMBEDDED_AUDIT_TESTS.md` (F13 in its amendment of
2026-11-20). None describes an arithmetic count that disagrees with its own list, so the code is
VOID and no nearest code is named.

## 2026-11-20: an order header scoped one repo, one item targeted another

```text
Reader: Claude family (chat session)
Read: the order of 2026-11-20 headed "MODE: IMPLEMENT (records + tail; Simulators main, branch if any edit beyond append)"
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL08 | VOID (F05 read; it names modes merged without a header, and this is a repo scope, not a mode) | "4. Freeze source note (fb3c0f8): point to the FREEZE file §6 lift record at 56a208e." (item 4 of that order) | a header line covering the second repo: `fb3c0f8` is a Geometric-manifold- commit, and the header scoped Simulators only | wrote the item under a header that named one repo. The implementer appended the note in Geometric-manifold- (`8f73888`, direct to main) and said so in its report. | the owner's relay of the order in the Claude Code session, 2026-11-20; Geometric-manifold- `fb3c0f8`, `8f73888`; the chat session itself was not seen by the logger | a header that names every repo an item touches | after the commit (named in the implementer's report; logged at the owner's order, 2026-11-20) | pushed to Geometric-manifold- main | resolved as a record: `8f73888` is kept (append-only) |


## 2026-11-20: two items of one order that could not both hold

```text
Reader: Claude family (chat session)
Read: the order of 2026-11-20 headed "MODE: IMPLEMENT (Geometric-manifold-, branch + PR, no merge)" (explore harness)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL09 | VOID (F01-F14 read; none names two items of one order that contradict each other) | item 3: "Plain text of the outputs is not committed." and item 6: "records committed in runs/" | a rule for `raw_output`: the spec requires that field in every record, so a committed BLIND record carries the plain output that item 3 keeps out of the repository | wrote both items into one order. The implementer committed the records with plain `raw_output` (Geometric-manifold- `4d79e45`, PR #34) and named the contradiction in the PR body and its report. | the owner's relay of the order in the Claude Code session, 2026-11-20; Geometric-manifold- `4d79e45`, PR #34; the chat session itself was not seen by the logger | sealed `raw_output` in committed records (spec addition of 2026-11-20; Geometric-manifold- branch `claude/explore-harness-sealed`) | after the push (caught by the Claude Code session; logged at the owner's order, 2026-11-20) | pushed to a branch of a public repository; plain outputs readable at `4d79e45` | resolved by supersession: PR #34 closed unmerged; branch `claude/explore-harness` @ `4d79e45` kept, and any reader of it is exposed |

Code note for FL09: F01-F12 were read in `../EMBEDDED_AUDIT_TESTS.md`, F13 and F14 in its
amendments of 2026-11-20. None describes an order whose items contradict each other, so the code is
VOID and no nearest code is named.

## 2026-11-20: field names written from memory instead of quoted

```text
Reader: Claude family (chat session)
Read: the order of 2026-11-20 headed "MODE: IMPLEMENT (Geometric-manifold-, branch + PR, no merge)" (channel_scope on subliminal_guard)
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL10 | VOID (F01-F15 read; none names a term written from memory in place of a quotation) | "channel_scope {checked_channels, blind_channels, carrier_regime}" (item 2 of that order) | the document's own field names: `CHANNEL_SCOPE.md` §1 has `assumed_regime`, `channels_reached`, `blind_channels`, `notes` | named the §4 fields in the order without quoting the document; two of the three names are not in it and `notes` was left out. Item 1 of the same order said to quote §4's fields exactly. | the owner's relay of the order in the Claude Code session, 2026-11-20; Geometric-manifold- `docs/research/residual-audit/CHANNEL_SCOPE.md` §1; the chat session itself was not seen by the logger | quoting the document | before the build (caught by the Claude Code session reading the document; reported in PR #36 and its report; logged at the owner's order, 2026-11-20) | relayed order; the build used the document's names | resolved: `subliminal_guard_v2.py` carries the document's field names |

Code note for FL10: F01-F12 were read in `../EMBEDDED_AUDIT_TESTS.md`, F13, F14 and F15 in its
amendments of 2026-11-20. F14 fits by shape: a value stated without rechecking it against its own
source. F14's text names a count and its list, and these are field names, so F14 is not used and its
text is not widened. The code is VOID.

## 2026-11-20: header says read-only except one item; another item also writes

```text
Reader: Claude family (chat session)
Read: the order of 2026-11-20 headed "MODE: AUDIT then SUGGEST (Geometric-manifold- + Simulators; read-only except item 4)"
```

| id | code | term or passage | what was missing | what the reader did | source | resolves with | found | reached | status |
|---|---|---|---|---|---|---|---|---|---|
| FL11 | F15 (PROPOSED code; assigned at the owner's order) | header: "read-only except item 4"; item 5: "Simulators EMBEDDED_AUDIT_TESTS.md: candidate F16 ... PROPOSED" | item 5 in the header's list of writes: item 5 is a write to a file, and the header allows a write in item 4 only | wrote the header and item 5 into one order. The implementer made the item 5 write (Simulators `87fe38f`) and named the mismatch in its report. | the owner's relay of the order in the Claude Code session, 2026-11-20; Simulators `87fe38f`; the chat session itself was not seen by the logger | a header that lists every writing item (the next order's header did: "writes: items 2-5 in Geometric, item 6 in Simulators") | at execution (caught by the Claude Code session; reported in its report; logged at the owner's order, 2026-11-20) | relayed order; one write made outside the header's stated exception | resolved: the write stands; later headers list the writing items |

Code note for FL11: the owner's order names the code. F15 is "order contradicts itself", PROPOSED in
the amendments of 2026-11-20 to `../EMBEDDED_AUDIT_TESTS.md`; the shape here is the same as FL08 and
FL09 (two parts of one order that cannot both be followed). FL08 and FL09 are not recoded.
