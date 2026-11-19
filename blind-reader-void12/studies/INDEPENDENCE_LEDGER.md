# Independence ledger (2026-11-19)

Applies the owner's independence rules (`../MODE_SEQUENCE.md`, dated section of 2026-11-19) to every reading, review and check in this folder. One row per (what was read or checked, who read or checked it). Every field is filled, or `void` where unknown. An unknown field caps the level at the lowest level it could be.

The fields are taken from each record's own files (`RUN_NOTES.md`, `SENT_RECORD.json`, the confusion records' headers, `readings/README.md`); a `void` means no file states the field. The levels are computed from the fields by the rule. This file and its levels are the Claude Code session's work, which is itself an L0 actor for everything it implemented.

```text
field key   fam = model family    mem = memory from other conversations    ctx = project / context features
            exposure: P packet, K key or scores, R repository, I the implementation read or checked,
                      O other readers' records           y / n / ? (? = void)
```

## Readings of the packet (implementer of what they are compared with: the first reading's build session, Claude family)

```text
reading          reader           session                  fam     mem   ctx                       P  K  R  I  O   level
pilot-A          Claude session   fresh, isolated          Claude  ?     ?                         y  n  ?  n  n   L1 (same family; ? caps no lower)
pilot-B          Claude session   fresh, isolated          Claude  ?     ?                         y  n  ?  n  n   L1
claude-fresh-1   Claude session   not fresh (RUN_NOTES)    Claude  ?     ?                         y  ?  ?  ?  ?   L0 cap (not fresh; exposures void)
Claude-v2-A      this session     Claude Code, another     Claude  ?     another repository        y  ?  ?  ?  ?   L0 cap (this session later
                                  repository attached                    attached                                implemented the amendment)
Kimi-v2-A        Kimi             as sent                  Kimi    ?     task text with labels     y  n  ?  n  ?   L2 (O and R void: L3 not
                                                                         of earlier readings                     establishable)
GPT-6            GPT              repository URL and       GPT     ?     project context,          y  n  y  ?  ?   L2 (R = y rules out L3)
                                  project context                        repository URL
```

## Reviews of the study material (implementer: the Claude Code session)

```text
record   reader          session                       fam     mem  ctx                         P  K  R  I  O   level
CF       this session    same session                  Claude  --   another repository attached y  y  y  y  y   L0 self-review
CH       chat session    another session, reports only Claude  ?    ?                           n  y  ?  n  ?   L1 cap
KC       Kimi            reviewed study material at    Kimi    ?    ?                           y  y  ?  y  y   L2 (I = y: not L3)
                         158aa12
GR       Grok            fresh conversation            Grok    on   memory ON (owner's record)  y  ?  ?  y  ?   L2 (I = y: not L3;
                                                                                                                   memory on, so K R O
                                                                                                                   void, not n)
GR, after the record     Grok, same conversation       Grok    on   read the repository         y  y  y  y  y   not usable as an
                                                                                                                   independent reader
```

The KC and GR rows are both L2 and from two different families. Under "agreement between readers at the same level counts once", where they converge (G2, G3 in `GAPS.md`) it counts once, at L2, not twice.

## Checks (implementer: the Claude Code session unless stated)

```text
check                              kind           design by        design reviewed by        execution by     status
instrument/test_instrument.py      deterministic  this session     KC (L2) on M02 rules:     this session     execution valid (rerun
  + fixtures                                                       found the C11 drift;      (L0)             reproducible); design: REVIEW-2
                                                                   nothing else reviewed                      incomplete, so the pass is a
                                                                                                              self-audit, not independent
instrument/validate.py             deterministic  this session     none                      this session     self-audit only
instrument/arms.py                 deterministic  this session     none                      this session     self-audit only
m01_code.py coding (basis kinds)   judgment       this session     none                      this session     L0; a second coder needed
                                                                                                              (CF08, CF17)
packets/build_packet.py leak scan  deterministic  this session     none                      this session     self-audit only; its banned
                                                                                                              list is a judgment
key a1 derivation                  judgment +     Manus (fam ?)    the owner decided the     Manus            Manus not independent of the
  (derive_specific.py)             deterministic                   content (PREREG)          (fam ?)          key (PREREG); fam void, L0 cap
                                                                                                              for any check of it by Manus
scoring/score_v2.py tests          deterministic  build sessions   none recorded             this session     self-audit only
PR #320 fixture repair (7bc51bb)   judgment       this session     none                      --               needs REVIEW-2 by a reader other
                                   (rule design)                                                              than this session before it counts
```

## What changes because of this ledger

- **"Two readers independently" in `GAPS.md`.** KC and GR are both L2, so their convergence counts once. A dated note is added there.
- **PR #320 is test design,** so under A2 it is a judgment act by the implementer. The commit message's "the owner decides whether to merge" is replaced by the rule: it needs a REVIEW-2 reader other than this session. Nothing is merged here.
- **CF20 is a self-review row (L0)** that missed this session's own earlier repair at `7bc51bb`. That is the HOLDS line observed once more: correction in the CF record's dated section.
