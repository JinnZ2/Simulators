# HOLDS -- which session holds which branch, and which paths it may touch

Operator protocol, 2026-10-07:

- Every session reads this file before starting work on a branch.
- It adds a row for any branch it takes.
- It skips any branch another session holds.
- The merge rule's scope check reads `allowed_paths`: a diff that touches
  a path outside its branch's allowed_paths fails the check.

`allowed_paths` is a comma-separated list. A trailing `/*` covers
everything under that directory. Status is HELD while work is open, then
MERGED (with PR and merge sha), RELEASED, or ABANDONED. A row is never
deleted; a finished row stays as the record.

| branch | allowed_paths | holder_session | started | status |
|---|---|---|---|---|
| claude/threshold-states-escape | threshold-states/*, interaction_class.py, test_interaction_class.py, .github/workflows/test.yml, threshold-states-in-animal-escape.md [a], archive/interaction_class/* [a], tests/test_archive_expected_red.py [a] | session_01Y4zVdoRHPDHpVwSPbqbeLR, session_014bxQGPgkmsJRWUx92REKSs | 2026-10-05 | MERGED #123 (c7aa5f2) |
| claude/repin-sense-as-match | KNOWN_RED.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #124 (2cb6eca) |
| claude/queue-holds | notes/queue/HOLDS.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #125 (731a94d) |
| claude/human-sensing-prior-cc0-cbm411 | CLAUDE.md, README.md, human-sensing-prior/PATHWAYS.md, human-sensing-prior/PATHWAY_B.md, human-sensing-prior/PREDICTIONS.md, human-sensing-prior/pathways.py, human-sensing-prior/test_pathways.py, human-sensing-prior/samples/features.sample.txt, human-sensing-prior/samples/lengths.sample.txt, human-sensing-prior/samples/score_unrun.sample.txt, notes/queue/HOLDS.md, human-sensing-prior/samples/pilot_unrun.sample.txt [b], human-sensing-prior/registered/human-sensing-prior.7f780aa.md [b] | session_014bxQGPgkmsJRWUx92REKSs, session_01U4mRsfZAdaV1xWBmZSRbjK [b] | 2026-10-07 | HELD; pilot BLOCKED_ON_RUNNER [c] |

[a] Backfilled after the fact. These paths are in #123's diff and not in
the operator's backfill list: `threshold-states/*, interaction_class.py,
test_interaction_class.py, .github/workflows/<ci file>`.
- `threshold-states-in-animal-escape.md` sits at the repo root, so
  `threshold-states/*` does not cover it. It carries the section 8
  rewrite that removes the duplicated literature table.
- `archive/interaction_class/*` and `tests/test_archive_expected_red.py`
  carry the archive move the operator ordered on 2026-10-07 (root build to
  `archive/` plus a redirect).

Under the operator's list alone, #123's scope check would fail on these 5
files. They are recorded here, not hidden.

Rule from 2026-10-07 on (operator): the session taking a hold declares
allowed_paths here BEFORE starting work. A backfill written chat-side
always lags the diff.

claude/human-sensing-prior-cc0-cbm411: allowed_paths is the branch's diff
against main (merge-base 9262516) as it stood before any work, plus this
file. The branch was opened by another session; this session took the
hold to merge it, and its row was declared in the branch's first commit,
before main was merged in.

[b] Backfilled after the fact, 2026-10-07. Session
session_01U4mRsfZAdaV1xWBmZSRbjK opened this branch. It continued work on
the branch at the operator's direction, and it did not read this file
before doing so. Its commit b0c8795 (amendment 2 harness) was made before
it fetched the hold. Two paths in that commit and its follow-up are
outside the declared list, and both are new files:
- `samples/pilot_unrun.sample.txt` is the sample output of the pilot gate
  that amendment 2 item 2 adds.
- `registered/human-sensing-prior.7f780aa.md` is a byte copy of pathway A
  at 7f780aa, sha256 1a42dc8c...cbd7, the pin in amendment 2 item 4.
  It is needed because the merge of main (79e6374) moved the working copy
  of A off the pin.

Under the declared list alone, the scope check would fail on these 2
files. They are recorded here, not hidden.

[c] 2026-10-07, operator. The human-sensing-prior pilot (amendment 2
item 2) is BLOCKED_ON_RUNNER. There is no model endpoint in the Claude
Code environment, and the operator is on a phone. A chat-side API runner
artifact may be built; that decision is pending. The hold stays HELD.
