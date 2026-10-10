# DISPATCH_QUEUE

Approved by Kavik 2026-10-10.

Purpose: standing-rule step 5 needs a queue both sessions can read.
Chat-side memory is unreachable from Claude Code, so it is mirrored here.
This file replaces the chat-side queue for step 5. Keep both in sync;
the repo file is authoritative for Claude Code.

Standing rule:
  Before any build: read this file, record branch + scope,
  skip if another session holds it. After merge/close: update
  the line, never delete it (append-only).

Format: append-only, one line per branch, pipe-delimited:
  branch | scope paths | session | status | date

A later line for the same branch supersedes an earlier one. Nothing
above it is edited or removed.

## Seed (as dispatched, 2026-10-10)

claude/presignal-ledger      | tools/presignal_ledger.py | — | merge-ready #137 | 2026-10-10
claude/threshold-states-escape | UNKNOWN | — | open | 2026-10-07
claude/baseline-by-id          | UNKNOWN | — | open | 2026-10-07
claude/sense-as-match          | UNKNOWN | — | open | 2026-10-07
claude/coinage-log-status-split| UNKNOWN | — | open | 2026-10-07
claude/human-sensing-prior     | UNKNOWN | — | open | 2026-10-07

## Log

claude/dispatch-queue | DISPATCH_QUEUE.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/presignal-ledger | tools/presignal_ledger.py | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #137 (merged 2026-10-09; tip 6ca6a34 in main) | 2026-10-10
claude/threshold-states-escape | UNKNOWN | — | MERGED #123 (tip 378b4ee in main) | 2026-10-10
claude/baseline-by-id | UNKNOWN | — | MERGED #119 (0a04bea); no remote branch | 2026-10-10
claude/sense-as-match | UNKNOWN | — | NOT_FOUND under this name; claude/repin-sense-as-match tip 948f508 in main | 2026-10-10
claude/coinage-log-status-split | UNKNOWN | — | MERGED #121 (59b71f8); no remote branch | 2026-10-10
claude/human-sensing-prior | UNKNOWN | — | NOT_FOUND under this name; claude/human-sensing-prior-cc0-cbm411 tip 9202714 open, not in main | 2026-10-10
claude/dispatch-queue | DISPATCH_QUEUE.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #145 (03cd312); line appended via claude/dispatch-queue-145 | 2026-10-10
claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #148 (3e18eb0) | 2026-10-10
method-layer:claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#4 (1fb7f6f) | 2026-10-10
claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #151 (04cd9f6) | 2026-10-10
method-layer:claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#5 (ecca94f) | 2026-10-10
claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
