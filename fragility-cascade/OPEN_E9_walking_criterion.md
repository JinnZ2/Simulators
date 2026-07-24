# OPEN_E9 — walking vs intermittent criterion

Status: **OPEN / EMPIRICAL**. Not a bug. Not a fix. A recorded divergence
between the residual() spec intent and the residual() implementation, held
open until an experiment resolves which rule wins.

## What happened

`divlog.residual([-1, 0, +2])` returns **WALKING** on the shipped v1.

SPEC_intent for the sequence `[-1, 0, +2]` was **INTERMITTENT**.

The disagreement is real (same input, different output). Per D5, it is logged
into the divlog rather than silently patched:

```
first real log entry
    id            48da4f4d47cd   (this install, under divlog v1-against-SPEC;
                                  same divergence has been logged under
                                  three ids across the module's evolution --
                                  user local: 03efe4e41e61,
                                  earlier install: 8a6a9e291671,
                                  current: 48da4f4d47cd;
                                  all reference the SAME divergence, differ
                                  only in field defaults + JSON serialization)
    subject       residual.WALKING_criterion
    axis_a        SPEC_intent
    axis_b        divlog.residual(v1)
    kind          SAME_INPUTS_DIFF_BAND   (same digest, different band)
    digest        n3-gaps:-1,0,+2         (the exact trigger, on the record)
    band_a        INTERMITTENT
    band_b        WALKING
    supersedes    None                    (baseline entry)
```

**Note on id stability across module revisions.** When `divlog.py` was
rewritten against SPEC_drift_mesh, the JSON serialization changed
(compact separators; slightly different field defaults). The id — which
is `sha256[:12]` of the serialized dict minus `note` — recomputed to a
new value even though the logical content is unchanged. This is a real
gap the SPEC does not address: if the id is a stable pointer, `supersedes`
references break when the divlog module is versioned. For E9 itself, the
gap is benign — every install re-logs the divergence and the E9 issue
tracks the CONCEPT, not any single id. For future issues that stack
`supersedes` chains across divlog versions, this needs an answer.

## The two rules on the table

**Shipped rule (v1)** — consecutive-diff sign inspection:

```
diffs = [gaps[i+1] - gaps[i] for i in range(len(gaps) - 1)]
has_pos = any(d > 0 for d in diffs)
has_neg = any(d < 0 for d in diffs)
INTERMITTENT iff has_pos AND has_neg
WALKING      iff monotone (has_pos xor has_neg, or one direction with zeros)
```

Under this rule, `[-1, 0, +2]` → diffs `[+1, +2]` → both positive → WALKING.

**Spec-author rule (implied)** — one plausible reading: INTERMITTENT fires
when the gap sequence crosses zero (the disagreement flips sides of the
primary), not merely when it reverses direction. Under that rule,
`[-1, 0, +2]` crosses zero (moves from negative to non-negative) →
INTERMITTENT.

Both rules are defensible on the label. Only real data will distinguish them.

## Handoff protocol (per D5)

- v1 lands **as-is**. No special-case for the failing sequence.
- Resolution comes as a **NEW entry that supersedes `8a6a9e291671`**
  (or `03efe4e41e61` on the user's local install) — not an untracked edit
  to `residual()`.
- Any change to the rule ships as a **versioned change** (retire current
  divlog to `legacy/divlog_v1.py`, land v2, log the supersedes chain).
- E9 experiment (the resolution mechanism):

```
synthetic arm    sweep candidate rules over n=3..30 gap sequences
                 report BOTH false-alarm and miss rates for each rule
                 rules considered:
                   consecutive-diff sign inspection (shipped)
                   zero-crossing (spec-author implied)
                   variance-of-gaps threshold
                   run-length on same-sign gap
                 pick the rule that minimises the sum of error rates
                 on the operator's real intent, not on either author's guess

field arm        only the operator's months of real divergence histories
                 can settle it. tag them with the intended shape, feed to
                 the synthetic-arm test rig, pick the rule that reproduces
                 the intent best. register the corresponding noise scale as
                 E16 (log actually becomes a baseline).
```

## Why this file exists at all

The divergence between spec and behavior is EXACTLY the failure mode the
drift mesh was built to log. Meta-consistent: divlog logs its own residual's
divergence from its own spec. The log records with enough detail to re-check
later, not a bug silently closed.

If the log fills with entries like this one and nobody ever runs E9 to
resolve any of them, the log has become a burial ground. The FIRST test of
"log actually becomes a baseline" (E16, T-tagged) is that some entry from
this file gets superseded by a later one whose `supersedes = 8a6a9e291671`.
Until that happens, this entry is the baseline; the shipped rule is what
`residual()` does; and the intent recorded here is what a future experiment
gets to argue against.
