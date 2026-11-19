# Confusion record (template)

For any reader of the packet, the studies or a report: a model session or a person. File one record per reader per piece of work in `studies/confusion/`, named `<date>_<reader pseudonym>_<subject>.md`. Records are filed as written; a later correction goes in a dated section at the end, never as an edit above it.

**Origin.** The request text is the owner's (2026-11-19); the columns `found`, `reached` and `status` were added in the Claude Code session and accepted by the owner ("Yes please").

```text
Reader: <family or pseudonym>      Read: <files or report, with commit>
```

The `Reader` slot names a model family ("Claude family", "Kimi", "GPT") or a pseudonym, never a model identifier or a person's name or account.

For every point where you were unsure, guessed, or stopped, give one row:

```text
id | term or passage | what was missing | what you did (guessed / stopped / read X as Y) | source path@commit | resolves with
   | found (before / after the output was written) | reached (working notes / published report / hashed file) | status (open / resolved: commit or decision)
```

- "what you did" matters most: a guess you made counts, even if it later turned out right.
- Leave a slot `void` if you don't know; don't drop the row.
- No confusion found: say "none found" and list what you read.
- One row per point; don't merge rows.
- `reached` says how far a correction has to travel: a guess in working notes costs nothing to fix; one in a published report needs a dated correction; one in a hashed file needs a dated PREREG note.
- A confusion record is not a score. It is never used to rank readers or to change a key.
