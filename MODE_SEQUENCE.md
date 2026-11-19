# MODE_SEQUENCE.md

SOURCE: Claude chat, 2026-11-19 11:48 (delivered by the owner; filed here at the owner's IMPLEMENT order of 2026-11-19).
Source text: `blind-reader-void12/studies/as_received/mode_and_authority_2026-11-19.md`, lines 91-106 (line numbers as of the commit that added this file). First filed, for one folder, as `blind-reader-void12/MODE_SEQUENCE.md`; that file stays and points here.

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
```

~~Open: in REVIEW-2 and AUDIT-2, does the reader have to differ from whoever implemented?  [void]~~
Struck 2026-11-19: answered by the block below. The line is kept as written.

## REVIEW-2 / AUDIT-2 / INDEPENDENCE

SOURCE: Kimi, 2026-11-19 12:16 (the REVIEW-2 and AUDIT-2 rule) + Claude chat amendments, 2026-11-19 (the L0-L4 ladder; test design is a judgment act and needs a REVIEW-2; memory and project context count; an unknown field caps the level; agreement counts once per level). Sources and times are owner-stated. The block was delivered whole by the owner and is filed verbatim; which lines are whose is given only at the level above. Applied in `blind-reader-void12/studies/INDEPENDENCE_LEDGER.md`.

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

## Where the rest is filed

- Request headers per mode, and the reader's suggestions they come from: `blind-reader-void12/studies/REQUEST_HEADERS.md`
- The role defaults that fill a gap where no mode is stated: `blind-reader-void12/studies/AI_ROLE_DEFAULTS.md`
- K3, the frame tally for the unstated mode sequence: `blind-reader-void12/studies/K3_MODE_SEQUENCE_DEFAULT.md`
