# studies/cleanup

Status: records. A read-only reclass of branches, run 2026-11-20T10:07:39Z to 10:08:45Z. Nothing
was deleted, pushed or archived by it. SAFE here means "a proof was found that deleting the branch
loses no file content"; it is not an instruction to delete.

## Why the date is 2026-11-20

The order named `SAFE_BRANCHES_2026-11-19.tsv`, to be taken from `BRANCH_RECLASS_2026-11-19.tsv`.
That scratch file is not on the machine that made this record and is in no repository. So the
inventory and reclass were rerun and the files carry the run date. The 2026-11-19 list is NOT
LOCATED; the two may differ.

## Files

- `SAFE_BRANCHES_2026-11-20.tsv`: 292 rows. Columns: repo, branch, tip, proof, needs_archive,
  archive_branch, commits_not_on_default, default_branch, default_tip.
- `ARCHIVES_NEEDED_2026-11-20.tsv`: the 40 rows with needs_archive YES.
- `reclass_branches.py`: the classifier as run.

## Scope

- 105 repo names read from the session's repo list; 103 cloned (bare, `--filter=blob:none`).
  NOT READ: `experiments`, `gap-quantification-protocol` (clone refused: credentials asked for).
- 465 non-default branches read across 102 repos (one repo has only its default branch).
- 17 `archive/*` branches are left out of the SAFE list whatever their proof.
- 156 branches got no proof (NONE). They are not listed here.

## Proof types

| proof | test | rows | needs_archive |
|---|---|---|---|
| ancestor | `git merge-base --is-ancestor <tip> <default tip>` | 240 | NO |
| content-proof | not an ancestor; `git merge-tree --write-tree <default> <tip>` exits 0 and its tree equals the default tree (merging the branch would change no file) | 40 | YES |
| archive-match | not an ancestor, no content-proof; the tip equals, or is an ancestor of, an `archive/*` branch in the same repo | 12 | NO (the archive branch is in `archive_branch`) |
| a2 | NOT RUN: no definition of "a2" was located in any repository or in the session record | 0 | |

Order of tests: ancestor, then content-proof, then archive-match. A branch gets the first that holds.

## needs_archive

YES = content-proof: the commits are not ancestors of the default branch, so deleting the branch
drops them from every ref even though their file content is on the default branch.
Count: 40, in 33 repos. 2 of the 40 already have an archive branch that contains the tip
(`archive_branch` column); 38 have none. No archive branch was created by this run.

## Limits

- Open pull requests were not read. A SAFE branch may be the head of an open PR.
- content-proof reads files at the two tips. It does not read commit messages or intermediate
  states; those are what an archive branch keeps.
- Tips are as of the run time. A branch pushed to since is not covered by its row.
- `Simulators claude/healing-folder-additions-u5aojl` (content-proof) is the working branch
  assigned to the session that made this record.
- 1 builder, 1 run, no second reader.
