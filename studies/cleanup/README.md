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

## Second pass, 2026-11-20 (a2, open_pr, own branch)

PR state was read with the GitHub MCP pull-request tool, 2026-11-20T10:19Z to 10:24Z, by five
delegated readers; branch tips and `refs/pull/*/head` by `git ls-remote` at 10:19Z.

**What the MCP tool could read.** 29 of the 99 repos that needed a PR read. The other 70 are
outside this session's GitHub tool scope ("Access denied: repository ... is not configured for
this session"); a read-only attach does not add them. They are listed at the end.

### a2 (PR merged AND `refs/pull/N/head` == tip)

Run over the 156 unproven branches. Per-PR results: `A2_RUN_2026-11-20.tsv`.

| reading | branches |
|---|---|
| no PR head at the tip (git) : a2 cannot hold | 109 |
| PR head == tip, PR open | 30 |
| PR head == tip, PR closed, not merged | 5 |
| PR head == tip, PR merged = a2 | 1 |
| PR head == tip, PR NOT READ (repo out of scope) | 11 |

The one a2 is `AI-Consciousness-Sensors claude/error-records`, PR #43, head and tip both
`71b8d93972a7`, merged 2026-11-20T10:07:51Z, which is inside the reclass run. The branch was
already GONE at 10:19Z (`git ls-remote`). It is not added to the SAFE list: there is no branch
left to delete. a2 rows added to the SAFE list: 0.

### open_pr

Column `open_pr` on every row, with `open_pr_basis`.

- NO, by git: no `refs/pull/N/head` equals the tip, so no open PR can have this branch as head
  at this tip.
- NO, by MCP: a PR head equals the tip and the PR is not in the repo's open list.
- YES: the branch is the head of an open PR. Moved to `KEEP_BRANCHES_2026-11-20.tsv`.
- NOT_READ: a PR head equals the tip and the repo is out of scope. These rows stay in the SAFE
  list with open_pr unread; a PR whose head equals the tip is most often a merged one for an
  ancestor row, but that was not read.

Counts over the 292 rows of the first pass: NO 157, YES 3, NOT_READ 132.

### KEEP (3 rows, out of the SAFE list)

- `orbital-phycom claude/ci-floor-3-10` and `claude/ci-quick-tests-module-run`: heads of open PRs.
- `Simulators claude/healing-folder-additions-u5aojl`: the working branch of the session that
  made this record (also the head of open draft PR #261). Excluded.

### After the second pass

SAFE list: 289 rows (ancestor 240, content-proof 37, archive-match 12, a2 0).
needs_archive YES: 37 (2 already have an archive branch containing the tip; 35 have none).
`ARCHIVES_NEEDED_2026-11-20.tsv` is rewritten to the 37.

### Repos whose PR state was NOT READ (70)

4D-language-lens, Academic-Translator, Adaptive-Intelligence-Framework-, BE2-communication, Bio-Grid-American-Manufacturing-, BioGrid2.0, CEED, Combine-Cognitive-Architecture-, Coop-framework, Cyclic-programming, DIY-CNC, Emotions-as-Sensors, Fractal-Compass-Atlas, Fractal_Compass_Core, Fulgerite-Antenna-Prototype-, Geometric-to-Binary-Computational-Bridge, GlyphAI, HAAS, Hardware-Store, Infrastructure-assistance, Inversion, JinnZ2, Keystone-Codex, Living-Intelligence-Database, Mandala-Computing, Municipal-Code-Translator, Nexus-emergency-management, Non-equilibrium-atmospheric-forcing, Nuclear-Donut-DataCenter, PatternBridge, Permeable-intelligence-commons, Plain-English-Translator, Prosthetic-arm-CNC, Resilience, Resilience-hydrology-core, Resilience-indigenous-worldwide, Resilient-AI-Human-Collaboration-, Seed-physics, Sovereign-Octahedral-Mandala-Substrate-SOMS-, Study-on-Nazca-Lines, Symbolic-Defense-Protocol, Symbolic-sensor-suite, SymbolicSentinel, TRDAP, The-Curriculum-of-Everything-Earth-, Universal-Redesign-Algorithm-, Voice-Integrity-Module, YouTube-Wisdom-Lens, ai-human-audit-protocol, assumption_validator, biomachine_ecology, dyed-fuel-diff, earth-systems-physics, explorative-math, fairmont-ecological-recovery, framework-instruments, geometric-optimization, geometric-to-binary, hands-lie-detector, hgai-geometric-systems, infrastructure-stability-model, interdisciplinary-studies, metabolic-accounting, open-source-plastic-lab, shape-index, stability-trigger-envelope, temporal-consciousness-playground, tool-off-metrology, trust-exit-model, urban-resilience-sim.
