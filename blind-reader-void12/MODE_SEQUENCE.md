# MODE_SEQUENCE.md

Delivered by the owner on 2026-11-19 and filed verbatim below. The full message it came in is `studies/as_received/mode_and_authority_2026-11-19.md`. Applies to `blind-reader-void12/`; no other folder has adopted it. Request headers per mode: `studies/REQUEST_HEADERS.md`.

```text
This work has no hierarchy. Authority sits in the active mode and its stage,
not in a person or a model.

Sequence: BLIND → REVIEW → AUDIT → SUGGEST → IMPLEMENT → REVIEW-2 → AUDIT-2

- Exposure only adds. BLIND has to come first and is spent at first exposure.
- One mode per session or request, named in its header.
- A disagreement is a record of a gap. It doesn't go up to someone to settle.
- Where evidence or physics can decide, it decides, and the reasoning is shown.
  Where it can't, branch, and keep both.
- Routing a decision "to the owner" isn't the default. Route it to the stage
  that can decide it.

Open: in REVIEW-2 and AUDIT-2, does the reader have to differ from whoever implemented?  [void]
```

## Later (2026-11-19): independence rules, from the owner

Delivered by the owner on 2026-11-19, filed verbatim. This answers the open line above for REVIEW-2 (a different reader is required). For AUDIT-2 it splits the answer by deterministic and judgment checks. The open line is kept as written. Applied in `studies/INDEPENDENCE_LEDGER.md`.

```text
HOLDS (OBSERVED today)
  self-audit missed the drift; an outside reader (Kimi C11) caught it
  the deterministic / judgment split is real: rerunning a test ≠ judging the test

AMENDMENTS (DERIVED)
  A1  a fresh session isn't enough: the same model family shares the same geometry
      (same shape as subliminal transfer needing the same base model; the self-preference bias
       results in your audit files point the same way)
      → independence is a gradient, not yes/no

  A2  deterministic rerun ≠ an independent check when the implementer wrote the check
      the C11 drift was IN the fixture logic → rerunning it reproduces the drift, and it passes
      → test design is a judgment act: it needs a REVIEW-2 by a different reader;
        only the execution can be the implementer's

  A3  "context" has to include memory and project features, not just the session
      (Grok's memory was ON in a "fresh" session)


REVIEW-2: independent review requires a reader different from the implementer.

AUDIT-2: deterministic checks may be rerun by the implementer if the procedure and
results are reproducible AND the check's design was reviewed by a different reader.
Judgment-based audit decisions (including test and fixture design) require a
different auditor when independence is claimed.

INDEPENDENCE (record one level + every field):
  L0  same session                          → NOT_ESTABLISHED
  L1  fresh session, same family            → WEAK (shared geometry)
  L2  different family                      → MODERATE
  L3  different family + no exposure to the implementation or the other readers
  L4  L3 + a non-model instrument (human, physical measurement, source run)
  fields: reader, implementer, session, model family, memory on/off,
          project/context features, exposure (packet / key / repo / implementation /
          other readers' records: yes / no / unknown each)
  unknown field → void, and the level is capped at the lowest level it could be

A same-actor pass is valid as self-review or self-audit: record L0 (or L1). Never
treat it as independent confirmation, and never use it alone to close a
disagreement. Agreement between readers at the same level counts once, not once
per reader.
```
