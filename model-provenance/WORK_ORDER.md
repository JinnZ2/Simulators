# WORK ORDER 5 — MODEL PROVENANCE

Delivered verbatim. Nothing in this file is edited; the audit is in
`AUDIT_NOTES.md` and `CLAIM_TABLE.md`.

---

WORK ORDER 5 — MODEL PROVENANCE

S1. FORWARD (write-time)
  On session open, Claude Code appends one line to
  CLAUDE.md or a sessions log:
    date, model identifier as self-reported, repo, branch
  Self-reported only. If the build string is unavailable,
  write UNKNOWN — do not infer from behaviour.

S2. RETROSPECTIVE (decode existing history)
  Input: git log across the repo ecosystem, plus the
  release-date table for the model line.
  For each commit, emit the model version implied by its
  date, as an INTERVAL not a point:
    unambiguous window -> single version
    within a switchover window -> both candidates, no pick
    commit predates the table -> NOT_DECODABLE
  Output is a decode table, stored alongside, never written
  back into history.

S3. WHY INTERVAL
  Version is derived from date under a stated assumption
  (always current-at-the-time). The assumption is the
  claim; record it as the derivation, not as a fact about
  the commit.

S4. CONSTRAINT
  Do not modify commits. Do not label any commit's output
  as better or worse by version. Reports structure only.
