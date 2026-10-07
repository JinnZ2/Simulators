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
| claude/queue-holds | notes/queue/HOLDS.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | HELD |
| claude/interaction-spec-q1-q4 | threshold-states-in-animal-escape.md, notes/queue/HOLDS.md, threshold-states/* [b] | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #127 (71df45c) |
| claude/holds-relation-axes | notes/queue/HOLDS.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | HELD |
| JinnZ2/Polyhedral-Intelligence: claude/relation-two-axes [c] | ontology/relation_classes.json, ontology/relation_class.py, ontology/relation_classes.md, tests/test_relation_class.py, CLAUDE.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | HELD |

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

[b] Widened 2026-10-07 BEFORE the build work starts, in its own commit,
on the operator's dispatch "§8 interaction precedence: resolve OPEN,
commit cases, then build". `threshold-states/*` carries
`outside_cases_v2.json` (committed alone, before any code change), the
Q1-Q4 build of `interaction.py`, its tests, the runner and the samples.

[c] A branch in another repository. Polyhedral-Intelligence carries no
HOLDS file, so the hold is declared here, before work, per the operator's
dispatch "RELATION ONTOLOGY: split class into two axes" (2026-10-07).
`CLAUDE.md` is listed because its Emotion Glyph Map note names the enum's
members; it is touched only if that list must change.
