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

